# TASK-032-build-cost-guard-cache-and-dashboard-stabilization.md

# TASK-032 Cost Guard / Embedding Cache / Dashboard Stabilization 구축

## 상태

DONE

---

# 목표

현재 Financial AI Engine의:

```text
OpenAI API 비용 증가 위험
Embedding 중복 생성
Dashboard UI 깨짐
Tailwind 스타일 누락
모바일/발표 화면 불안정
```

문제를 해결하기 위한:

```text
Cost Guard
Embedding Cache
Dashboard Stabilization
```

시스템을 구축한다.

현재 TASK의 목표는
단순 기능 추가가 아니라:

```text
발표 가능한 안정성 확보
실제 사용 가능한 수준의 UX 안정화
OpenAI 비용 폭증 방지
```

이다.

---

# 배경

현재 프로젝트는 다음 흐름까지 구축 완료되었다.

```text
수집
→ 저장
→ Chunking
→ Embedding
→ Semantic Retrieval
→ Financial Analysis
→ Reflection
→ Layered Memory
→ Temporal Market Memory
→ Stock Chain
→ Signal Evaluation
→ Explainable Dashboard
→ Company Resolver
→ Dynamic Ingestion Pipeline
```

현재 시스템은:

```text
회사명 입력
→ ticker 자동 식별
→ ingestion
→ embedding
→ retrieval
→ AI 분석
```

까지 가능하다.

하지만 현재 구조는:

```text
embedding 중복 생성 가능성
OpenAI API 비용 증가 가능성
Dashboard CSS/레이아웃 불안정
Tailwind 적용 누락
UI 깨짐
```

문제가 존재한다.

현재 TASK에서는:

```text
비용 안정성
+
Dashboard 안정성
```

을 동시에 개선한다.

---

# 범위

현재 TASK에서 포함하는 작업:

- Embedding Cache 구축
- 중복 Embedding 생성 방지
- Ingestion Cache 구축
- Vector Index 재사용 구조 구축
- OpenAI Token Usage Logging 구축
- 예상 비용 계산 구축
- Daily Budget Guard 구축
- DRY_RUN Mode 구축
- Presentation Cache Mode 구축
- 최대 뉴스 수 제한 구축
- 최대 Chunk 수 제한 구축
- Dashboard CSS 안정화
- Tailwind 적용 문제 수정
- Dashboard Grid/Layout 안정화
- 반응형 Layout 수정
- 발표 화면 UX 안정화
- Typography 개선
- Card Layout 정리
- Dark Theme 안정화
- Button/Input 스타일 안정화
- 결과 로그 기록

---

# 현재 제외 범위

현재 TASK에서 제외:

- 신규 AI 모델 추가
- 신규 Retrieval 구조 추가
- 신규 Memory 구조 추가
- 신규 Reflection 구조 추가
- Real-time Streaming
- Broker API
- Auto Trading
- HTS UI
- 실시간 전체 시장 ingestion
- 분산 MLOps
- Kubernetes
- Multi-user SaaS
- 복잡한 Auth 시스템

현재 TASK는:

```text
안정성 + 비용 제어
```

만 수행한다.

---

# 현재 문제

현재 Dashboard 상태:

```text
- 스타일 깨짐
- Tailwind 일부 미적용
- Grid 레이아웃 불안정
- spacing 불균형
- 발표 화면 readability 부족
```

현재 ingestion 상태:

```text
같은 종목 재실행 시
embedding 재생성 가능성 존재
```

---

# 생성 대상 구조

```text
src/cost_guard/
├─ token_usage_logger.py
├─ cost_estimator.py
├─ budget_guard.py
├─ embedding_cache_manager.py
├─ ingestion_cache_manager.py
└─ presentation_mode.py
```

```text
dashboard-ui/src/
├─ styles/
│  ├─ dashboard.css
│  ├─ report-layout.css
│  └─ typography.css
```

---

# Cost Guard 역할

현재 역할:

- OpenAI API 비용 제어
- token usage 추적
- embedding 중복 방지
- 발표용 cache mode 지원

---

# Embedding Cache 목표

현재 목표:

```text
동일 chunk 재임베딩 금지
```

예상 흐름:

```text
chunk hash 확인
↓

이미 embedding 존재

↓

재사용
```

---

# Ingestion Cache 목표

현재 목표:

```text
이미 ingestion 완료된 종목
재수집 최소화
```

예상 흐름:

```text
현대자동차 ingestion 존재
↓

cache hit
↓

기존 vector index 재사용
```

---

# Daily Budget Guard 목표

현재 목표:

```text
일일 OpenAI 비용 제한
```

예상 설정:

```python
MAX_DAILY_COST_USD = 5
```

---

# DRY_RUN 목표

현재 목표:

```text
실제 embedding 생성 없이
pipeline 검증
```

예상 사용:

```bash
python ingestion_runner.py --dry-run
```

---

# Presentation Mode 목표

현재 목표:

```text
발표 시 cache 기반 실행
```

예상 동작:

```text
새 embedding 생성 금지
↓

기존 trace/cache 사용
```

---

# UI Stabilization 목표

현재 목표:

```text
발표 가능한 Dashboard 완성
```

---

