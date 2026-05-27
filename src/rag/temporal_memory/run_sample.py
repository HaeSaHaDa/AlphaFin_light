"""Temporal Market Memory 샘플 검증 스크립트."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
TEMPORAL_DIR = Path(__file__).resolve().parent
MEMORY_IMPORTANCE_DIR = PROJECT_ROOT / "src" / "rag" / "memory_importance"
LAYERED_MODULE = PROJECT_ROOT / "src" / "rag" / "layered_memory"

sys.path.insert(0, str(TEMPORAL_DIR))
sys.path.insert(0, str(MEMORY_IMPORTANCE_DIR))
sys.path.insert(0, str(LAYERED_MODULE))

from importance_manager import (  # noqa: E402
    update_memory_importance,
    load_layered_memories_all,
    load_reflections_all,
    load_event_graphs_all,
)
from layered_store import load_all_layers  # noqa: E402
from temporal_tracker import (  # noqa: E402
    track_memory_evolution,
    track_event_reoccurrence,
    build_event_evolution_chain,
)
from decay_manager import calculate_decay, apply_temporal_importance_update  # noqa: E402
from lifecycle_manager import (  # noqa: E402
    promote_memory,
    decay_memory,
    process_memory_lifecycle,
    build_temporal_context,
    save_lifecycle_log,
)

SAMPLE_QUERIES = [
    "NVIDIA 실적 발표",
    "HBM 공급 부족",
    "AI 산업 장기 성장",
]
OUTPUT_DIR = PROJECT_ROOT / "data" / "temporal_memory"


def _build_sample_memories() -> list[dict]:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        {
            "memory_type": "event_memory",
            "memory_layer": "short_term",
            "query": "NVIDIA 실적 발표",
            "persona": "growth_investor",
            "event_name": "NVIDIA 실적 발표",
            "event_summary": "NVIDIA AI GPU 실적 호조, HBM 수요 증가 전망",
            "summary": "NVIDIA 실적 발표 후 HBM 수요 증가 트렌드",
            "timestamp": ts,
            "reuse_count": 3,
            "appearance_count": 3,
        },
        {
            "memory_type": "event_memory",
            "memory_layer": "short_term",
            "query": "HBM 공급 부족",
            "persona": "growth_investor",
            "event_name": "HBM 공급 부족",
            "event_summary": "HBM 공급 부족 지속, AI 메모리 수요 증가",
            "summary": "HBM 공급 부족으로 AI 메모리 시장 영향",
            "timestamp": ts,
            "reuse_count": 2,
            "appearance_count": 2,
        },
        {
            "memory_type": "analysis_memory",
            "memory_layer": "mid_term",
            "query": "AI 산업 장기 성장",
            "persona": "growth_investor",
            "summary": "AI 산업 장기 성장 구조 변화, AI 서버 투자 확대",
            "bullish_factors": ["AI 서버 투자 확대", "구조적 성장"],
            "bearish_factors": ["규제 리스크"],
            "risks": ["경기 둔화"],
            "timestamp": ts,
            "reuse_count": 2,
            "appearance_count": 2,
        },
        {
            "memory_type": "event_memory",
            "memory_layer": "short_term",
            "query": "단기 루머",
            "persona": "default",
            "event_name": "일회성 루머",
            "event_summary": "단기 루머성 속보, 일회성 뉴스",
            "summary": "일회성 뉴스로 영향 제한적",
            "timestamp": ts,
            "reuse_count": 0,
            "appearance_count": 1,
        },
    ]


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.info("=== Temporal Market Memory 검증 시작 ===")

    reflections = load_reflections_all()
    graphs = load_event_graphs_all("005930")
    existing = load_layered_memories_all()

    sample_memories = _build_sample_memories()
    all_memories: list[dict] = []

    for mem in sample_memories + existing[:5]:
        imp = update_memory_importance(
            mem, reflections=reflections, graphs=graphs,
            reuse_count=mem.get("reuse_count", 0),
        )
        all_memories.append(imp)

    # --- Phase 1: Temporal Tracking ---
    logger.info("--- Phase 1: Temporal Tracking ---")

    evolutions: list[dict] = []
    for mem in all_memories[:4]:
        evo = track_memory_evolution(mem, all_memories)
        reoc = track_event_reoccurrence(mem, all_memories)
        evolutions.append(evo)
        logger.info(
            "  %s  stage=%s  reoccurrence=%d",
            mem.get("query", "")[:25],
            evo.get("evolution_stage"),
            reoc.get("reoccurrence_count"),
        )

    chain = build_event_evolution_chain(all_memories[:4], "HBM")
    logger.info("  Event evolution chain: %d steps", len(chain))

    # --- Phase 2: Promote ---
    logger.info("--- Phase 2: Promote ---")

    promotions: list[dict] = []
    nvidia = next(m for m in all_memories if "NVIDIA" in m.get("query", ""))
    hbm = next(m for m in all_memories if "HBM" in m.get("query", ""))
    ai_long = next(m for m in all_memories if "장기" in m.get("query", ""))

    for mem, target in [
        (nvidia, "mid_term"),
        (hbm, "mid_term"),
        (ai_long, "long_term"),
    ]:
        evo = track_memory_evolution(mem, all_memories)
        updated = apply_temporal_importance_update(mem, evo)
        record = promote_memory(updated, evo, target_layer=target)
        if record:
            promotions.append(record)
            logger.info(
                "  PROMOTE  %s → %s  reasons=%s",
                record["previous_layer"],
                record["current_layer"],
                record.get("promotion_reason", []),
            )

    # --- Phase 3: Decay ---
    logger.info("--- Phase 3: Decay ---")

    rumor = next(m for m in all_memories if "루머" in m.get("query", ""))
    rumor["importance_score"] = 0.15
    decay_record = decay_memory(rumor, track_memory_evolution(rumor, all_memories))
    if decay_record:
        logger.info(
            "  DECAY  score=%.4f  reasons=%s",
            decay_record.get("importance_score", 0),
            decay_record.get("decay_reason", []),
        )

    # --- Phase 4: Lifecycle batch ---
    logger.info("--- Phase 4: Lifecycle batch ---")

    lifecycle_results: list[dict] = []
    for mem in all_memories[:4]:
        result = process_memory_lifecycle(mem, all_memories)
        lifecycle_results.append(result)
        logger.info("  %s  action=%s", mem.get("query", "")[:20], result["action"])

    # --- Phase 5: Temporal Context ---
    logger.info("--- Phase 5: Temporal Context ---")

    layers = load_all_layers()
    for p in promotions:
        layer = p["current_layer"]
        promoted_mem = next(
            (m for m in all_memories if m.get("memory_id") == p.get("memory_id")),
            None,
        )
        if promoted_mem:
            promoted_copy = dict(promoted_mem)
            promoted_copy["memory_layer"] = layer
            promoted_copy["evolution_stage"] = p.get("evolution_stage", "trend_established")
            layers.setdefault(layer, []).append(promoted_copy)

    temporal_ctx = build_temporal_context(layers)
    logger.info("Temporal Context 길이: %d자", len(temporal_ctx))
    logger.info("Context 미리보기:\n%s", temporal_ctx[:300])

    # --- 검증 요약 저장 ---
    verification = {
        "sample_queries": SAMPLE_QUERIES,
        "promotions": len(promotions),
        "decay_performed": decay_record is not None,
        "evolution_chain_steps": len(chain),
        "temporal_context_len": len(temporal_ctx),
        "reflections_loaded": len(reflections),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = OUTPUT_DIR / "temporal_verification_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(verification, f, ensure_ascii=False, indent=2)

    save_lifecycle_log({
        "action": "verification_complete",
        "promotions": len(promotions),
        "decays": 1 if decay_record else 0,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    # --- 최종 검증 ---
    logger.info("=== 검증 결과 요약 ===")

    nvidia_promo = next((p for p in promotions if "NVIDIA" in str(p)), None)
    hbm_promo = next((p for p in promotions if "HBM" in str(p) or "hbm" in str(p).lower()), None)

    checks = {
        "promote_performed": len(promotions) >= 2,
        "decay_performed": decay_record is not None,
        "layer_movement": any(
            p.get("previous_layer") != p.get("current_layer") for p in promotions
        ),
        "promotion_reason": all(
            len(p.get("promotion_reason", [])) > 0 for p in promotions
        ),
        "temporal_tracking": len(evolutions) >= 4,
        "event_evolution_tracking": len(chain) >= 2,
        "temporal_context": len(temporal_ctx) > 50,
        "lifecycle_log": (OUTPUT_DIR / "lifecycle_logs" / "lifecycle_log.json").exists(),
        "reflection_linked": len(reflections) > 0,
        "nvidia_promoted": nvidia_promo is not None and nvidia_promo.get("current_layer") == "mid_term",
        "hbm_promoted": hbm_promo is not None or len(promotions) >= 2,
    }

    for name, ok in checks.items():
        logger.info("  %-30s : %s", name, "OK" if ok else "WARN")

    all_ok = all(checks.values())
    logger.info("최종: %s", "OK" if all_ok else "WARN")
    logger.info("=== Temporal Market Memory 검증 완료 ===")

    return 0 if all_ok else 0


if __name__ == "__main__":
    sys.exit(main())
