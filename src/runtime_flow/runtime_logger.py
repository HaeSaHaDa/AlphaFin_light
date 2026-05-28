"""Runtime 단계별 로그."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger("runtime_flow")


@dataclass
class RuntimeLogger:
    lines: list[str] = field(default_factory=list)

    def log(self, tag: str, message: str) -> None:
        line = f"[{tag}] {message}"
        self.lines.append(line)
        logger.info(line)

    def resolver(self, company: str, ticker: str) -> None:
        self.log("Resolver", f"{company} → {ticker}")

    def ingestion(self, status: str, detail: str = "") -> None:
        msg = status if not detail else f"{status}  {detail}"
        self.log("Ingestion", msg)

    def retrieval(self, count: int, ticker: str) -> None:
        self.log("Retrieval", f"retrieved {count} chunks  ticker={ticker}")

    def engine(self, status: str) -> None:
        self.log("Engine", status)

    def trace(self, trace_id: str) -> None:
        self.log("Trace", f"trace_id={trace_id} 생성 완료")
