"""Reflection 분석 모듈."""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REFLECTION_DIR = Path(__file__).resolve().parent

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "reflection_prompt_builder",
    REFLECTION_DIR / "prompt_builder.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
build_reflection_prompt = _mod.build_reflection_prompt

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-4o-mini"

_client: OpenAI | None = None


def _load_api_key() -> str:
    load_dotenv(PROJECT_ROOT / ".env")
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise ValueError("OPENAI_API_KEY가 .env에 설정되지 않았습니다.")
    return key


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=_load_api_key())
        logger.info("OpenAI Chat 클라이언트 초기화 완료")
    return _client


def _call_chat_api(messages: list[dict], model: str = DEFAULT_MODEL) -> dict:
    client = _get_client()
    try:
        resp = client.chat.completions.create(
            model=model, messages=messages,
            temperature=0.3, max_tokens=2000,
        )
        raw = resp.choices[0].message.content.strip()
        logger.info("Chat API 응답 수신  len=%d", len(raw))

        cleaned = raw
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [ln for ln in lines if not ln.strip().startswith("```")]
            cleaned = "\n".join(lines)

        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("JSON 파싱 실패 — raw 응답을 reflection_summary로 저장")
        return {
            "reflection_summary": raw,
            "missing_risks": [],
            "overconfidence_detected": False,
            "overconfidence_reasons": [],
            "context_gaps": [],
            "improvement_suggestions": [],
        }
    except Exception:
        logger.exception("Chat API 호출 실패")
        return {}


def analyze_reflection(
    analysis_result: dict,
    evaluation: dict | None = None,
    model: str = DEFAULT_MODEL,
) -> dict:
    """이전 분석 결과에 대한 Reflection을 생성한다.

    Args:
        analysis_result: 이전 분석 결과.
        evaluation: Evaluation 결과 (선택).
        model: Chat 모델명.

    Returns:
        Reflection dict.
    """
    logger.info(
        "=== analyze_reflection  query='%s' ===",
        analysis_result.get("query", "")[:30],
    )

    messages = build_reflection_prompt(analysis_result, evaluation)
    llm_reflection = _call_chat_api(messages, model)
    if not llm_reflection:
        return {"query": analysis_result.get("query", ""), "error": "Reflection 생성 실패"}

    rule_checks = _run_rule_based_checks(analysis_result, evaluation)

    reflection = {
        "query": analysis_result.get("query", ""),
        "persona": analysis_result.get("persona", "default"),
        "reflection_summary": llm_reflection.get("reflection_summary", ""),
        "missing_risks": _merge_lists(
            llm_reflection.get("missing_risks", []),
            rule_checks.get("missing_risks", []),
        ),
        "overconfidence_detected": (
            llm_reflection.get("overconfidence_detected", False)
            or rule_checks.get("overconfidence_detected", False)
        ),
        "overconfidence_reasons": _merge_lists(
            llm_reflection.get("overconfidence_reasons", []),
            rule_checks.get("overconfidence_reasons", []),
        ),
        "context_gaps": _merge_lists(
            llm_reflection.get("context_gaps", []),
            rule_checks.get("context_gaps", []),
        ),
        "improvement_suggestions": llm_reflection.get("improvement_suggestions", []),
        "model": model,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    logger.info(
        "Reflection 완료  missing_risks=%d  overconfidence=%s  gaps=%d  suggestions=%d",
        len(reflection["missing_risks"]),
        reflection["overconfidence_detected"],
        len(reflection["context_gaps"]),
        len(reflection["improvement_suggestions"]),
    )
    return reflection


def detect_overconfidence(analysis_result: dict) -> dict:
    """규칙 기반으로 과도한 낙관을 탐지한다."""
    bullish = analysis_result.get("bullish_factors", [])
    bearish = analysis_result.get("bearish_factors", [])
    risks = analysis_result.get("risks", [])

    detected = False
    reasons: list[str] = []

    if len(bullish) > len(bearish) + len(risks):
        detected = True
        reasons.append(
            f"상승 요인({len(bullish)})이 하락 요인({len(bearish)})+리스크({len(risks)})보다 많음"
        )

    if not risks:
        detected = True
        reasons.append("리스크 항목 없음")

    return {"overconfidence_detected": detected, "overconfidence_reasons": reasons}


def detect_missing_risks(analysis_result: dict) -> list[str]:
    """규칙 기반으로 누락된 리스크를 탐지한다."""
    missing: list[str] = []
    risks_text = " ".join(analysis_result.get("risks", []))
    summary = analysis_result.get("summary", "")
    all_text = risks_text + " " + summary

    risk_topics = [
        ("환율", "환율 변동 리스크"),
        ("금리", "금리 변동 리스크"),
        ("경쟁", "경쟁 심화 리스크"),
        ("규제", "규제 변동 리스크"),
        ("공급", "공급망 리스크"),
        ("지정학", "지정학적 리스크"),
    ]

    for keyword, risk_name in risk_topics:
        if keyword not in all_text:
            missing.append(risk_name)

    return missing[:3]


def detect_context_gaps(analysis_result: dict, evaluation: dict | None = None) -> list[str]:
    """Context 부족 영역을 탐지한다."""
    gaps: list[str] = []

    refs = analysis_result.get("referenced_chunks", [])
    doc_types = set(r.get("document_type", "") for r in refs)

    if "disclosure" not in doc_types:
        gaps.append("공시 데이터 미포함")
    if "news_article" not in doc_types:
        gaps.append("뉴스 데이터 미포함")

    if evaluation:
        cu = evaluation.get("context_usage", {})
        if cu.get("usage_rating") == "weak":
            gaps.append("Context 활용도 낮음")

    return gaps


def _run_rule_based_checks(
    analysis_result: dict,
    evaluation: dict | None = None,
) -> dict:
    overconf = detect_overconfidence(analysis_result)
    missing = detect_missing_risks(analysis_result)
    gaps = detect_context_gaps(analysis_result, evaluation)

    return {
        "overconfidence_detected": overconf["overconfidence_detected"],
        "overconfidence_reasons": overconf["overconfidence_reasons"],
        "missing_risks": missing,
        "context_gaps": gaps,
    }


def _merge_lists(list1: list, list2: list) -> list:
    seen: set[str] = set()
    merged: list = []
    for item in list1 + list2:
        if str(item) not in seen:
            seen.add(str(item))
            merged.append(item)
    return merged
