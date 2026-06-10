# AlphaFin LTE 하네스 엔지니어링 학습 가이드

## 문서 목적

이 문서는 AlphaFin LTE 프로젝트에 실제로 적용된 하네스를 이용해
하네스 엔지니어링(Harness Engineering)을 학습하기 위한 안내서다.

여기서 하네스는 단순한 실행 스크립트를 뜻하지 않는다. 사람과 AI가 같은 규칙을 읽고,
작업 범위를 제한하고, 실행 과정을 기록하고, 결과를 검증할 수 있게 만드는 전체 작업
환경을 뜻한다.

이 프로젝트의 하네스는 다음 관점으로 보는 것이 적절하다.

```text
AI 협업 규칙과 작업 기록 학습: 적합
TASK 단위 변경 추적 학습: 적합
문서 우선 개발 학습: 적합
자동 검증과 CI 모범 구현: 부족
프로덕션 수준 재현 환경: 부족
직접 자동화를 보강하는 실습 프로젝트: 매우 적합
```

---

# 1. 하네스 엔지니어링이란

코드 생성 능력만으로는 안정적인 소프트웨어 개발이 어렵다. 특히 AI는 현재 작업의
범위를 잊거나, 기존 설계를 충분히 읽지 않거나, 검증 없이 완료했다고 판단할 수 있다.

하네스는 이런 문제를 줄이기 위해 AI와 사람이 따라야 할 작업 환경을 만든다.

```text
규칙
-> 작업 정의
-> 실행 요청
-> 코드 변경
-> 검증
-> 결과 기록
-> 상태 전환
```

좋은 하네스는 다음 질문에 답할 수 있어야 한다.

```text
무엇을 해야 하는가
무엇을 하면 안 되는가
어떤 문서를 먼저 읽어야 하는가
이번 변경의 범위는 어디까지인가
무엇을 실행해 검증해야 하는가
실제로 무엇이 변경되었는가
실패와 위험 요소는 어디에 기록되는가
중단된 세션을 어떻게 이어서 작업하는가
```

---

# 2. AlphaFin LTE의 현재 하네스 구조

현재 프로젝트의 핵심 하네스는 다음 파일과 디렉터리로 구성된다.

```text
README.md
AGENTS.md

project/
docs/
├─ architecture/
├─ conventions/
├─ data/
├─ harness/
└─ rag/

tasks/
├─ backlog/
├─ todo/
├─ doing/
├─ review/
└─ done/

prompts/
└─ TASK-XXX/

logs/
├─ TASK-XXX/
├─ daily/
├─ issues/
├─ ai-decisions/
└─ experiments/

scripts/
src/
dashboard-ui/
```

각 영역의 책임은 다음과 같다.

| 영역 | 책임 |
|---|---|
| `README.md` | 프로젝트 목적과 첫 진입점 |
| `AGENTS.md` | AI와 사람이 지켜야 할 최상위 작업 규칙 |
| `project/` | 현재 상태, 범위, 로드맵, 용어 |
| `docs/architecture/` | 실제 시스템 구조와 실행 흐름 |
| `docs/conventions/` | TASK, Prompt, 검증 및 작업 방식 |
| `tasks/` | 해야 할 작업의 상태와 완료 조건 |
| `prompts/` | AI에게 실제로 전달한 실행 요청 |
| `logs/` | 변경 결과, 검증 결과, 이슈와 의사결정 |
| `scripts/` | 반복 검증과 운영 명령 자동화 |
| `src/`, `dashboard-ui/` | 실제 구현 |

핵심은 코드만 하네스가 아니라는 점이다. 규칙, 상태, 실행 기록, 검증 기록이 함께
존재해야 세션이 바뀌어도 작업 맥락을 복구할 수 있다.

---

# 3. 가장 중요한 TASK-Prompt-Log 연결

AlphaFin LTE 하네스의 중심은 다음 세 문서의 역할 분리다.

