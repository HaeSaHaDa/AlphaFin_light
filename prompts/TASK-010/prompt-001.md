# TASK-010 Prompt 001

## 작업

TASK-010-build-rag-context-assembly 초기 구현

## 수행 내용

- TASK-009 완료 처리 및 tasks/done/ 이동
- prompts/TASK-010/, logs/TASK-010/ 생성
- src/rag/context/ 디렉토리 구조 생성
- formatter.py 구현 (뉴스/공시 Context 포맷, Prompt Context 생성)
- assembler.py 구현 (그룹화, 길이 제한, Context 조립, JSON 저장)
- run_sample.py 구현 (4단계 검증)
- 삼성전자 Query 기준 Context 생성 검증

## 환경

- openai 2.38.0
- text-embedding-3-small
- MariaDB finance_study
- pymysql

## 샘플 Query

- 삼성전자 반도체 실적 전망
- HBM 시장 성장
- AI 메모리 수요 증가
