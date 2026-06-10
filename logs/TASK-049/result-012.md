# TASK-049 RAG 및 공시 Memory 저장 검증 결과

## 실제 실행

- query: `삼성전자 005930 공시 실적`
- trace: `20260609_163343`
- Runtime status: `completed`
- OpenAI API 호출 성공
- 공시 수집: 5건
- 통합 retrieval: 9건
- 최종 evidence: 공시 9건

## RAG 동작 확인

다음 흐름이 실제로 완료됐다.

1. OpenDART 공시 수집
2. 공시 chunk 검색
3. news/disclosure 통합 retrieval
4. `[DISCLOSURE]` prompt context 생성
5. OpenAI 분석 실행
6. 분석 결과 및 trace 저장
7. Analysis Memory 저장
8. MID layer Memory 저장

Retrieval score:

- min: `0.4908`
- max: `0.5810`
- avg: `0.5552`
- 관련 문서 판정: `true`

## 발견한 Memory 저장 문제

기존 엔진은 분석용 `referenced_chunks`를 다음 네 필드로 축약한 뒤 Memory에 저장했다.

- chunk_id
- document_type
- score
- ticker

이 때문에 공시 제목, 본문, 날짜, URL이 Memory 파일에서 사라졌다.

## 수정

- Memory 저장에는 원본 retrieval evidence를 전달한다.
- 저장 필드에 공시 제목, 본문, 날짜, URL, metadata를 포함한다.
- 기존 trace는 Memory API에서 Runtime context를 이용해 공시 evidence를 복원한다.
- Memory 상세 화면에서 저장된 공시 근거를 펼쳐 확인할 수 있게 했다.
- RAG 평가기가 `chunk_text`와 `text` 필드를 모두 평가하도록 수정했다.

## 저장 검증

새 trace `20260609_163343`:

- Memory referenced evidence: 9건
- disclosure evidence: 9건
- 본문 포함 evidence: 9건
- 모든 ticker: `005930`
- Analysis Memory JSON 저장 확인
- MID layer Memory JSON 저장 확인
- `/api/memory/20260609_163343` 본문 반환 확인

## 남은 RAG 품질 문제

RAG 파이프라인은 동작하지만 grounding 평가는 `weak`이다.

- context overlap: `0.0`
- retrieved evidence는 9건 모두 존재한다.
- 생성된 분석은 공시의 구체 문구보다 일반적인 반도체 전망에 치우친다.

또한 현재 OpenDART collector는 목록 API 결과의 `report_name`을 `raw_text`로 저장한다. 따라서 일부 공시는 실제 본문이 아니라 공시 제목 수준의 내용만 retrieval된다.

실제 공시 원문 XML/첨부 문서를 수집하고 정제하는 별도 TASK가 필요하다.

## 검증

- Python compileall 통과
- Frontend lint 통과
- TypeScript 검사 통과
- Memory route `200`
- Backend health `200`

## TASK 파일

이번 작업에서는 `tasks/` 아래 파일을 수정하거나 이동하지 않았다.