```text
TASK
-> 무엇을, 어디까지, 어떤 완료 조건으로 작업할지 정의

Prompt
-> 해당 TASK를 수행하기 위해 AI에게 실제 전달한 요청을 기록

Log
-> 실제 변경, 실행 결과, 검증, 실패, 남은 위험을 기록
```

예를 들어 TASK-051은 다음과 같이 연결된다.

```text
tasks/done/TASK-051-build-freshness-aware-runtime-retrieval.md
prompts/TASK-051/prompt-001.md
logs/TASK-051/result-001.md
```

## TASK가 담당하는 것

TASK-051은 최신성 기반 Retrieval이라는 목적과 다음 경계를 정의한다.

```text
포함:
- 뉴스와 공시 TTL
- 최신성 점수
- Dashboard 기준 시각
- Runtime 검증

제외:
- 신규 AI 모델
- Backtesting
- Auto Trading
- 대규모 Schema 변경
```

이처럼 제외 범위가 있으면 AI가 요청을 확장해서 unrelated change를 만드는 위험을 줄일
수 있다.

## Prompt가 담당하는 것

Prompt는 TASK 전체를 다시 쓰는 문서가 아니다. 실제 실행 시점에 선택한 세부 조건을
기록한다.

TASK-051의 Prompt에는 다음 결정이 남아 있다.

```text
뉴스 cache TTL: 12시간
공시 cache TTL: 12시간
뉴스 날짜 범위: 90일
결과 위치: logs/TASK-051/result-001.md
```

## Log가 담당하는 것

Log는 계획이 아니라 증거다.

TASK-051 결과에는 다음 실행 증거가 기록되어 있다.

```text
실제 cache 갱신 시각
freshness 계산식
trace_id
검색된 뉴스와 공시 수
OpenAI 호출 상태
compileall, ESLint, TypeScript 검증
남은 Runtime 위험 요소
```

좋은 결과 로그는 "수정 완료"에서 끝나지 않고, 어떤 명령과 데이터로 성공을 판단했는지
보여준다.

---

# 4. 현재 작업 생명주기

프로젝트 규칙을 종합하면 권장 생명주기는 다음과 같다.

```text
1. README와 AGENTS 확인
2. 현재 TASK 확인
3. 관련 architecture와 convention 확인
4. 기존 Prompt와 Log 확인
5. 관련 코드와 현재 Git 변경 확인
6. TASK 범위 안에서 구현
7. 정적 검사와 실행 검증
8. Prompt와 결과 Log 기록
9. TASK 완료 조건 확인
10. TASK 파일을 done으로 이동
11. TASK의 상태 값만 DONE으로 변경
```

TASK 파일에는 특별한 불변성 규칙이 있다.

```text
허용:
- 상태 폴더 사이의 파일 이동
- done 이동 시 ## 상태 값만 DONE으로 변경

금지:
- 작업 도중 TASK 본문 재작성
- 결과에 맞춰 완료 조건 변경
- 상태 외 본문 수정
```

이 규칙은 작업이 끝난 뒤 기준을 유리하게 바꾸는 것을 막는다. TASK는 계약이고,
Prompt와 Log가 실행 이력이 된다.

---

# 5. 현재 하네스에서 잘된 부분

## 규칙의 우선순위가 명확하다

`AGENTS.md`는 문서 읽기 순서, 작은 변경 원칙, 금지 사항, 검증 기준을 명시한다.
AI가 코드를 먼저 고치는 대신 프로젝트 맥락을 읽도록 유도한다.

## 작업 정의와 실행 기록을 분리했다

TASK 본문을 계속 수정하지 않고 Prompt와 Log를 별도로 쌓기 때문에 원래 요구사항과
실제 실행 내용을 비교할 수 있다.

## TASK 식별자가 전체 기록을 연결한다

`TASK-051`이라는 하나의 식별자로 TASK, Prompt, Log를 찾을 수 있다. 복잡한 별도
도구가 없어도 파일 시스템만으로 작업 이력을 탐색할 수 있다.

