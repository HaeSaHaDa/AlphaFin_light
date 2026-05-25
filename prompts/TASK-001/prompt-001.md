# TASK-001 Prompt-001

날짜: 2026-05-25
실행 대상: Cursor

---

# 목적

```text
TASK-001 기준 디렉토리 구조 점검 및 누락 보완
```

---

# 프롬프트

```text
AGENTS.md와 현재 프로젝트 문서를 기준으로 작업해라.

현재 작업:
TASK-001-create-project-structure

목표:
AlphaFin LTE 프로젝트의 기본 디렉토리 구조와 문서 구조를 점검하고,
현재 하네스 규칙에 맞게 누락된 구조를 보완한다.

작업 대상:

TASK-001-create-project-structure.md

수행 내용:

- 현재 디렉토리 구조 점검
- TASK-001 문서와 실제 디렉토리 구조 불일치 확인
- 누락된 디렉토리 생성
- prompts/TASK-001/ 생성
- logs/TASK-001/ 생성
- docs/data/data-sources.md 위치 확인
- 루트에 불필요한 임시 md 파일이 있으면 이동 후보만 제안하고 직접 이동하지 않음
- TASK-001 상태가 DONE 가능한지 검토

제외 범위:

- TASK-002 생성 금지
- pykrx collector 구현 금지
- DB 구현 금지
- RAG 구현 금지
- LLM 연동 금지
- 기존 문서 대규모 재작성 금지

완료 기준:

- TASK-001 기준 필수 디렉토리 존재 확인
- prompts/TASK-001/ 존재 확인
- logs/TASK-001/ 존재 확인
- 점검 결과를 logs/TASK-001/result-001.md에 기록
- 실행한 Prompt를 prompts/TASK-001/prompt-001.md에 저장
```

---

# 결과

```text
- TASK-001 정의 필수 디렉토리 30개 전체 존재 확인
- 누락 디렉토리 11개 생성 (docs/project, docs/pipeline, docs/rag, docs/evaluation, docs/setup, src/* 6개)
- prompts/TASK-001/ 존재 확인 (이미 존재)
- logs/TASK-001/ 존재 확인 (이미 존재)
- docs/data/data-sources.md 미존재 확인 (후속 작업 필요)
- 루트 project/ 파일 이동 후보 제안 (직접 이동하지 않음)
- README.md 외 3개 파일 fence 미종료 확인 (기존 파일, 후속 수정 필요)
- TASK-001 DONE 가능 판단: 디렉토리 구조 충족, 문서 이관은 후속 분리 권장
- 결과를 logs/TASK-001/result-001.md에 기록 완료
```
