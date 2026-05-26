# TASK-011 Prompt 001

## 작업

TASK-011-build-financial-analysis-flow 초기 구현

## 수행 내용

- TASK-010 완료 처리 및 tasks/done/ 이동
- prompts/TASK-011/, logs/TASK-011/ 생성
- src/rag/analysis/ 디렉토리 구조 생성
- prompts.py 구현 (system prompt, 분석 Prompt 생성)
- analyzer.py 구현 (Retrieval → Context → Prompt → Chat API → 결과)
- run_sample.py 구현 (Prompt 검증 + 전체 분석 Flow 검증)
- 삼성전자 Query 기준 금융 분석 검증

## 환경

- openai 2.38.0
- gpt-4o-mini (Chat API)
- text-embedding-3-small (Embedding)
- MariaDB finance_study
- pymysql

## 샘플 Query

- 삼성전자 반도체 전망 분석

## 분석 제한 원칙

- 투자 추천 금지
- 매수/매도 판단 금지
- 확정적 예측 금지
- 금융 자문 형태 금지
- 정보 기반 분석 보조 수준 유지
