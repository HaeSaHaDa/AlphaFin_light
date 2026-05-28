"""ingestion용 collector 모듈 로드 (sys.path 충돌 방지)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_collector_module(collector_dir: Path, label: str) -> ModuleType:
    path = collector_dir / "collector.py"
    mod_name = f"_ingest_collector_{label}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"collector 로드 실패: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_db_store() -> ModuleType:
    db_dir = Path(__file__).resolve().parents[1] / "common" / "db"
    path = db_dir / "store.py"
    mod_name = "_ingest_db_store"
    if mod_name in sys.modules:
        return sys.modules[mod_name]
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"store 로드 실패: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod
