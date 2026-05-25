"""OpenDART 기반 단일 기업 공시 목록 수집기."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

OPENDART_LIST_URL = "https://opendart.fss.or.kr/api/list.json"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[3] / "data" / "raw" / "dart"
REQUEST_TIMEOUT_SEC = 30


def load_api_key() -> str:
    """DART_API_KEY를 .env에서 로드한다.

    Returns:
        API 키 문자열.

    Raises:
        ValueError: 키가 설정되지 않았을 때.
    """
    env_path = Path(__file__).resolve().parents[3] / ".env"
    load_dotenv(env_path)

    key = os.getenv("DART_API_KEY", "").strip()
    if not key:
        raise ValueError("DART_API_KEY가 .env에 설정되지 않았습니다.")

    logger.info("DART_API_KEY 로드 완료")
    return key


def fetch_disclosures(
    corp_code: str,
    begin_date: str,
    end_date: str,
    api_key: str | None = None,
    page_count: int = 100,
) -> dict:
    """단일 기업의 공시 목록을 조회한다.

    Args:
        corp_code: DART 기업 고유번호 (예: "00126380")
        begin_date: 시작일 (예: "20240101")
        end_date: 종료일 (예: "20240131")
        api_key: DART API 키. None이면 .env에서 로드.
        page_count: 페이지당 건수 (최대 100).

    Returns:
        OpenDART API 응답 dict.
    """
    if api_key is None:
        api_key = load_api_key()

    params = {
        "crtfc_key": api_key,
        "corp_code": corp_code,
        "bgn_de": begin_date,
        "end_de": end_date,
        "page_count": page_count,
    }

    logger.info(
        "fetch_disclosures  corp_code=%s  %s ~ %s",
        corp_code, begin_date, end_date,
    )

    try:
        resp = requests.get(
            OPENDART_LIST_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SEC,
        )
        resp.raise_for_status()
    except requests.RequestException:
        logger.exception("OpenDART API 요청 실패  corp_code=%s", corp_code)
        return {}

    data = resp.json()
    status = data.get("status", "")

    if status != "000":
        msg = data.get("message", "알 수 없는 오류")
        logger.warning("OpenDART 응답 오류  status=%s  message=%s", status, msg)
        return data

    total = data.get("total_count", 0)
    logger.info("공시 목록 수집 완료  corp_code=%s  total_count=%s", corp_code, total)
    return data


def save_disclosures_json(
    data: dict,
    output_path: Path | str | None = None,
    filename: str = "disclosures.json",
) -> Path | None:
    """공시 목록 데이터를 JSON으로 저장한다.

    Args:
        data: OpenDART API 응답 dict.
        output_path: 저장 디렉토리. None이면 data/raw/dart/ 사용.
        filename: 저장 파일명.

    Returns:
        저장된 파일 경로. 빈 데이터면 None.
    """
    if not data or not data.get("list"):
        logger.warning("저장 생략 (공시 데이터 없음)")
        return None

    out_dir = Path(output_path) if output_path else DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    filepath = out_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    count = len(data.get("list", []))
    logger.info("JSON 저장 완료  %s  공시 %d건", filepath, count)
    return filepath
