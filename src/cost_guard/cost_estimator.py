"""예상 OpenAI 비용 계산 (USD)."""
from __future__ import annotations

# text-embedding-3-small: $0.02 / 1M tokens (approx)
# gpt-4o-mini: input $0.15 / 1M, output $0.60 / 1M (approx)

EMBEDDING_PRICE_PER_1M = 0.02
CHAT_INPUT_PRICE_PER_1M = 0.15
CHAT_OUTPUT_PRICE_PER_1M = 0.60


def estimate_embedding_cost(token_count: int) -> float:
    return round(token_count / 1_000_000 * EMBEDDING_PRICE_PER_1M, 6)


def estimate_chat_cost(prompt_tokens: int, completion_tokens: int) -> float:
    inp = prompt_tokens / 1_000_000 * CHAT_INPUT_PRICE_PER_1M
    out = completion_tokens / 1_000_000 * CHAT_OUTPUT_PRICE_PER_1M
    return round(inp + out, 6)


def estimate_usage_cost(totals: dict) -> float:
    emb = estimate_embedding_cost(totals.get("embedding_tokens", 0))
    chat = estimate_chat_cost(
        totals.get("prompt_tokens", 0),
        totals.get("completion_tokens", 0),
    )
    return round(emb + chat, 6)