# 현재 UI 문제 해결 목표

현재 이미지 기준 문제:

```text
- 기본 HTML처럼 보임
- Tailwind 미적용 의심
- spacing 불균형
- typography 부족
- card layout 미적용
```

---

# 수정 목표

현재 수정 방향:

```text
개발용 화면
↓

제품 수준 Dashboard
```

---

# Dashboard Layout 목표

```text
┌────────────────────────────────┐
│ Header                         │
├────────────────────────────────┤
│ AI 시장 분석 리포트            │
├──────────────┬─────────────────┤
│ 상승 요인    │ 리스크          │
├────────────────────────────────┤
│ 시장 연결 구조                 │
├────────────────────────────────┤
│ AI 분석 과정                   │
└────────────────────────────────┘
```

---

# Typography 목표

현재 목표:

- 큰 제목
- 카드 제목 hierarchy
- spacing consistency
- 발표 readability 강화

---

# Tailwind 목표

현재 목표:

- Tailwind 정상 적용
- dark theme 안정화
- responsive grid 정상화
- button/input styling 적용

---

# 한국어 UX 목표

현재 목표:

```text
개발자 로그 느낌 제거
```

↓

```text
AI 금융 분석 리포트 느낌 강화
```

---

# API 연동 대상

현재 API 연동 대상:

```text
POST /api/ingestion/run
POST /api/engine/run
GET /api/signal/{trace_id}
GET /api/evaluation/{trace_id}
```

---

# 구현 규칙

현재 TASK는 다음 원칙을 따른다.

- 기존 Engine 구조 재사용
- 기존 Dashboard API 재사용
- 기존 Event Graph 유지
- 기존 Memory Timeline 유지
- 기존 Signal Evaluation 유지
- OpenAI 호출 최소화
- embedding 재사용 우선
- 발표용 readability 우선
- Tailwind 기반 유지
- 작은 component 유지
- 과도한 abstraction 금지

---

# 예상 기능

## embedding_cache_manager.py

역할:

- embedding cache 관리

예상 기능:

```text
check_embedding_exists()
reuse_embedding()
save_embedding_cache()
```

---

## token_usage_logger.py

역할:

- token usage 기록

예상 기능:

```text
log_openai_usage()
calculate_token_usage()
```

---

## budget_guard.py

역할:

- 비용 제한

예상 기능:

```text
check_daily_budget()
block_expensive_request()
```

---

## presentation_mode.py

역할:

- 발표 모드 관리

예상 기능:

```text
enable_cache_only_mode()
disable_new_embedding()
```

---

# UI 수정 목표

## Header 개선

현재 목표:

- title spacing 개선
- typography 강화
- subtitle hierarchy 추가

---

## Card Layout 개선

현재 목표:

- rounded card
- shadow 적용
- padding consistency
- responsive grid

---

## Button/Input 개선

현재 목표:

- Tailwind button 적용
- hover state 추가
- spacing 개선

---

# Visualization 활용 목표

현재 활용 목표:

```text
- 발표 가능한 안정적 Dashboard
- OpenAI 비용 안정화
- Embedding 중복 방지
- 발표용 cache 실행
- 실제 사용 가능한 UX 확보
```

---

# 검증 항목

현재 TASK 완료 전
다음 항목을 반드시 검증한다.

## Cache 검증

- embedding cache 동작 여부
- ingestion cache 동작 여부
- duplicate embedding 방지 여부

---

## Cost 검증

- token usage logging 여부
- 예상 비용 계산 여부
- daily budget guard 동작 여부

---

## DRY_RUN 검증

- dry-run 동작 여부
- embedding skip 여부

---

## Presentation Mode 검증

- cache only mode 동작 여부
- 새 embedding 차단 여부

---

## UI 검증

- Tailwind 정상 적용 여부
- layout 정상 여부
- typography 정상 여부
- responsive 정상 여부
- dashboard readability 여부

---

## 구조 검증

- 기존 Engine 구조 유지 여부
- 기존 Event Graph 유지 여부
- TASK 범위 외 수정 여부 확인

---

# 관련 Prompt

```text
prompts/TASK-032/
```

---

# 관련 Logs

```text
logs/TASK-032/
```

---

# 완료 조건

다음 조건 충족 시 완료 가능.

- Embedding Cache 구축 성공
- Cost Guard 구축 성공
- Daily Budget Guard 구축 성공
- DRY_RUN 구축 성공
- Presentation Cache Mode 구축 성공
- Dashboard UI 안정화 성공
- Tailwind 정상 적용 성공
- 발표 가능한 Dashboard 확보 성공
- OpenAI 비용 안정화 성공
- 결과 로그 작성 완료
- TASK 범위 외 구현 없음

---

# 완료 후 다음 TASK 후보

현재 TASK 완료 후
다음 작업 후보:

- TASK-033-build-portfolio-backtesting-suite
- TASK-034-build-backtesting-visualization
- TASK-035-build-presentation-demo-scenario

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- Explainable AI 유지
- End-to-End traceability 유지
- 발표 가능한 UX 유지
- OpenAI 비용 안정성 유지
- Embedding 재사용 우선
- AI 협업 가능한 구조 유지
- 과도한 Autonomous AI 구조 금지
