# TASK-050 prompt-001

## 날짜

```text
2026-06-10
```

## 실행 주체

```text
Codex
```

## 목적

OpenDART 공시 제목만 저장하던 흐름을 보완하여 실제 공시 본문을 수집하고,
정리된 section chunk를 기존 Disclosure Retrieval과 Runtime에 연결한다.

## 수행 범위

- OpenDART `document.xml` 원문 ZIP 수집
- XML/HTML의 script, style, 불필요한 tag 제거
- 본문 문단과 표 내용 추출
- 기존 `disclosure_documents.raw_text`에 본문 저장
- section 단위 disclosure chunk 생성 및 갱신
- 기존 Disclosure Retrieval과 Runtime 연동 검증
- 실제 공시 한 건 이상 수집 검증

## 제한 사항

- 신규 AI 모델 추가 금지
- Backtesting 금지
- Auto Trading 금지
- 대규모 Schema 변경 금지
- 기존 News Retrieval 제거 금지
- 대규모 Refactoring 금지

## 결과 위치

```text
logs/TASK-050/result-001.md
```
