"""Disclosure-aware runtime query pipeline."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from src.runtime_flow.retrieval_executor import execute_retrieval
from src.runtime_flow.runtime_logger import RuntimeLogger

from .disclosure_runtime_integration import integrate_disclosure_runtime
from .runtime_context_assembler import assemble_runtime_context
from .unified_retrieval_builder import build_unified_retrieval

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENGINE_DIR = PROJECT_ROOT / "src" / "rag" / "unified_engine"
UNIFIED_RESULTS = PROJECT_ROOT / "data" / "unified_engine" / "final_results"


def _patch_unified_result(trace_id: str, runtime_context: dict) -> None:
    if not trace_id:
        return
    path = UNIFIED_RESULTS / f"{trace_id}_result.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data["runtime_context"] = runtime_context
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("runtime_context saved  trace_id=%s", trace_id)
    except Exception:
        logger.warning("runtime_context patch failed  trace_id=%s", trace_id, exc_info=True)


def run_disclosure_aware_engine(
    *,
    runtime_query: str,
    ticker: str,
    persona: str = "growth_investor",
    premerged_chunks: list[dict] | None = None,
    runtime_context: dict | None = None,
) -> dict:
    engine_dir = str(ENGINE_DIR)
    if engine_dir not in sys.path:
        sys.path.insert(0, engine_dir)
    from engine_runner import run_unified_pipeline  # type: ignore[import]

    return run_unified_pipeline(
        query=runtime_query,
        persona=persona,
        ticker=ticker,
        preloaded_chunks=premerged_chunks,
        runtime_context=runtime_context,
    )


def run_disclosure_aware_query(
    runtime_query: str,
    ticker: str,
    *,
    persona: str = "growth_investor",
    run_engine: bool = True,
    log: RuntimeLogger | None = None,
    news_freshness: dict | None = None,
    keywords: list[str] | None = None,
) -> dict:
    """News + disclosure unified retrieval → engine → runtime context."""
    log = log or RuntimeLogger()

    disc = integrate_disclosure_runtime(ticker, runtime_query)
    log.log(
        "Disclosure",
        f"collect={disc.get('collect_status')}  chunks={disc.get('disclosure_chunk_count', 0)}",
    )

    news_chunks = execute_retrieval(
        runtime_query,
        ticker,
        top_k=6,
        document_type="news_article",
    )
    news, disclosure, merged = build_unified_retrieval(
        runtime_query,
        ticker,
        news_chunks=news_chunks,
        disclosure_chunks=disc.get("disclosure_chunks") or [],
    )
    log.retrieval(len(merged), f"{ticker} (news+disclosure)")

    news_meta = news_freshness or {}
    disclosure_meta = disc.get("collect") or {}
    freshness = {
        "news": {
            "data_as_of": news_meta.get("news_data_as_of", ""),
            "last_collected_at": news_meta.get("cache_updated_at", ""),
            "cache_status": news_meta.get("cache_status", "UNKNOWN"),
            "ttl_hours": news_meta.get("cache_ttl_hours", 12),
        },
        "disclosure": {
            "data_as_of": disclosure_meta.get("data_as_of", ""),
            "last_collected_at": (
                disclosure_meta.get("cache_updated_at")
                or disclosure_meta.get("updated_at", "")
            ),
            "cache_status": disclosure_meta.get("cache_status", "UNKNOWN"),
            "ttl_hours": disclosure_meta.get("cache_ttl_hours", 12),
        },
    }
    runtime_context = assemble_runtime_context(
        ticker=ticker,
        query=runtime_query,
        news_chunks=news,
        disclosure_chunks=disclosure,
        merged_evidence=merged,
        collect_status=disc.get("collect_status", ""),
        freshness=freshness,
        keywords=keywords,
    )

    trace_id = ""
    engine_status = "skipped"
    if run_engine:
        if not merged:
            log.engine("partial — no merged chunks")
            engine_status = "partial"
        else:
            runtime_context["trace_id"] = ""
            result = run_disclosure_aware_engine(
                runtime_query=runtime_query,
                ticker=ticker,
                persona=persona,
                premerged_chunks=merged,
                runtime_context=runtime_context,
            )
            trace_id = result.get("trace_id", "")
            runtime_context["trace_id"] = trace_id
            _patch_unified_result(trace_id, runtime_context)
            chunk_n = int(result.get("retrieval_chunk_count", 0))
            engine_status = "completed" if chunk_n > 0 else "partial"
            log.engine("disclosure-aware reasoning completed")
            log.trace(trace_id)

    return {
        "trace_id": trace_id,
        "engine_status": engine_status,
        "runtime_context": runtime_context,
        "retrieval_chunk_count": len(merged),
        "news_chunk_count": len(news),
        "disclosure_chunk_count": len(disclosure),
        "disclosure_collect_status": disc.get("collect_status"),
        "freshness": freshness,
    }
