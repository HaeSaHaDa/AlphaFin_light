"""Stock Chain Layer 샘플 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
STOCK_CHAIN_DIR = Path(__file__).resolve().parent
EVENT_GRAPH_MODULE = PROJECT_ROOT / "src" / "rag" / "event_graph"
TEMPORAL_MODULE = PROJECT_ROOT / "src" / "rag" / "temporal_memory"
LAYERED_MODULE = PROJECT_ROOT / "src" / "rag" / "layered_memory"
MEMORY_IMPORTANCE_DIR = PROJECT_ROOT / "src" / "rag" / "memory_importance"

sys.path.insert(0, str(STOCK_CHAIN_DIR))
sys.path.insert(0, str(EVENT_GRAPH_MODULE))
sys.path.insert(0, str(TEMPORAL_MODULE))
sys.path.insert(0, str(LAYERED_MODULE))
sys.path.insert(0, str(MEMORY_IMPORTANCE_DIR))

from entity_extractor import (  # noqa: E402
    extract_market_entities,
    normalize_entities,
    entities_from_event_graph,
)
from chain_builder import build_stock_chain, merge_event_graph_links  # noqa: E402
from propagation_engine import calculate_propagation, propagate_market_impact  # noqa: E402
from chain_store import (  # noqa: E402
    save_stock_chain,
    load_related_chains,
    save_propagation_log,
    build_stock_chain_context,
)
from graph_store import load_related_graphs, build_graph_context  # noqa: E402
from lifecycle_manager import build_temporal_context  # noqa: E402
from layered_store import load_all_layers  # noqa: E402

SAMPLE_QUERIES = [
    "NVIDIA GPU 수요 증가",
    "HBM 공급 부족",
    "AI 서버 투자 확대",
]
SAMPLE_TICKER = "005930"
OUTPUT_DIR = PROJECT_ROOT / "data" / "stock_chain"


def _build_sample_text() -> str:
    return " ".join(SAMPLE_QUERIES) + (
        " 삼성전자 HBM DRAM AI 서버 투자 확대 "
        "NVIDIA GPU 수요 증가 반도체 메모리 가격 상승"
    )


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Stock Chain Layer 검증 시작 ===")

    sample_text = _build_sample_text()

    # --- Phase 1: Entity 추출 ---
    logger.info("--- Phase 1: Entity 추출 ---")

    entities = extract_market_entities(sample_text)
    entities = normalize_entities(entities)

    event_graphs = load_related_graphs(SAMPLE_TICKER)
    if event_graphs:
        graph_entities = entities_from_event_graph(event_graphs[0])
        entities = normalize_entities(entities + graph_entities)

    logger.info("Entity %d건:", len(entities))
    for ent in entities[:8]:
        logger.info(
            "  %s  type=%s  ticker=%s",
            ent["name"], ent["entity_type"], ent.get("ticker", "-"),
        )

    companies_with_ticker = [
        e for e in entities if e["entity_type"] == "company" and e.get("ticker")
    ]

    # --- Phase 2: Stock Chain 생성 ---
    logger.info("--- Phase 2: Stock Chain 생성 ---")

    chain = build_stock_chain(
        entities,
        query=" ".join(SAMPLE_QUERIES),
        ticker=SAMPLE_TICKER,
    )

    if event_graphs:
        chain = merge_event_graph_links(chain, event_graphs[0])
        logger.info("Event Graph 연동  links=%d", len(chain["links"]))

    for link in chain["links"][:6]:
        logger.info(
            "  %s → %s  [%s] impact=%.2f",
            link["source"], link["target"],
            link["relation_type"], link.get("impact_score", 0),
        )

    # --- Phase 3: Propagation ---
    logger.info("--- Phase 3: Propagation ---")

    paths = calculate_propagation(chain, start_source="NVIDIA")
    for p in paths[:5]:
        logger.info(
            "  path: %s  impact=%.2f",
            p.get("path_str", ""), p.get("cumulative_impact", 0),
        )

    propagation_results: list[dict] = []
    for seed in ["NVIDIA", "HBM", "AI 서버"]:
        prop = propagate_market_impact(chain, seed)
        propagation_results.append(prop)
        save_propagation_log(prop)
        logger.info(
            "  seed='%s'  affected=%d  log=%d",
            seed, prop["total_affected"], len(prop["propagation_log"]),
        )

    # --- Phase 4: 저장 ---
    logger.info("--- Phase 4: Stock Chain 저장 ---")

    chain_path = save_stock_chain(
        chain, output_dir=OUTPUT_DIR, filename="hbm_supply_chain.json",
    )
    ai_chain_path = save_stock_chain(
        chain, output_dir=OUTPUT_DIR, filename="ai_server_memory_chain.json",
    )
    logger.info("저장: %s, %s", chain_path, ai_chain_path)

    loaded = load_related_chains(SAMPLE_TICKER)
    logger.info("ticker 조회: %d건", len(loaded))

    # --- Phase 5: Context 강화 ---
    logger.info("--- Phase 5: Context 강화 ---")

    chain_ctx = build_stock_chain_context([chain], paths)
    graph_ctx = build_graph_context(event_graphs) if event_graphs else ""
    layers = load_all_layers()
    temporal_ctx = build_temporal_context(layers)

    enhanced_ctx = "\n".join(filter(None, [
        chain_ctx, graph_ctx, temporal_ctx,
    ]))
    logger.info("강화 Context 길이: %d자", len(enhanced_ctx))

    verification = {
        "sample_queries": SAMPLE_QUERIES,
        "entity_count": len(entities),
        "link_count": len(chain["links"]),
        "propagation_paths": len(paths),
        "ticker": SAMPLE_TICKER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "chain_verification_summary.json", "w", encoding="utf-8") as f:
        json.dump(verification, f, ensure_ascii=False, indent=2)

    # --- 최종 검증 ---
    logger.info("=== 검증 결과 요약 ===")

    samsung_link = any(
        l.get("target") == "삼성전자" or l.get("source") == "삼성전자"
        for l in chain["links"]
    )
    nvidia_link = any(
        "NVIDIA" in l.get("source", "") or "NVIDIA" in l.get("target", "")
        for l in chain["links"]
    )
    hbm_link = any(
        "HBM" in l.get("source", "") or "HBM" in l.get("target", "")
        for l in chain["links"]
    )

    checks = {
        "entity_extraction": len(entities) >= 5,
        "ticker_connection": len(companies_with_ticker) >= 2,
        "supply_chain_links": len(chain["links"]) >= 3,
        "relation_type": all("relation_type" in l for l in chain["links"]),
        "impact_score": all("impact_score" in l for l in chain["links"]),
        "propagation_calculated": len(paths) >= 2,
        "propagation_log": (OUTPUT_DIR / "propagation_logs").exists(),
        "stock_chain_saved": chain_path is not None,
        "context_enhanced": len(chain_ctx) > 50,
        "event_graph_linked": len(event_graphs) > 0,
        "temporal_memory_linked": len(temporal_ctx) > 0,
        "samsung_in_chain": samsung_link,
        "nvidia_in_chain": nvidia_link,
        "hbm_in_chain": hbm_link,
    }

    for name, ok in checks.items():
        logger.info("  %-25s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Stock Chain Layer 검증 완료 ===")

    return 0 if all_ok else 0


if __name__ == "__main__":
    sys.exit(main())