## 제외 범위가 적극적으로 사용된다

금융 시스템에서는 작은 변경이 Backtesting, Trading, Schema 변경으로 번지기 쉽다.
TASK마다 금지 범위를 명시한 것은 AI 작업의 범위 폭주를 막는 좋은 방법이다.

## 검증과 위험 요소를 결과에 남긴다

성공한 항목뿐 아니라 브라우저 검증 실패, timeout의 한계, Runtime 상태 계약 문제도
기록한다. 이렇게 남은 위험은 다음 TASK의 입력이 된다.

## 세션 복구에 유리하다

새로운 사람이나 AI가 다음 순서로 읽으면 이전 대화가 없어도 상당한 맥락을 복구할 수
있다.

```text
현재 상태
-> TASK
-> Prompt
-> Result Log
-> 실제 diff
```

---

# 6. 현재 하네스의 부족한 부분

## 규칙은 있지만 자동 강제가 없다

현재는 사람이 다음 항목을 직접 확인해야 한다.

```text
하나의 TASK가 여러 상태 폴더에 중복되었는가
done TASK의 상태가 DONE인가
TASK에 대응하는 Prompt와 Log가 있는가
TASK 본문이 상태 외에 변경되었는가
완료 조건별 검증 증거가 존재하는가
```

문서 규칙만으로는 실수를 예방할 수 없다. 반복 가능한 검사는 스크립트와 CI로 옮기는
것이 더 안전하다.

## 단일 검증 진입점이 없다

현재 Backend, Frontend, Runtime 검증 명령을 각각 기억해야 한다.

권장 목표:

```text
하나의 명령
-> 하네스 구조 검사
-> Python 정적 검사
-> Frontend lint와 type check
-> Backend health
-> Runtime smoke test
-> 결과 요약
```

예:

```powershell
.\scripts\verify_project.ps1
```

## 자동 테스트가 부족하다

수동 smoke test는 실제 API 연결을 확인하는 데 좋지만 회귀 원인을 빠르게 좁히기
어렵다.

최소 자동 테스트 후보:

```text
TASK 상태 중복 검사
selectedTicker 보존
traceId 생성과 유지
ticker별 Retrieval 필터
freshness score 계산
공시 0건 cache 처리
OpenAI 실패 상태
Navigation route 연결
```

## Git 상태와 TASK 경계가 자동 연결되지 않는다

현재 규칙은 TASK 단위 작은 커밋을 요구하지만, 변경 파일이 현재 TASK 범위에 속하는지
자동으로 검사하지 않는다.

개선 방향:

```text
Prompt에 예상 변경 경로 기록
-> Git diff의 실제 변경 경로 수집
-> 범위 밖 파일이 있으면 경고
-> 검증 후 TASK 단위 커밋
```

## 생성 데이터와 소스 변경의 경계가 약하다

Runtime 실행은 cache, trace, graph, memory 등의 파일을 만들 수 있다. 이 파일들이 Git
변경에 섞이면 코드 변경을 검토하기 어려워진다.

권장 분류:

```text
Git 추적:
- 작은 테스트 fixture
- 재현에 필요한 sample
- 문서화된 benchmark 결과

Git 제외:
- 사용자별 cache
- 일회성 Runtime trace
- 대량 수집 원문
- 임시 embedding
- 개발 서버 로그
```

## 현재 상태 문서는 자동 갱신되지 않는다

TASK가 완료되어도 `project/current-status.md`와 `project/roadmap.md`는 자동으로
갱신되지 않는다. 따라서 TASK 디렉터리와 상태 문서가 서로 다른 현재 상태를 설명할 수
있다.

---

# 7. 더 나은 하네스 구조 예시

현재 구조를 유지하면서 작은 자동화를 추가하는 방향이 적절하다.

```text
scripts/
├─ verify_harness.py
├─ verify_backend.ps1
├─ verify_frontend.ps1
├─ verify_runtime.ps1
└─ verify_project.ps1

tests/
├─ harness/
├─ runtime_flow/
├─ retrieval/
└─ api/

.github/
└─ workflows/
   └─ verify.yml
```

