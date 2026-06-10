# TASK-050 OpenDART 공시 본문 수집 결과

## 수행 요약

- OpenDART `document.xml` 원문 ZIP 수집기를 추가했다.
- XML/HTML에서 `script`, `style`을 제거하고 제목, 문단, 표 행을 추출했다.
- 기존 `disclosure_documents.raw_text`를 공시 본문 저장 필드로 사용했다.
- 기존 `report_name`과 문서 메타데이터는 유지했다.
- section marker와 표 행을 보존한 disclosure chunk를 생성했다.
- 변경된 문서의 chunk와 embedding만 동기화하도록 수정했다.
- 기존 제목-only cache를 식별하기 위한 body cache version을 추가했다.
- Runtime 뉴스 retrieval을 `news_article`로 제한하고 공시 본문과 분리 병합했다.
- 공시 결과의 `text`와 Unified Engine의 `chunk_text` 계약을 일치시켰다.

## 수집된 공시 본문 예시

수집 대상:

```text
기업: 삼성전자
ticker: 005930
report_name: 최대주주등소유주식변동신고서
receipt_no: 20260608800918
본문 길이: 6,190자
```

본문 근거 예시:

```text
보통주식총수 | 종류주식총수 | 발행주식총수
5,846,278,608 | 802,371,203 | 6,648,649,811

직전보고서 합계: 1,152,182,230
이번보고서 합계: 1,152,149,501
증감 합계: -32,729
```

## 생성된 chunk 수

```text
본문 수집 문서: 1건
해당 문서 본문 chunk: 19건
005930 전체 disclosure document: 113건
005930 전체 disclosure chunk: 119건
005930 전체 disclosure embedding: 119건
신규 생성 embedding: 19건
```

## Retrieval 개선 내용

- 기존 제목-only chunk 대신 최대 976자의 실제 공시 본문 chunk를 검색한다.
- `005930 장내매도` 검색 결과:

```text
top score: 0.9872
검색 결과: 5건
표 행과 주식 수치 포함
```

- Disclosure API:

```text
GET /api/disclosure/search
본문 chunk 반환 확인
```

- Unified Context:

```text
context 길이: 5,244자
발행주식총수 수치 포함: 확인
장내매도 표 행 포함: 확인
```

## Runtime 영향

검증 Runtime:

```text
trace_id: 20260610_090351
ticker: 005930
news chunks: 6
disclosure body chunks: 5
```

최종 source 분리:

```text
NEWS: 6
DISCLOSURE: 5
OTHER: 0
```

공시 본문은 `chunk_text`로 Unified Engine에 전달된다. 기존 News Retrieval은
`news_article`만 조회하며 제거하거나 대체하지 않았다.

## 검증 결과

- 실제 OpenDART ZIP 응답 확인: 성공
- HTML/XML 정리: 성공
- script/style 제거: 성공
- 표 행 보존: 성공
- MariaDB 본문 저장: 성공
- section chunk 생성: 성공
- embedding 생성: 성공
- Disclosure API 검색: 성공
- Runtime Context 연결: 성공
- Python `compileall`: 성공
- Frontend ESLint: 성공
- TypeScript `tsc --noEmit`: 성공
- Backend health: 정상

## 발견한 위험 요소

- OpenDART 공시 형식마다 XML tag 구조가 달라 일부 복잡한 XBRL 문서는 section 품질이 다를 수 있다.
- Runtime 자동 수집은 응답 시간과 비용을 제한하기 위해 최신 본문 1건을 우선 수집한다.
- 명시적 Disclosure Collect API는 `body_limit`으로 최대 100건까지 조정할 수 있다.
- 공시에는 공개된 개인 식별 정보가 포함될 수 있으므로 Dashboard 노출 범위를 주의해야 한다.
- `run_with_timeout`은 executor 종료를 기다리는 구조라 실제 wall-clock timeout 보장이 약하다.
- `runtime_flow.__init__`의 기존 순환 import 문제는 이번 TASK 범위 밖으로 유지했다.

## Schema

신규 테이블이나 컬럼을 추가하지 않았다.

```text
disclosure_documents.raw_text
```

기존 `LONGTEXT` 필드를 공시 본문 저장에 재사용했다.
