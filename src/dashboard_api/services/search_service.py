"""검색 트리거 — runtime_query_runner 위임."""
from __future__ import annotations

from src.runtime_flow.runtime_query_runner import run_runtime_query


def search_and_ingest(
    query: str,
    *,
    run_engine: bool = True,
    force: bool = False,
) -> dict:
    if not run_engine:
        from src.company_resolver.company_resolver import resolve_company
        from src.ingestion_pipeline.ingestion_runner import run_ingestion_for_company
        from src.ingestion_pipeline.vector_index_manager import _db_embedding_count

        resolved = resolve_company(query)
        if not resolved:
            return {
                "status": "failed",
                "error": "질문에서 회사를 식별할 수 없습니다.",
            }
        ing = run_ingestion_for_company(
            resolved, force=force or _db_embedding_count(resolved.ticker) < 1,
        )
        from .company_service import resolve_company_query
        company = resolve_company_query(query, prefetch=False)
        return {
            "status": ing.get("status", ""),
            "query": query,
            "company": company,
            "ingestion": {
                "status": ing.get("status", ""),
                "documents": int(ing.get("documents", 0)),
                "chunks": int(ing.get("chunks", 0)),
                "embeddings": int(ing.get("embeddings", 0)),
                "embeddings_created": int(ing.get("embeddings_created", 0)),
                "embeddings_skipped": int(ing.get("embeddings_skipped", 0)),
                "skipped_collectors": ing.get("skipped_collectors", []),
            },
            "trace_id": "",
            "engine_status": "",
        }

    rt = run_runtime_query(query, skip_ingestion=False)
    if rt.get("status") == "failed":
        return rt

    from .company_service import resolve_company_query
    company = resolve_company_query(query, prefetch=False)
    if company and rt.get("stats"):
        company["stats"] = rt["stats"]
        company["cache_ready"] = rt["stats"].get("embedding_count", 0) >= 3

    ing = rt.get("ingestion") or {}
    return {
        "status": rt.get("status", ""),
        "query": query,
        "company": company,
        "ingestion": {
            "status": ing.get("status", ""),
            "documents": int(ing.get("documents", 0)),
            "chunks": int(ing.get("chunks", 0)),
            "embeddings": int(ing.get("embeddings", 0)),
            "embeddings_created": int(ing.get("embeddings_created", 0)),
            "embeddings_skipped": int(ing.get("embeddings_skipped", 0)),
            "skipped_collectors": ing.get("skipped_collectors", []),
        },
        "trace_id": rt.get("trace_id", ""),
        "engine_status": rt.get("status", ""),
        "runtime_logs": rt.get("runtime_logs", []),
    }