각 도구는 단일 책임을 유지한다.

| 도구 | 책임 |
|---|---|
| `verify_harness.py` | TASK, Prompt, Log 구조와 상태 검사 |
| `verify_backend.ps1` | Python compile, unit test, API health |
| `verify_frontend.ps1` | lint, type check, build |
| `verify_runtime.ps1` | 표준 Runtime query와 결과 계약 검사 |
| `verify_project.ps1` | 앞의 검사를 순서대로 호출하고 요약 |
| `verify.yml` | Pull Request에서 같은 검사를 반복 |

---

# 8. 하네스 검사기 예시

다음 코드는 권장 개념을 설명하는 예시이며 현재 프로젝트에 구현된 코드는 아니다.

```python
from pathlib import Path
import re


TASK_PATTERN = re.compile(r"^(TASK-\d{3})-.*\.md$")


def collect_task_locations(tasks_root: Path) -> dict[str, list[Path]]:
    locations: dict[str, list[Path]] = {}

    for path in tasks_root.glob("*/*.md"):
        match = TASK_PATTERN.match(path.name)
        if match:
            locations.setdefault(match.group(1), []).append(path)

    return locations


def validate_task(task_id: str, paths: list[Path], root: Path) -> list[str]:
    errors: list[str] = []

    if len(paths) != 1:
        errors.append(f"{task_id}: 상태 위치가 {len(paths)}개입니다.")
        return errors

    task_path = paths[0]
    prompt_dir = root / "prompts" / task_id
    log_dir = root / "logs" / task_id

    if not list(prompt_dir.glob("prompt-*.md")):
        errors.append(f"{task_id}: Prompt가 없습니다.")

    if task_path.parent.name == "done":
        text = task_path.read_text(encoding="utf-8")
        if not re.search(r"## 상태\s+DONE\b", text):
            errors.append(f"{task_id}: done TASK의 상태가 DONE이 아닙니다.")
        if not list(log_dir.glob("result-*.md")):
            errors.append(f"{task_id}: 완료 결과 Log가 없습니다.")

    return errors
```

실제 구현에서는 예시를 그대로 복사하기보다 다음 요구사항을 테스트로 먼저 정의하는
것이 좋다.

```text
정상 TASK는 통과한다
중복 TASK는 실패한다
done이지만 TODO이면 실패한다
Prompt가 없으면 실패한다
완료 Log가 없으면 실패한다
TASK 번호가 잘못되면 실패한다
```

---

# 9. 통합 검증 명령 예시

Windows PowerShell 기준의 권장 형태다.

```powershell
$ErrorActionPreference = "Stop"

python scripts/verify_harness.py
python -m compileall src
python -m pytest

Push-Location dashboard-ui
try {
    npm run lint
    npx tsc --noEmit
    npm run build
}
finally {
    Pop-Location
}

python -m src.runtime_flow.runtime_query_runner "삼성전자 최신 뉴스와 공시 분석"
```

이 예시도 현재 존재하는 명령이 아니라 개선 목표다. 실제 도입 시에는 외부 API 호출
비용과 MariaDB 의존성을 고려해 검증 단계를 분리하는 것이 좋다.

```text
fast:
- 하네스 검사
- unit test
- compile
- lint
- type check

integration:
- MariaDB
- Backend API
- Frontend build

external:
- OpenDART
- 뉴스 수집
- OpenAI
- 실제 Runtime query
```

모든 커밋에서 외부 API를 호출하기보다 빠른 검사는 항상 실행하고, 비용이 드는 검사는
명시적으로 선택하는 편이 안전하다.

---

# 10. 더 좋은 TASK 작성 예시

좋지 않은 TASK:

```text
RAG, 화면, DB, 테스트를 전체적으로 개선한다.
```

문제:

