# TASK-004-build-news-collector.md

# TASK-004 뉴스 수집기 초기 구축

## 상태

TODO

---

# 목표

뉴스 기반 시장 정보 수집기의
초기 구조를 구축한다.

현재 TASK의 목표는
단일 키워드 기준 뉴스 데이터를 수집하고
Raw Data로 저장하는 최소 Collector를 만드는 것이다.

현재 단계에서는
대규모 크롤링보다
기본 수집 구조 안정화에 집중한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- `src/collectors/news/` 구조 생성
- 네이버 뉴스 검색 기반 수집
- 뉴스 URL 추출
- 기사 본문 수집
- JSON 저장
- Raw Data 저장 구조 사용
- 샘플 실행 스크립트 작성
- 기본 로그 출력
- 샘플 실행 검증

---

# 현재 제외 범위

현재 TASK에서 제외:

- DB 저장
- MariaDB 연동
- Selenium 사용
- Playwright 사용
- 비동기 처리
- 병렬 처리
- 대량 크롤링
- Chunking
- Embedding 생성
- RAG 연결
- LLM 분석
- 뉴스 요약
- 감성 분석
- 스케줄러
- 성능 최적화

현재 TASK는
뉴스 수집기 초기 구조만 구현한다.

---

# 생성 대상 구조

```text
src/collectors/news/
├─ __init__.py
├─ collector.py
└─ run_sample.py
```

---

# 저장 대상 구조

```text
data/raw/news/
```

예상 저장 파일 예시:

```text
data/raw/news/samsung_news_202401.json
```

---

# 구현 규칙

현재 TASK는 다음 규칙을 따른다.

- 작은 함수 유지
- 단일 책임 유지
- requests 기반 구현
- BeautifulSoup 기반 파싱
- 하드코딩 최소화
- 예외 무시 금지
- 명확한 오류 메시지 출력
- 과도한 abstraction 금지
- Raw Data 원본 유지
- DB 저장 금지

---

# 예상 기능

## collector.py

역할:

- 뉴스 검색 요청
- 뉴스 URL 추출
- 기사 본문 수집
- JSON 데이터 생성
- JSON 저장

예상 함수:

```text
search_news(keyword, max_pages)
extract_news_links(html)
fetch_article(url)
save_news_json(data, output_path)
```

---

## run_sample.py

역할:

- 샘플 키워드 기준 실행
- 뉴스 수집
- JSON 저장 검증
- 실행 결과 출력

샘플 기준:

```text
keyword: 삼성전자
max_pages: 1
```

---

# 수집 대상 데이터

현재 단계에서는 다음 정보만 수집한다.

```text
- 제목
- 본문
- 날짜
- 언론사
- URL
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## 실행 검증

- `run_sample.py` 실행 가능 여부
- 뉴스 검색 성공 여부
- 기사 본문 수집 성공 여부
- JSON 저장 성공 여부

---

## 데이터 검증

- 뉴스 데이터 존재 여부
- 제목 존재 여부
- 본문 존재 여부
- 날짜 존재 여부
- URL 존재 여부
- JSON 비어 있지 않은지 확인

---

## 구조 검증

- `src/collectors/news/` 구조 정상 여부
- `data/raw/news/` 저장 여부
- TASK 범위 외 파일 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-004/
```

---

# 관련 Logs

```text
logs/TASK-004/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- 뉴스 collector 초기 구조 생성 완료
- 뉴스 검색 성공
- 기사 본문 수집 성공
- JSON 저장 성공
- 샘플 실행 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-005-design-mariadb-schema
- TASK-006-build-chunking-pipeline
- TASK-007-build-embedding-pipeline

단,
Chunking 및 RAG 연결은
현재 TASK에서 구현하지 않는다.

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- 작은 TASK 기반 개발
- Raw Data 우선 저장
- 검증 가능한 샘플 우선
- 단일 기능 우선 구현
- AI 협업 가능한 구조 유지
- 재현 가능한 실험 구조 유지
- 과도한 크롤링 금지