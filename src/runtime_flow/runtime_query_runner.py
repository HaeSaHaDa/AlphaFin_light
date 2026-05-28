"""Runtime Query Runner — 검색어 기반 End-to-End 실행."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.company_master.query_builder import build_runtime_query
from src.company_master.ticker_selection_service import (
    SelectedCompany,
    to_resolved_company,
)
from src.company_resolver.company_resolver import resolve_company
from src.ingestion_pipeline.ingestion_runner import run_ingestion_for_company
from src.ingestion_pipeline.ticker_stats import get_ticker_stats
from src.ingestion_pipeline.vector_index_manager import _db_embedding_count, is_ticker_ready

from .dashboard_response_builder import build_dashboard_bundle
from .retrieval_executor import execute_retrieval
from .runtime_context_builder import RuntimeContext
from .runtime_logger import RuntimeLogger

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENGINE_DIR = PROJECT_ROOT / "src" / "rag" / "unified_engine"


def run_runtime_query_selected(
    ticker: str,
    company_name: str,
    keywords: list[str] | None = None,
    *,
    corp_code: str = "",
    market: str = "KOSPI",
    persona: str = "growth_investor",
    skip_ingestion: bool = False,
    run_engine: bool = True,
) -> dict:
    """확정 ticker + topic keywords 기반 Runtime."""
    log = RuntimeLogger()
    kw = keywords or []
    runtime_query = build_runtime_query(company_name, ticker, kw)

    sel = SelectedCompany(
        ticker=ticker,
        company_name=company_name,
        corp_code=corp_code,
        market=market,
    )
    resolved = to_resolved_company(sel)

    log.resolver(f"{company_name} (selected)", ticker)
    log.log("Query", runtime_query)

    if not skip_ingestion:
        cache_hit = is_ticker_ready(ticker)
        force = _db_embedding_count(ticker) < 1
        ing = run_ingestion_for_company(resolved, force=force)
        if cache_hit and ing.get("status") == "cached":
            log.ingestion("cache hit", f"embeddings={ing.get('embeddings', 0)}")
        else:
            log.ingestion(
                ing.get("status", "?"),
                f"docs={ing.get('documents', 0)}",
            )
    else:
        ing = {}

    chunks = execute_retrieval(runtime_query, ticker, top_k=8)
    log.retrieval(len(chunks), ticker)

    trace_id = ""
    engine_status = "failed"
    if run_engine:
        engine_dir = str(ENGINE_DIR)
        if engine_dir not in sys.path:
            sys.path.insert(0, engine_dir)
        from engine_runner import run_unified_pipeline  # type: ignore[import]

        result = run_unified_pipeline(
            query=runtime_query,
            persona=persona,
            ticker=ticker,
        )
        trace_id = result.get("trace_id", "")
        chunk_n = int(result.get("retrieval_chunk_count", 0))
        engine_status = "completed" if chunk_n > 0 else "partial"
        if chunk_n > 0:
            log.engine("runtime reasoning completed")
        else:
            log.engine("partial")
        log.trace(trace_id)

    stats = get_ticker_stats(ticker)
    return {
        "status": engine_status,
        "query": runtime_query,
        "runtime_query": runtime_query,
        "ticker": ticker,
        "company_name": company_name,
        "keywords": kw,
        "corp_code": corp_code,
        "trace_id": trace_id,
        "retrieval_chunk_count": len(chunks),
        "ingestion": ing if not skip_ingestion else {},
        "stats": stats,
        "runtime_logs": log.lines,
    }


def run_runtime_query(
    query: str,
    *,
    persona: str = "growth_investor",
    skip_ingestion: bool = False,
) -> dict:
    """Query → Resolver → Ingestion → Retrieval → Engine → Trace."""
    log = RuntimeLogger()
    ctx = RuntimeContext(query=query, persona=persona)

    resolved = resolve_company(query)
    if not resolved:
        log.log("Resolver", "회사 식별 실패")
        return {
            "status": "failed",
            "error": "질문에서 회사를 식별할 수 없습니다. 회사명을 포함해 주세요.",
            "runtime_logs": log.lines,
        }

    ctx.company = resolved
    ctx.ticker = resolved.ticker
    log.resolver(resolved.company_name, resolved.ticker)

    if not skip_ingestion:
        cache_hit = is_ticker_ready(resolved.ticker)
        force = _db_embedding_count(resolved.ticker) < 1
        ing = run_ingestion_for_company(resolved, force=force)
        ctx.ingestion = ing
        if cache_hit and ing.get("status") == "cached":
            log.ingestion("cache hit", f"embeddings={ing.get('embeddings', 0)}")
        else:
            log.ingestion(
                ing.get("status", "?"),
                f"docs={ing.get('documents', 0)} emb+={ing.get('embeddings_created', 0)}",
            )
    else:
        log.ingestion("skipped", "skip_ingestion=true")

    chunks = execute_retrieval(query, resolved.ticker, top_k=8)
    ctx.retrieval_chunks = chunks
    log.retrieval(len(chunks), resolved.ticker)

    engine_dir = str(ENGINE_DIR)
    if engine_dir not in sys.path:
        sys.path.insert(0, engine_dir)
    from engine_runner import run_unified_pipeline  # type: ignore[import]

    ctx.engine_result = run_unified_pipeline(
        query=query,
        persona=persona,
        ticker=resolved.ticker,
    )
    ctx.trace_id = ctx.engine_result.get("trace_id", "")
    chunk_n = int(ctx.engine_result.get("retrieval_chunk_count", 0))
    if chunk_n > 0:
        log.engine("runtime reasoning completed")
    else:
        log.engine("partial — retrieval chunks 0")
    log.trace(ctx.trace_id)

    stats = get_ticker_stats(resolved.ticker)
    bundle = build_dashboard_bundle(ctx.trace_id) if ctx.trace_id else None

    engine_status = "completed" if chunk_n > 0 else "partial"
    return {
        "status": engine_status,
        "query": query,
        "ticker": resolved.ticker,
        "company_name": resolved.company_name,
        "corp_code": resolved.corp_code,
        "trace_id": ctx.trace_id,
        "retrieval_chunk_count": chunk_n,
        "ingestion": ctx.ingestion,
        "stats": stats,
        "runtime_logs": log.lines,
        "dashboard": bundle,
    }


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    parser = argparse.ArgumentParser(description="Runtime query runner")
    parser.add_argument("query", nargs="?", default="현대자동차 전기차 전망")
    args = parser.parse_args()

    result = run_runtime_query(args.query)
    for line in result.get("runtime_logs", []):
        print(line)
    print("---")
    print(
        f"status={result.get('status')}  trace_id={result.get('trace_id')}  "
        f"ticker={result.get('ticker')}",
    )
    return 0 if result.get("status") in ("completed", "partial") else 1


if __name__ == "__main__":
    raise SystemExit(main())
