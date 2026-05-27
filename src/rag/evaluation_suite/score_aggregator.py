"""Engine Evaluation Score 집계 및 Report 저장 모듈."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from retrieval_evaluator import evaluate_retrieval
from reasoning_evaluator import evaluate_reasoning, evaluate_reflection
from memory_evaluator import evaluate_memory
from stock_chain_evaluator import evaluate_stock_chain

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation_suite"

WEIGHTS = {
    "retrieval_score": 0.20,
    "reasoning_score": 0.25,
    "reflection_score": 0.15,
    "memory_score": 0.20,
    "stock_chain_score": 0.20,
}


def evaluate_engine_run(
    unified_result: dict,
    trace: dict | None = None,
) -> dict:
    """Unified Engine 실행 결과를 종합 평가한다."""
    retrieval = evaluate_retrieval(unified_result)
    reasoning = evaluate_reasoning(unified_result, trace)
    reflection = evaluate_reflection(unified_result)
    memory = evaluate_memory(unified_result)
    stock_chain = evaluate_stock_chain(unified_result)

    scores = {
        "retrieval_score": retrieval["retrieval_score"],
        "reasoning_score": reasoning["reasoning_score"],
        "reflection_score": reflection["reflection_score"],
        "memory_score": memory["memory_score"],
        "stock_chain_score": stock_chain["stock_chain_score"],
    }

    overall_score = round(
        sum(scores[k] * WEIGHTS[k] for k in WEIGHTS), 4,
    )
    scores["overall_score"] = overall_score

    consistency = calculate_consistency_score(unified_result, trace, scores)
    hallucination = evaluate_hallucination_risk(unified_result)

    report = build_evaluation_report(
        unified_result, trace, scores,
        {
            "retrieval": retrieval,
            "reasoning": reasoning,
            "reflection": reflection,
            "memory": memory,
            "stock_chain": stock_chain,
        },
        consistency, hallucination,
    )

    logger.info("Engine 평가 완료  overall=%.4f", overall_score)
    return report


def calculate_consistency_score(
    unified_result: dict,
    trace: dict | None,
    scores: dict,
) -> dict:
    """엔진 단계 간 consistency를 평가한다."""
    checks: list[float] = []

    analysis = unified_result.get("analysis_result", {})
    reflection = unified_result.get("reflection_result", {})

    if analysis.get("summary") and reflection.get("reflection_summary"):
        checks.append(0.8)

    if unified_result.get("memory_updates", {}).get("analysis_memory"):
        checks.append(0.9)

    if (unified_result.get("event_graph") or {}).get("node_count", 0) > 0:
        checks.append(0.85)

    if trace:
        ok_steps = sum(1 for s in trace.get("steps", []) if s.get("status") == "ok")
        total_steps = len(trace.get("steps", []))
        if total_steps:
            checks.append(ok_steps / total_steps)

    score_variance = max(scores.values()) - min(
        v for k, v in scores.items() if k != "overall_score"
    )
    balance = 1.0 - min(score_variance, 0.5)
    checks.append(balance)

    consistency_score = round(
        sum(checks) / len(checks) if checks else 0.0, 4,
    )

    return {
        "consistency_score": consistency_score,
        "checks_passed": len(checks),
        "score_variance": round(score_variance, 4),
    }


def evaluate_hallucination_risk(unified_result: dict) -> dict:
    """hallucination risk를 평가한다."""
    eval_result = unified_result.get("evaluation_result", {})
    halluc = eval_result.get("hallucination_risk", {})
    reflection = unified_result.get("reflection_result", {})

    risk_level = halluc.get("risk_level", "medium")
    overconf = reflection.get("overconfidence_detected", False)

    risk_score = {"low": 0.1, "medium": 0.5, "high": 0.9}.get(risk_level, 0.5)
    if overconf:
        risk_score = min(risk_score + 0.15, 1.0)

    return {
        "risk_level": risk_level,
        "risk_score": round(risk_score, 4),
        "reasons": halluc.get("reasons", []),
        "overconfidence_detected": overconf,
    }


def build_evaluation_report(
    unified_result: dict,
    trace: dict | None,
    scores: dict,
    details: dict,
    consistency: dict,
    hallucination: dict,
) -> dict:
    """Evaluation Report dict를 생성한다."""
    return {
        "trace_id": unified_result.get("trace_id", ""),
        "query": unified_result.get("query", ""),
        "persona": unified_result.get("persona", ""),
        "ticker": unified_result.get("ticker", ""),
        "scores": scores,
        "consistency": consistency,
        "hallucination_risk": hallucination,
        "details": details,
        "trace_summary": {
            "step_count": len((trace or {}).get("steps", [])),
            "completed_at": unified_result.get("completed_at", ""),
        },
        "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def save_evaluation_report(
    report: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path:
    """Evaluation Report를 JSON으로 저장한다."""
    out = Path(output_dir) if output_dir else (DEFAULT_OUTPUT_DIR / "reports")
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        trace_id = report.get("trace_id", "report")
        query_slug = report.get("query", "")[:15].replace(" ", "_")
        filename = f"{query_slug}_{trace_id}_report.json"

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    logger.info("Evaluation Report 저장  %s", filepath.name)
    return filepath


def save_evaluation_trace(
    report: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path:
    """Evaluation trace를 저장한다."""
    out = Path(output_dir) if output_dir else (DEFAULT_OUTPUT_DIR / "traces")
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = f"{report.get('trace_id', 'eval')}_eval_trace.json"

    trace = {
        "trace_id": report.get("trace_id"),
        "query": report.get("query"),
        "scores": report.get("scores"),
        "consistency_score": report.get("consistency", {}).get("consistency_score"),
        "hallucination_risk": report.get("hallucination_risk"),
        "evaluated_at": report.get("evaluated_at"),
    }

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)

    logger.info("Evaluation trace 저장  %s", filepath.name)
    return filepath


def save_full_engine_score(
    scores: dict,
    output_dir: Path | str | None = None,
    filename: str = "full_engine_score.json",
) -> Path:
    """Full Engine Score를 scores/에 저장한다."""
    out = Path(output_dir) if output_dir else (DEFAULT_OUTPUT_DIR / "scores")
    out.mkdir(parents=True, exist_ok=True)

    entry = {
        **scores,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    filepath = out / filename
    existing: list[dict] = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing = data if isinstance(data, list) else [data]
        except (json.JSONDecodeError, Exception):
            existing = []

    existing.append(entry)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info("Full Engine Score 저장  overall=%.4f", scores.get("overall_score", 0))
    return filepath


def load_unified_result(trace_id: str | None = None) -> tuple[dict | None, dict | None]:
    """저장된 Unified Result와 Trace를 로드한다."""
    results_dir = PROJECT_ROOT / "data" / "unified_engine" / "final_results"
    traces_dir = PROJECT_ROOT / "data" / "unified_engine" / "traces"

    result = None
    trace = None

    if trace_id:
        rp = results_dir / f"{trace_id}_result.json"
        tp = traces_dir / f"{trace_id}_trace.json"
        if rp.exists():
            with open(rp, "r", encoding="utf-8") as f:
                result = json.load(f)
        if tp.exists():
            with open(tp, "r", encoding="utf-8") as f:
                trace = json.load(f)
        return result, trace

    if results_dir.exists():
        files = sorted(results_dir.glob("*_result.json"), reverse=True)
        if files:
            with open(files[0], "r", encoding="utf-8") as f:
                result = json.load(f)
            tid = result.get("trace_id", "")
            tp = traces_dir / f"{tid}_trace.json"
            if tp.exists():
                with open(tp, "r", encoding="utf-8") as f:
                    trace = json.load(f)

    return result, trace
