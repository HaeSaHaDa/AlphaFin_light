"""Stock Chain Propagation 계산 모듈."""
from __future__ import annotations

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DECAY_PER_HOP = 0.08


def calculate_propagation(chain: dict, start_source: str | None = None) -> list[dict]:
    """Chain 링크를 따라 propagation 경로와 impact를 계산한다."""
    links = chain.get("links", [])
    if not links:
        return []

    adjacency: dict[str, list[dict]] = {}
    for link in links:
        adjacency.setdefault(link["source"], []).append(link)

    if start_source is None:
        start_source = links[0]["source"]

    paths: list[dict] = []
    _dfs_propagate(start_source, adjacency, [], 1.0, paths, set())

    logger.info("calculate_propagation  paths=%d", len(paths))
    return paths


def _dfs_propagate(
    node: str,
    adjacency: dict[str, list[dict]],
    current_path: list[str],
    current_impact: float,
    results: list[dict],
    visited: set[str],
) -> None:
    path = current_path + [node]
    if len(path) >= 2:
        results.append({
            "path": list(path),
            "path_str": " → ".join(path),
            "cumulative_impact": round(current_impact, 4),
            "hop_count": len(path) - 1,
        })

    if node in visited or len(path) > 6:
        return
    visited.add(node)

    for link in adjacency.get(node, []):
        target = link["target"]
        hop_impact = current_impact * link.get("impact_score", 0.5)
        next_impact = max(hop_impact - DECAY_PER_HOP, 0.1)
        _dfs_propagate(
            target, adjacency, path, next_impact, results, visited.copy(),
        )


def propagate_market_impact(
    chain: dict,
    seed_event: str,
) -> dict:
    """시장 이벤트 시드로 영향 전파 결과를 생성한다."""
    links = chain.get("links", [])
    affected: list[dict] = []
    log_entries: list[dict] = []

    seed_links = [
        l for l in links
        if seed_event.lower() in l["source"].lower()
        or seed_event.lower() in l.get("relation_type", "").lower()
    ]

    if not seed_links:
        entities = chain.get("entities", [])
        for ent in entities:
            if seed_event.lower() in ent.get("name", "").lower():
                seed_links = [
                    l for l in links if l["source"] == ent["name"]
                ]
                if not seed_links:
                    seed_links = [
                        l for l in links if l["target"] == ent["name"]
                    ]
                break

    for link in seed_links:
        impact = link.get("impact_score", 0.5)
        entry = {
            "seed": seed_event,
            "source": link["source"],
            "target": link["target"],
            "relation_type": link["relation_type"],
            "impact_score": impact,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        log_entries.append(entry)
        affected.append({
            "entity": link["target"],
            "impact_score": impact,
            "via": link["source"],
        })

        secondary = [
            l for l in links if l["source"] == link["target"]
        ]
        for sec in secondary:
            sec_impact = round(impact * sec.get("impact_score", 0.5) - DECAY_PER_HOP, 4)
            log_entries.append({
                "seed": seed_event,
                "source": sec["source"],
                "target": sec["target"],
                "relation_type": sec["relation_type"],
                "impact_score": sec_impact,
                "hop": 2,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
            affected.append({
                "entity": sec["target"],
                "impact_score": sec_impact,
                "via": f"{link['source']} → {sec['source']}",
            })

    result = {
        "seed_event": seed_event,
        "affected_entities": affected,
        "propagation_log": log_entries,
        "total_affected": len(affected),
    }

    logger.info(
        "propagate_market_impact  seed='%s'  affected=%d  log=%d",
        seed_event[:20], len(affected), len(log_entries),
    )
    return result
