"""Disclosure retrieval timeout protection."""
from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

DEFAULT_TIMEOUT_SEC = 8.0


def run_with_timeout(
    fn: Callable[[], T],
    *,
    timeout_sec: float = DEFAULT_TIMEOUT_SEC,
    fallback: T | None = None,
    label: str = "disclosure",
) -> T | None:
    pool = ThreadPoolExecutor(max_workers=1)
    fut = pool.submit(fn)
    try:
        return fut.result(timeout=timeout_sec)
    except FuturesTimeout:
        fut.cancel()
        logger.warning("%s retrieval timeout  %.1fs", label, timeout_sec)
        return fallback
    except Exception:
        logger.exception("%s retrieval failed", label)
        return fallback
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
