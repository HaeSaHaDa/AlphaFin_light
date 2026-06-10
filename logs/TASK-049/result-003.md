# TASK-049 Sidebar 활성 상태 후속 수정

## 발견된 문제

- Dashboard 메뉴가 `/` 경로만 기준으로 활성화되어 News 등 Dashboard 내부 섹션과 동시에 선택됐다.
- Dashboard 스크롤 상태 감지 목록에 Retrieval이 없어 Retrieval 선택 상태가 다른 섹션으로 덮였다.
- Dashboard 메뉴를 다시 선택해도 `currentSection`이 `summary`로 명시적으로 복원되지 않았다.

## 수정 내용

- Dashboard는 `/` 경로이면서 `currentSection === "summary"`일 때만 활성화한다.
- Dashboard 클릭 시 Summary 섹션으로 이동하고 상태를 동기화한다.
- 로컬 섹션 목록에 Retrieval을 실제 DOM 순서대로 추가했다.
- 깨져 있던 로컬 메뉴 한글 라벨을 정상화했다.

## 검증 결과

```text
npm run lint      성공
npx tsc --noEmit  성공
Frontend HTTP     200
Retrieval target  확인
```
