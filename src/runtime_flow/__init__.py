"""Runtime Query → DB → Retrieval → Engine → Trace → Dashboard."""

from __future__ import annotations


def run_runtime_query(*args, **kwargs):
    from .runtime_query_runner import run_runtime_query as _run_runtime_query

    return _run_runtime_query(*args, **kwargs)

__all__ = ["run_runtime_query"]
