"""Event Graph 저장 및 조회 모듈."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_GRAPH_DIR = PROJECT_ROOT / "data" / "event_graph"


def build_event_graph(
    nodes: list[dict],
    relations: list[dict],
    query: str = "",
    ticker: str | None = None,
) -> dict:
    """Event Graph dict를 생성한다."""
    graph = {
        "query": query,
        "ticker": ticker,
        "nodes": nodes,
        "relations": relations,
        "metadata": {
            "node_count": len(nodes),
            "relation_count": len(relations),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    }

    logger.info(
        "Event Graph 생성  노드=%d  관계=%d  query='%s'",
        len(nodes), len(relations), query[:30],
    )
    return graph


def save_event_graph(
    graph: dict,
    output_dir: Path | str | None = None,
    filename: str | None = None,
) -> Path | None:
    """Event Graph를 JSON으로 저장한다."""
    out = Path(output_dir) if output_dir else DEFAULT_GRAPH_DIR
    out.mkdir(parents=True, exist_ok=True)

    if filename is None:
        ticker = graph.get("ticker", "unknown")
        filename = f"{ticker}_event_graph.json"

    filepath = out / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    logger.info("Event Graph 저장  %s", filepath)
    return filepath


def load_event_graph(
    filepath: Path | str,
) -> dict | None:
    """저장된 Event Graph를 로드한다."""
    fp = Path(filepath)
    if not fp.exists():
        logger.warning("Graph 파일 없음  %s", fp)
        return None

    try:
        with open(fp, "r", encoding="utf-8") as f:
            graph = json.load(f)
        logger.info(
            "Graph 로드  노드=%d  관계=%d",
            len(graph.get("nodes", [])),
            len(graph.get("relations", [])),
        )
        return graph
    except (json.JSONDecodeError, Exception):
        logger.exception("Graph 파일 파싱 실패  %s", fp)
        return None


def load_related_graphs(
    ticker: str,
    graph_dir: Path | str | None = None,
) -> list[dict]:
    """특정 ticker 관련 Graph를 로드한다."""
    out = Path(graph_dir) if graph_dir else DEFAULT_GRAPH_DIR
    if not out.exists():
        return []

    results: list[dict] = []

    for fp in out.glob("*.json"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                graph = json.load(f)

            if graph.get("ticker") == ticker:
                results.append(graph)
                continue

            for node in graph.get("nodes", []):
                if node.get("ticker") == ticker:
                    results.append(graph)
                    break
        except (json.JSONDecodeError, Exception):
            logger.warning("Graph 파일 파싱 실패  %s", fp)

    logger.info(
        "관련 Graph 조회  ticker=%s  결과=%d건", ticker, len(results),
    )
    return results


def build_graph_context(graphs: list[dict], max_relations: int = 10) -> str:
    """Event Graph를 Prompt Context 문자열로 변환한다.

    Args:
        graphs: Graph dict 목록.
        max_relations: 최대 Relation 수.

    Returns:
        Graph Context 문자열.
    """
    parts: list[str] = ["[Event Graph]"]

    seen_relations: set[str] = set()
    count = 0

    for graph in graphs:
        for rel in graph.get("relations", []):
            if count >= max_relations:
                break

            key = f"{rel['source']}→{rel['target']}"
            if key in seen_relations:
                continue
            seen_relations.add(key)

            conf = rel.get("confidence", 0)
            rtype = rel.get("relation_type", "")
            parts.append(
                f"- {rel['source']} → {rel['target']}  "
                f"[{rtype}] (conf={conf:.2f})"
            )
            count += 1

    parts.append("")

    context = "\n".join(parts)
    logger.info(
        "Graph Context 생성  graphs=%d  relations=%d  len=%d",
        len(graphs), count, len(context),
    )
    return context
