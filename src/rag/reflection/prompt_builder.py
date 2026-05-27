"""Reflection Prompt 생성 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

REFLECTION_SYSTEM_PROMPT = """당신은 한국 주식 시장 금융 분석 품질 검토 전문가입니다.

역할:
- 이전 금융 분석 결과의 품질을 검토합니다.
- 과도한 낙관이나 비관 여부를 판별합니다.
- 누락된 리스크를 식별합니다.
- Context 부족 영역을 식별합니다.
- 분석 개선 방향을 제안합니다.

제한:
- 투자 추천을 하지 않습니다.
- 매수/매도 판단을 하지 않습니다.
- 새로운 분석을 생성하지 않습니다.
- 기존 분석에 대한 검토만 수행합니다.

응답 형식 (반드시 아래 JSON 형식으로만 응답):
{
  "reflection_summary": "전체 검토 요약 (2~3문장)",
  "missing_risks": ["누락된 리스크 1", "누락된 리스크 2"],
  "overconfidence_detected": true 또는 false,
  "overconfidence_reasons": ["과도한 낙관 근거 1"],
  "context_gaps": ["Context 부족 영역 1"],
  "improvement_suggestions": ["개선 제안 1", "개선 제안 2"]
}"""


def build_reflection_prompt(
    analysis_result: dict,
    evaluation: dict | None = None,
) -> list[dict]:
    """Reflection Prompt 메시지 목록을 생성한다.

    Args:
        analysis_result: 이전 분석 결과 dict.
        evaluation: Evaluation 결과 dict (선택).

    Returns:
        OpenAI Chat API messages 형식의 dict 목록.
    """
    query = analysis_result.get("query", "")
    persona = analysis_result.get("persona", "default")
    bullish = analysis_result.get("bullish_factors", [])
    bearish = analysis_result.get("bearish_factors", [])
    risks = analysis_result.get("risks", [])
    summary = analysis_result.get("summary", "")

    user_parts = [
        "다음 금융 분석 결과를 검토하세요.",
        "",
        f"[Query] {query}",
        f"[Persona] {persona}",
        "",
        "[상승 요인]",
    ]
    for b in bullish:
        user_parts.append(f"- {b}")

    user_parts.append("")
    user_parts.append("[하락 요인]")
    for b in bearish:
        user_parts.append(f"- {b}")

    user_parts.append("")
    user_parts.append("[리스크]")
    for r in risks:
        user_parts.append(f"- {r}")

    user_parts.append("")
    user_parts.append(f"[요약] {summary}")

    if evaluation:
        halluc = evaluation.get("hallucination_risk", {})
        rq = evaluation.get("retrieval_quality", {})
        cu = evaluation.get("context_usage", {})

        user_parts.append("")
        user_parts.append("[Evaluation]")
        user_parts.append(f"- hallucination_risk: {halluc.get('risk_level', '?')}")
        user_parts.append(f"- retrieval_relevant: {rq.get('has_relevant', '?')}")
        user_parts.append(f"- context_usage: {cu.get('usage_rating', '?')}")

        reasons = halluc.get("reasons", [])
        if reasons:
            user_parts.append(f"- halluc_reasons: {reasons}")

    user_parts.append("")
    user_parts.append(
        "위 분석을 검토하여 "
        "누락된 리스크, 과도한 낙관/비관 여부, "
        "Context 부족 영역, 개선 제안을 "
        "JSON 형식으로 응답하세요."
    )

    user_content = "\n".join(user_parts)

    messages = [
        {"role": "system", "content": REFLECTION_SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    logger.info(
        "build_reflection_prompt  query='%s'  persona=%s  eval=%s",
        query[:30], persona, "yes" if evaluation else "no",
    )
    return messages
