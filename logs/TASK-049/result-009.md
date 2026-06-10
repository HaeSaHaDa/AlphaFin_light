# TASK-049 대시보드 뉴스 chunk 표시 수정 결과

## 문제

- 대시보드 뉴스 영역이 기사 제목 대신 `[news_article] chunk #...` 형태로 표시됐다.
- 뉴스 영역에 공시 chunk도 함께 표시됐다.
- 최종 분석 결과의 referenced chunk에는 ID와 점수만 남아 기사 metadata가 누락됐다.

## 수정

- Runtime context의 merged evidence로 referenced chunk 정보를 복원했다.
- `metadata_json`에서 기사 제목, 언론사, 발행일, 원문 URL을 추출했다.
- 뉴스 패널은 `news_article`만 표시하도록 공시와 분리했다.
- 뉴스 카드를 제목, 언론사, 발행일, 본문 미리보기, 원문 링크로 구성했다.
- 참조 뉴스가 없는 분석은 chunk 대신 명확한 빈 상태를 표시한다.

## 검증

- trace `20260609_154829`
  - 뉴스 1건
  - 제목: `신한자산운용 AI반도체톱2플러스 순자산 3조5천억원 돌파`
  - 언론사: `SBS Biz`
  - 발행일: `2026-05-28 10:26:12`
  - 네이버 뉴스 원문 URL 확인
- trace `20260609_155431`
  - 참조 뉴스 0건
  - 공시 chunk가 뉴스로 표시되지 않음을 확인
- Python compileall 통과
- Frontend lint 통과
- TypeScript 검사 통과
- Backend health `200`
- Frontend route `200`

## 제한

인앱 브라우저 자동 검증은 Windows 샌드박스 초기화 오류로 실행되지 않았다. API 실응답과 프런트 라우트 응답으로 대체 검증했다.

## TASK 파일

이번 작업에서는 `tasks/` 아래 파일을 수정하거나 이동하지 않았다.