```text
완료 기준이 불명확하다
변경 범위가 너무 넓다
실패 원인을 분리하기 어렵다
하나의 커밋으로 검토하기 어렵다
```

권장 TASK:

```text
# TASK-052-build-harness-validator

## 상태

TODO

## 목표

TASK-Prompt-Log 구조의 누락과 중복을 자동 검사한다.

## 범위

- TASK ID 중복 검사
- 상태 폴더 중복 검사
- done 상태값 검사
- Prompt 및 Result Log 존재 검사
- 검사기 자체 단위 테스트

## 제외 범위

- Runtime 코드 변경
- Frontend 변경
- TASK 자동 이동
- Git 자동 커밋

## 완료 조건

- 정상 fixture 통과
- 중복 상태 fixture 실패
- Prompt 누락 fixture 실패
- done 상태 오류 fixture 실패
- 표준 실행 명령 문서화
```

이렇게 작성하면 구현 경계와 검증 조건이 코드로 옮겨지기 쉽다.

---

# 11. 추천 학습 실습

## 실습 1: 작업 이력 복원

TASK-050 또는 TASK-051을 선택하고 다음 순서로 읽는다.

```text
TASK
-> Prompt
-> Result Log
-> 관련 Git diff
-> 실제 코드
```

다음 질문에 답한다.

```text
원래 목표와 실제 변경이 일치하는가
제외 범위가 지켜졌는가
완료 조건별 증거가 있는가
Result에 없는 변경이 존재하는가
남은 위험이 다음 TASK로 연결되었는가
```

## 실습 2: 하네스 구조 검사기 작성

`verify_harness.py`를 작은 함수로 나눠 작성한다.

```text
TASK 수집
ID 파싱
상태 중복 검사
DONE 상태 검사
Prompt 검사
Log 검사
결과 출력
종료 코드 반환
```

검사 실패 시 사람이 읽기 쉬운 파일 경로와 원인을 출력한다.

## 실습 3: 실패하는 fixture 만들기

실제 `tasks/`를 손상시키지 말고 임시 테스트 디렉터리에 다음 사례를 만든다.

```text
같은 TASK가 todo와 done에 동시에 존재
done TASK의 상태가 TODO
Prompt 디렉터리 누락
Result Log 누락
잘못된 TASK 파일명
```

각 사례가 예상대로 실패하는지 테스트한다.

## 실습 4: 검증을 빠른 단계와 외부 단계로 분리

다음 두 명령을 설계한다.

```text
verify-fast
-> 로컬에서 수십 초 안에 완료

verify-external
-> DB와 외부 API를 실제 호출
```

이 분리는 개발 속도와 실제 통합 검증을 모두 확보하는 데 중요하다.

## 실습 5: Result Log 자동 초안 생성

검증 결과를 JSON으로 저장하고 Markdown Result 초안을 생성한다.

```json
{
  "task_id": "TASK-052",
  "checks": {
    "harness": "passed",
    "python_compile": "passed",
    "frontend_lint": "passed"
  },
  "failed_checks": [],
  "executed_at": "2026-06-10T12:00:00+09:00"
}
```

자동 생성된 결과를 사람이 검토하고 위험 요소와 판단을 추가한다. 자동화가 사람의
판단을 대체하기보다 증거 수집을 맡게 하는 것이 좋다.

## 실습 6: CI 연결

Pull Request에서 다음 조건을 확인한다.

```text
TASK ID가 존재하는가
Prompt가 존재하는가
하네스 검사가 통과하는가
Python test가 통과하는가
Frontend lint와 build가 통과하는가
```

외부 API key가 필요한 테스트는 기본 CI와 분리한다.

---

# 12. 추천 학습 순서

## 1단계: 문서 기반 하네스

```text
README
AGENTS
TASK
Prompt
Log
Architecture
Convention
```

목표는 각 문서의 책임을 구분하는 것이다.

## 2단계: 검증 하네스

```text
완료 조건
정적 검사
unit test
integration test
smoke test
외부 API test
```

