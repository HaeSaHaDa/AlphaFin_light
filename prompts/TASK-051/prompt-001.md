# TASK-051 prompt-001

## 날짜

```text
2026-06-10
```

## 실행 주체

```text
Codex
```

## 목적

Runtime Retrieval을 관련성 중심 검색에서 관련성과 최신성을 함께 반영하는
Freshness-aware Retrieval로 개선한다.

## 수행 범위

- 뉴스 cache 12시간 TTL 적용
- 공시 cache 12시간 TTL 적용
- stale cache의 Runtime 실행 전 자동 재수집
- 뉴스 90일 날짜 필터 적용
- 뉴스와 공시 최신성 점수 적용
- Runtime Context에 기준 시각, 수집 시각, cache 상태 저장
- Dashboard에 뉴스와 공시 freshness 상태 표시
- OpenAI key, embedding, chat 호출 재검증
- Runtime timeout과 module import 안정성 확인

## 제한 사항

- 신규 AI 모델 추가 금지
- Schema 변경 금지
- Backtesting 및 Auto Trading 추가 금지
- 기존 News Retrieval 제거 금지
- 대규모 Refactoring 금지

## 결과 위치

```text
logs/TASK-051/result-001.md
```
