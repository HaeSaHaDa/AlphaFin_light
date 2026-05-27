"""Memory Importance System 샘플 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MEMORY_IMPORTANCE_DIR = Path(__file__).resolve().parent
LAYERED_MODULE = PROJECT_ROOT / "src" / "rag" / "layered_memory"
sys.path.insert(0, str(MEMORY_IMPORTANCE_DIR))
sys.path.insert(0, str(LAYERED_MODULE))

from importance_calculator import calculate_importance, calculate_importance_factors  # noqa: E402
from importance_manager import (  # noqa: E402
    update_memory_importance,
    rank_memories_by_importance,
    prioritize_for_retrieval,
    load_layered_memories_all,
    load_reflections_all,
    load_event_graphs_all,
    save_importance_record,
    apply_retention_to_memory,
)
from retention_policy import should_promote_memory, should_decay_memory  # noqa: E402
from layered_store import save_layered_memory  # noqa: E402

SAMPLE_QUERIES = [
    "NVIDIA 실적 발표",
    "HBM 공급 부족",
    "AI 메모리 시장 성장",
]
OUTPUT_DIR = PROJECT_ROOT / "data" / "memory_importance"


def _build_sample_memories() -> list[dict]:
    """샘플 Memory 목록을 생성한다."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        {
            "memory_type": "event_memory",
            "memory_layer": "short_term",
            "query": "NVIDIA 실적 발표",
            "persona": "growth_investor",
            "event_name": "NVIDIA 실적 발표",
            "event_summary": "NVIDIA AI GPU 실적 호조, 데이터센터 매출 급증",
            "summary": "NVIDIA 실적 발표로 AI 반도체 수요 전망 강화",
            "timestamp": ts,
            "reuse_count": 3,
        },
        {
            "memory_type": "event_memory",
            "memory_layer": "short_term",
            "query": "HBM 공급 부족",
            "persona": "growth_investor",
            "event_name": "HBM 공급 부족",
            "event_summary": "HBM 공급 부족 지속, AI 서버 투자 확대로 수요 증가",
            "summary": "HBM 공급 부족으로 메모리 가격 상승 압력",
            "timestamp": ts,
            "reuse_count": 2,
        },
        {
            "memory_type": "analysis_memory",
            "memory_layer": "short_term",
            "query": "AI 메모리 시장 성장",
            "persona": "growth_investor",
            "summary": "AI 메모리 시장 성장, HBM 및 DRAM 수요 증가 전망",
            "bullish_factors": ["AI 서버 투자 확대", "HBM 수요 증가"],
            "bearish_factors": ["경쟁 심화"],
            "risks": ["공급 과잉 가능성"],
            "timestamp": ts,
            "reuse_count": 1,
        },
        {
            "memory_type": "event_memory",
            "query": "단기 루머",
            "persona": "default",
            "event_name": "일회성 뉴스",
            "event_summary": "단기 루머성 속보, 영향 범위 제한적",
            "summary": "일회성 뉴스로 시장 영향 미미",
            "timestamp": ts,
            "reuse_count": 0,
            "memory_layer": "short_term",
        },
    ]


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Memory Importance System 검증 시작 ===")

    reflections = load_reflections_all()
    graphs = load_event_graphs_all("005930")
    layered_existing = load_layered_memories_all()
    logger.info(
        "로드  reflections=%d  graphs=%d  layered=%d",
        len(reflections), len(graphs), len(layered_existing),
    )

    sample_memories = _build_sample_memories()
    all_memories = sample_memories + layered_existing

    # --- Phase 1: Importance 계산 ---
    logger.info("--- Phase 1: Importance 계산 ---")

    updated: list[dict] = []
    for mem in all_memories:
        reuse = mem.get("reuse_count", 0)
        result = update_memory_importance(
            mem, reflections=reflections, graphs=graphs, reuse_count=reuse,
        )
        updated.append(result)
        logger.info(
            "  %s  score=%.4f  factors=%s",
            result.get("query", result.get("event_name", ""))[:25],
            result["importance_score"],
            list(result.get("importance_factors", {}).keys()),
        )

    # --- Phase 2: Ranking ---
    logger.info("--- Phase 2: Importance Ranking ---")

    ranked = rank_memories_by_importance(updated)
    for mem in ranked[:5]:
        logger.info(
            "  rank=%d  score=%.4f  query='%s'",
            mem.get("importance_rank", 0),
            mem.get("importance_score", 0),
            mem.get("query", mem.get("event_name", ""))[:30],
        )

    top = ranked[0] if ranked else None
    bottom = ranked[-1] if ranked else None

    # --- Phase 3: Retrieval 우선순위 ---
    logger.info("--- Phase 3: Retrieval 우선순위 ---")

    for query in SAMPLE_QUERIES:
        prioritized = prioritize_for_retrieval(updated, query, max_results=3)
        logger.info("  Query='%s'", query)
        for p in prioritized:
            logger.info(
                "    priority=%.4f  importance=%.4f  %s",
                p.get("retrieval_priority_score", 0),
                p.get("importance_score", 0),
                p.get("query", p.get("event_name", ""))[:25],
            )

    # --- Phase 4: Retention 정책 ---
    logger.info("--- Phase 4: Retention 정책 ---")

    promote_count = 0
    decay_count = 0
    for mem in updated:
        retained = apply_retention_to_memory(mem)
        if should_promote_memory(retained):
            promote_count += 1
            logger.info(
                "  PROMOTE  score=%.4f  %s → %s  query='%s'",
                retained["importance_score"],
                retained.get("memory_layer", "?"),
                retained.get("promote_target_layer", "?"),
                retained.get("query", "")[:25],
            )
        if should_decay_memory(retained):
            decay_count += 1
            logger.info(
                "  DECAY  score=%.4f  %s",
                retained["importance_score"],
                retained.get("query", "")[:25],
            )

    # --- Phase 5: Layered Memory 연동 저장 ---
    logger.info("--- Phase 5: Layered Memory 연동 ---")

    for mem in sample_memories[:3]:
        imp = update_memory_importance(
            mem, reflections=reflections, graphs=graphs,
            reuse_count=mem.get("reuse_count", 0),
        )
        save_layered_memory(imp)
        save_importance_record(
            {
                "memory_id": imp["memory_id"],
                "query": imp.get("query", ""),
                "importance_score": imp["importance_score"],
                "importance_factors": imp["importance_factors"],
                "importance_reasons": imp["importance_reasons"],
                "retention_action": imp["retention_action"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            output_dir=OUTPUT_DIR,
            filename="sample_importance_verification.json",
        )

    verification = {
        "sample_queries": SAMPLE_QUERIES,
        "ranked_top": {
            "query": top.get("query", "") if top else "",
            "importance_score": top.get("importance_score", 0) if top else 0,
        },
        "ranked_bottom": {
            "query": bottom.get("query", "") if bottom else "",
            "importance_score": bottom.get("importance_score", 0) if bottom else 0,
        },
        "promote_count": promote_count,
        "decay_count": decay_count,
        "total_memories": len(updated),
    }
    out_path = OUTPUT_DIR / "importance_verification_summary.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(verification, f, ensure_ascii=False, indent=2)
    logger.info("검증 요약 저장  %s", out_path)

    # --- 최종 검증 ---
    logger.info("=== 검증 결과 요약 ===")

    nvidia_mem = next(
        (m for m in updated if "NVIDIA" in m.get("query", "") or "NVIDIA" in m.get("event_name", "")),
        None,
    )
    rumor_mem = next(
        (m for m in updated if "루머" in m.get("query", "") or "일회성" in m.get("summary", "")),
        None,
    )

    checks = {
        "importance_score_generated": all(
            "importance_score" in m for m in updated[:4]
        ),
        "importance_factors": all(
            "importance_factors" in m for m in updated[:4]
        ),
        "importance_ranking": (
            top is not None
            and bottom is not None
            and top.get("importance_score", 0) >= bottom.get("importance_score", 0)
        ),
        "high_importance_nvidia": (
            nvidia_mem is not None and nvidia_mem.get("importance_score", 0) >= 0.3
        ),
        "low_importance_rumor": (
            rumor_mem is not None
            and nvidia_mem is not None
            and rumor_mem.get("importance_score", 0) < nvidia_mem.get("importance_score", 0)
        ),
        "retrieval_priority": len(
            prioritize_for_retrieval(updated, "HBM 공급 부족", max_results=1),
        ) > 0,
        "promote_judgment": promote_count > 0 or any(
            should_promote_memory(m) for m in updated if m.get("importance_score", 0) >= 0.55
        ),
        "decay_judgment": decay_count > 0 or any(
            should_decay_memory(m) for m in updated
        ),
        "reflection_boost": any(
            m.get("reflection_mentions", 0) > 0 for m in updated
        ),
        "layered_memory_linked": (OUTPUT_DIR / "sample_importance_verification.json").exists(),
    }

    for name, ok in checks.items():
        logger.info("  %-35s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Memory Importance System 검증 완료 ===")

    return 0 if all_ok else 0


if __name__ == "__main__":
    sys.exit(main())
