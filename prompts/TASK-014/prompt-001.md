# TASK-014 Prompt 001

## 작업

TASK-014-build-character-layer 초기 구현

## 수행 내용

- TASK-013 완료 처리 및 tasks/done/ 이동
- prompts/TASK-014/, logs/TASK-014/ 생성
- src/rag/character/ 디렉토리 구조 생성
- personas.py 구현 (4개 Persona 정의, 로드, 목록)
- prompt_builder.py 구현 (Persona 기반 system/user Prompt 생성)
- analyzer.py 구현 (Character별 분석, 전체 실행, 비교, JSON 저장)
- run_sample.py 구현 (4 Persona 통합 검증)
- 삼성전자 Query 기준 Persona별 분석 검증

## 환경

- openai (gpt-4o-mini Chat API)
- text-embedding-3-small (Embedding)
- MariaDB finance_study

## Persona

- growth_investor
- value_investor
- risk_averse_analyst
- aggressive_trader

## 샘플 Query

- 삼성전자 반도체 전망 분석
