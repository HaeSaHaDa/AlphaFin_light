"""Persona 기반 Prompt 생성 모듈."""
from __future__ import annotations

import logging

from personas import get_persona_config

logger = logging.getLogger(__name__)

BASE_RULES = """제한:
- 투자 추천을 하지 않습니다.
- 매수/매도 판단을 하지 않습니다.
- 확정적 예측을 하지 않습니다.
- Context에 없는 정보를 만들어내지 않습니다.

응답 형식 (반드시 아래 JSON 형식으로만 응답):
{
  "bullish_factors": ["상승 요인 1", "상승 요인 2"],
  "bearish_factors": ["하락 요인 1", "하락 요인 2"],
  "risks": ["리스크 1", "리스크 2"],
  "summary": "전체 분석 요약 (2~3문장)"
}"""


def build_character_prompt(
    persona_name: str,
    query: str,
    context: str,
) -> list[dict]:
    """Persona 기반 Chat API 메시지 목록을 생성한다.

    Args:
        persona_name: Persona 이름 (예: "growth_investor").
        query: 사용자 분석 질문.
        context: RAG Context 문자열.

    Returns:
        OpenAI Chat API messages 형식의 dict 목록.

    Raises:
        ValueError: Persona가 존재하지 않을 때.
    """
    config = get_persona_config(persona_name)
    if config is None:
        raise ValueError(f"존재하지 않는 Persona: {persona_name}")

    system_content = (
        f"당신은 한국 주식 시장 전문 금융 분석 보조입니다.\n\n"
        f"[Persona: {config['name']}]\n"
        f"{config['system_instruction']}\n\n"
        f"{BASE_RULES}"
    )

    user_content = (
        f"다음 질문에 대해 제공된 Context를 기반으로 금융 분석을 수행하세요.\n\n"
        f"[분석 관점]\n"
        f"{config['analysis_focus']}\n\n"
        f"[질문]\n"
        f"{query}\n\n"
        f"[Context]\n"
        f"{context}\n\n"
        f"위 Context만을 근거로 {config['analysis_focus']}하여 "
        f"상승 요인, 하락 요인, 리스크, 요약을 JSON 형식으로 응답하세요."
    )

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]

    logger.info(
        "build_character_prompt  persona='%s'  query='%s'  context_len=%d",
        persona_name, query[:30], len(context),
    )
    return messages