목표는 "실행했다"와 "검증했다"의 차이를 이해하는 것이다.

## 3단계: 변경 관리 하네스

```text
Git diff
TASK 범위
작은 commit
생성 데이터 분리
rollback
```

목표는 코드 변경과 실행 부산물을 분리하는 것이다.

## 4단계: 자동화 하네스

```text
단일 검증 명령
구조 검사기
CI
Result 초안
상태 동기화 검사
```

목표는 사람이 기억해야 할 규칙을 실행 가능한 검사로 전환하는 것이다.

---

# 13. 하네스 품질을 평가하는 질문

새 기능을 만들기 전에 다음 체크리스트로 하네스를 평가할 수 있다.

## 작업 정의

- 하나의 TASK가 하나의 목적만 가지는가
- 범위와 제외 범위가 명확한가
- 완료 조건이 실행 가능한 문장인가

## 추적성

- TASK와 Prompt와 Log를 같은 ID로 찾을 수 있는가
- 변경 이유와 실제 결과가 남는가
- 중단된 세션을 문서만으로 이어갈 수 있는가

## 검증

- 완료 조건마다 검증 증거가 있는가
- 실패 경로도 테스트하는가
- 검증 명령이 반복 가능하고 표준화되어 있는가

## 재현성

- 의존성 버전이 고정되어 있는가
- 환경 변수 예제가 있는가
- 생성 데이터 없이도 최소 테스트를 실행할 수 있는가

## 변경 안전성

- 현재 TASK 밖의 변경을 탐지할 수 있는가
- 사용자 변경을 덮어쓰지 않는가
- 생성 파일이 Git diff에 섞이지 않는가

## 자동화

- 문서 규칙을 스크립트가 검사하는가
- 로컬과 CI가 같은 명령을 사용하는가
- 실패 시 정확한 원인과 경로를 보여주는가

---

# 14. AlphaFin LTE에 권장하는 다음 방향

현재 구조를 대규모로 바꾸기보다 다음 순서로 작은 TASK를 진행하는 것이 좋다.

```text
1. TASK-Prompt-Log 구조 검사기
2. 검사기 단위 테스트
3. 빠른 통합 검증 명령
4. Runtime 외부 검증 명령 분리
5. 생성 데이터 Git 정책 정리
6. current-status와 TASK 상태 불일치 검사
7. CI 연결
8. Result Log 자동 초안
```

가장 먼저 추천하는 작업:

```text
TASK-052-build-harness-validator
```

이 TASK는 신규 금융 기능을 만들지 않고 현재 문서 규칙을 실행 가능한 코드로 바꾸는
작업이어야 한다.

---

# 15. 최종 판단

AlphaFin LTE의 하네스는 AI 협업의 기본 개념을 학습하기에 좋은 구조다.

특히 다음 내용을 실제 파일로 확인할 수 있다.

```text
문서가 AI 작업 경계를 만드는 방법
TASK와 Prompt를 분리하는 이유
Result Log가 세션 복구에 주는 효과
제외 범위가 작업 폭주를 막는 방법
trace와 검증 증거를 남기는 방법
규칙만 있고 자동 검사가 없을 때 생기는 한계
```

다만 현재 구조를 완성된 모범 하네스로 외우면 안 된다. 가장 좋은 학습 방법은 현재
규칙을 읽고 실제 TASK 이력을 복원한 다음, 사람이 수동으로 확인하는 절차를 하나씩
검사기와 테스트로 바꾸는 것이다.

```text
문서 규칙을 이해한다
-> 실제 작업 이력과 비교한다
-> 반복되는 수동 검사를 찾는다
-> 작은 검사 스크립트를 만든다
-> 실패 fixture를 추가한다
-> 단일 검증 명령으로 묶는다
-> CI에서 반복한다
```

이 과정을 거치면 하네스는 단순한 문서 모음에서 실제로 개발 품질을 지키는 실행 가능한
시스템으로 발전한다.
