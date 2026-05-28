# TASK-038 Prompt 001

## 목표

selectedTicker 중심 Market Graph의 relation semantics, direction, confidence, evidence 품질을 개선한다.

## 수행

- Reasoning 모듈(`dashboard-ui/src/reasoning/*`) 초기 구축
- Relation 타입 확장: `SUPPLIES`, `COMPETES_WITH`, `DEPENDS_ON`, `AFFECTED_BY`, `BENEFITS_FROM`, `EXPOSED_TO`, `RELATED_TO`
- confidence/direction/impact/evidence 필드 추가
- API 확장: `/api/market-insight/{traceId}`, `/api/relation-explanation/{traceId}`, `/api/risk-exposure/{traceId}`
- Market Intelligence 컴포넌트(`dashboard-ui/src/components/market-intelligence/*`) 추가
- Runtime Market Graph 패널에 insight/리스크/설명 카드 연결

## 검증

- selectedTicker 중심 유지
- weak relation pruning 동작
- relation explanation/evidence 노출
- 매크로(금리/환율/유가/IRA/중국) 키워드 기반 관계 생성
