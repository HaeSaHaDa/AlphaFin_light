"""한국 주요 종목 레지스트리 (KRX + OpenDART corp_code)."""
from __future__ import annotations

from typing import TypedDict


class CompanyRecord(TypedDict):
    company_name: str
    ticker: str
    corp_code: str
    market: str
    aliases: list[str]


COMPANY_REGISTRY: list[CompanyRecord] = [
    {
        "company_name": "삼성전자",
        "ticker": "005930",
        "corp_code": "00126380",
        "market": "KOSPI",
        "aliases": ["삼성", "samsung", "삼성전자주식회사"],
    },
    {
        "company_name": "현대자동차",
        "ticker": "005380",
        "corp_code": "00164742",
        "market": "KOSPI",
        "aliases": ["현대차", "hyundai", "현대 자동차"],
    },
    {
        "company_name": "SK하이닉스",
        "ticker": "000660",
        "corp_code": "00181751",
        "market": "KOSPI",
        "aliases": ["하이닉스", "sk하이닉스", "sk hynix"],
    },
    {
        "company_name": "LG에너지솔루션",
        "ticker": "373220",
        "corp_code": "01515323",
        "market": "KOSPI",
        "aliases": ["lg에너지", "lg energy", "엔솔"],
    },
    {
        "company_name": "NAVER",
        "ticker": "035420",
        "corp_code": "00266961",
        "market": "KOSPI",
        "aliases": ["네이버", "naver"],
    },
    {
        "company_name": "카카오",
        "ticker": "035720",
        "corp_code": "00258801",
        "market": "KOSPI",
        "aliases": ["kakao"],
    },
]
