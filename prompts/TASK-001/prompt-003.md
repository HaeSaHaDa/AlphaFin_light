# TASK-001 Prompt-003

날짜: 2026-05-25
실행 대상: Cursor

---

# 목적

```text
markdown 코드블럭 미종료 문제 수정
```

---

# 프롬프트

```text
AGENTS.md와 TASK-001 기준으로 작업해라.

현재 작업:
TASK-001 markdown fence 수정

목표:
markdown 코드블럭 미종료 문제만 수정한다.

수정 대상:

README.md
project/alphafin-lte-scope.md
project/project-overview.md
project/roadmap.md

수행 내용:

- 미종료 markdown fence 수정
- ``` 개수 불일치 수정
- markdown 구조 검증

제외 범위:

- 문서 내용 재작성 금지
- 구조 변경 금지
- 문장 수정 금지
- 파일 이동 금지
- TASK-002 생성 금지

완료 기준:

- 모든 markdown fence 정상 종료
- markdown preview 정상 동작
- 수정 결과를 logs/TASK-001/result-003.md 기록
- Prompt를 prompts/TASK-001/prompt-003.md 저장
```

---

# 결과

```text
- README.md: 닫는 fence 추가 → OK
- project/alphafin-lte-scope.md: 닫는 fence 추가 → OK
- project/project-overview.md: 닫는 fence 추가 → OK
- project/roadmap.md: 닫는 fence 추가 → OK
- 전체 fence 검증: PASS (4개 파일 모두 짝수 fence)
- 문서 내용·구조·문장 변경 없음
- logs/TASK-001/result-003.md 기록 완료
```
