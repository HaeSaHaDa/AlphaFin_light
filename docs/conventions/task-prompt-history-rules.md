# TASK Prompt 기록 규칙

## 목적

이 문서는
TASK 진행 시 사용하는 프롬프트 기록 규칙을 정의한다.

목표는 다음과 같다.

- AI 작업 히스토리 보존
- 프롬프트 유실 방지
- 세션 복구 가능성 확보
- 작업 재현 가능성 확보
- Cursor / Codex 작업 추적 가능성 확보

---

# 기본 원칙

현재 프로젝트는
프롬프트를 TASK 기준으로 분리 관리한다.

구조:

```text
tasks/
→ 작업 정의

prompts/
→ 실제 실행 Prompt 기록

logs/
→ 실행 결과 및 이슈 기록
```

예시:

```text
tasks/todo/TASK-001-create-project-structure.md

prompts/TASK-001/prompt-001.md

logs/TASK-001/result-001.md
```

---

# 프롬프트 기록 위치

프롬프트는
prompts/TASK-XXX/ 구조에 저장한다.

예시:

```text
prompts/TASK-001/prompt-001.md
```

TASK 문서는
작업 정의와 상태 관리만 담당한다.

---

# TASK 문서 권장 구조

```text
1. 목표
2. 범위
3. 제외 범위
4. 검증 기준
5. 관련 Prompt
6. 관련 Logs
7. 현재 상태
```

---

# 실행 프롬프트 기록 구조

권장 구조:

```text
# 실행 프롬프트 기록

## Prompt-001
## Prompt-002
## Prompt-003
```

---

# Prompt 기록 예시

## Prompt-001

날짜:

```text
2026-05-24
```

실행 대상:

```text
Cursor
```

목적:

```text
프로젝트 기본 디렉토리 구조 생성
```

프롬프트:

```text
현재 프로젝트 구조 문서를 기반으로
다음 디렉토리 구조를 생성해라.

- docs/
- tasks/
- logs/
- data/
- src/
```

결과:

```text
- 디렉토리 생성 완료
- md 파일 생성 완료
```

---

# 결과 기록 규칙

각 Prompt 실행 후
반드시 결과를 기록한다.

예시:

```text
결과:
- 생성 성공
- markdown 오류 발생
- 구조 수정 필요
```

---

# 이슈 기록 규칙

오류 또는 문제 발생 시
TASK 내부에 기록한다.

예시:

```text
이슈:
- markdown 코드블럭 미종료
- directory depth 오류
- Cursor 구조 오인식
```

---

# 현재 원칙

현재 프로젝트는 다음 원칙을 유지한다.

- TASK 단위 프롬프트 관리
- Prompt 히스토리 유지
- 세션 복구 가능 구조 유지
- AI 작업 추적 가능 구조 유지
- 반복 가능한 작업 구조 유지

---

# 현재 금지 사항

현재 금지:

- 프롬프트 미기록
- TASK와 무관한 Prompt 저장
- 결과 없는 Prompt 기록
- 세션 의존 작업 진행
- 로그 없는 구조 변경

---

# 현재 목표

현재 목표는 다음과 같다.

```text
TASK
→ 작업 정의

prompts
→ 실행 Prompt 기록

logs
→ 결과 및 이슈 기록
```

구조를 분리 유지한다.