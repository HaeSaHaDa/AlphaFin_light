# TASK-028 실행 Prompt

## 요청 요약

Dashboard Query Flow를 `latest` 기반에서 `query → trace_id` 기반으로 수정.

## 수행 방향

1. 백엔드: `POST /api/engine/run` + memory/stock_chain `/{trace_id}` GET 엔드포인트 추가
2. 프론트: `runEngine()` API 함수 + `runAndLoad()` 훅 + QueryInputPanel Run Engine 버튼

## 핵심 제약

- 기존 `/latest` API는 그대로 유지 (Latest Trace 버튼용)
- multi-user, WebSocket, streaming 금지
- 과도한 추상화 금지
