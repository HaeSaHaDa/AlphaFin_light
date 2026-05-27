# TASK-026 Prompt-001

## 작업

TASK-026-build-retrieval-analysis-viewer

## 목표

Retrieval · Analysis · Reflection 흐름의 explainability 강화 Viewer 구축

## 수행 내용

- TASK-025 완료 확인
- `/analysis` 페이지 및 7개 Viewer 컴포넌트 구현
- trace_id 기반 API 연동 (retrieval, reflection, trace, evaluation)
- retrieval API explainability 필드 보강 (rank, source_file, analysis, context_layers)
- collapsible UI · similarity progress bar · Recharts metadata chart

## 환경

- dashboard-ui (Next.js 15)
- Backend API http://localhost:8000

## 접속

- Overview: http://localhost:3000
- Analysis: http://localhost:3000/analysis

## 샘플 검증

- trace_id: 20260527_123745
- Query: 삼성전자 반도체 전망 분석 (HBM / AI 서버 맥락)

## 제외 범위

- LLM streaming · CoT 완전 노출 · Prompt editing 금지
