"""금융 분석용 Prompt 생성 모듈."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """당신은 한국 주식 시장 전문 금융 분석 보조입니다.

역할:
- 제공된 뉴스와 공시 데이터를 근거로 분석합니다.
- 상승 요인, 하락 요인, 리스크를 구분하여 정리합니다.
- 반드시 제공된 Context에 기반하여 답변합니다.

제한:
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
}
"""


def build_analysis_prompt(query: str, context: str) -> list[dict]:
    """금융 분석 Prompt 메시지 목록을 생성한다.

    Args:
        query: 사용자 분석 질문.
        context: RAG Context 문자열 (assembler의 prompt_context).

    Returns:
        OpenAI Chat API messages 형식의 dict 목록.
    """
    user_content = f"""다음 질문에 대해 제공된 Context를 기반으로 금융 분석을 수행하세요.

[질문]
{query}

[Context]
{context}

위 Context만을 근거로 상승 요인, 하락 요인, 리스크, 요약을 JSON 형식으로 응답하세요."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    logger.info(
        "build_analysis_prompt  query='%s'  context_len=%d",
        query[:30], len(context),
    )
    return messages
