# TASK-004 Prompt-001

날짜: 2026-05-25
실행 대상: Cursor

---

# 목적

```text
네이버 뉴스 검색 기반 뉴스 수집기 초기 구조 구현
```

---

# 프롬프트

```text
AGENTS.md와 TASK-004 기준으로 작업해라.

현재 작업:

1. TASK-003-build-opendart-collector 완료 처리
2. TASK-004-build-news-collector 초기 구현

수행 내용:

- TASK-003 완료 조건 검토 및 tasks/done/ 이동
- prompts/TASK-004/ 생성
- logs/TASK-004/ 생성
- src/collectors/news/ 생성
- collector.py 생성
- run_sample.py 생성
- 네이버 뉴스 검색 기반 수집 구현
- 뉴스 URL 추출 구현
- 기사 본문 수집 구현
- JSON 저장 구현
- data/raw/news/ 저장 구조 사용
- 삼성전자 기준 샘플 실행 검증

구현 범위: 단일 키워드, 단일 페이지, JSON 저장, Raw Data 저장
샘플 기준: keyword=삼성전자, max_pages=1
수집 대상: 제목, 본문, 날짜, 언론사, URL

제외 범위: DB, Selenium, Playwright, 비동기, 병렬,
대량 크롤링, Chunking, Embedding, RAG, LLM
```

---

# 결과

```text
- TASK-003 → tasks/done/ 이동 완료 (DONE 상태)
- prompts/TASK-004/, logs/TASK-004/ 생성 완료
- src/collectors/news/ 생성 완료 (__init__.py, collector.py, run_sample.py)
- data/raw/news/ 생성 완료
- 네이버 뉴스 HTML 구조 변경 대응 (SDS 컴포넌트 기반)
- run_sample.py 실행 성공 (exit code 0)
- 삼성전자 뉴스 5건 수집 완료
- 제목 5/5, 본문 5/5, 날짜 5/5, URL 5/5 수집 성공
- JSON 저장 완료: data/raw/news/samsung_news_sample.json
```
