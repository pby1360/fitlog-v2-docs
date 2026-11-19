# 작업 실행 현황

이 파일은 개발 작업 실행 상태의 원본이다. 요구사항, 수용 기준과 우선순위는 [백로그](BACKLOG.md)에 둔다. 여기의 우선순위는 해당 백로그 위치를 참조한다. 구현 사실과 검증 범위는 [현재 상태](CURRENT_STATUS.md)에서 확인한다. 상태 전이와 선점은 [개발 작업 등록과 실행](../operations/DEVELOPMENT_WORKFLOW.md)을 따른다.

각 작업은 고유한 Task ID와 같은 이름의 제목 아래에 둔다. 백로그 ID가 있으면 사용하며, 하나의 백로그 항목을 여러 실행 작업으로 나누면 각 Task에 고유한 접미사를 붙이고 같은 백로그 ID를 연결한다. 별도 작업의 완료·취소 기록은 보존한다. 시각은 `Asia/Seoul`의 `YYYY-MM-DDTHH:mm:ss+09:00` 형식이다. `미확인`은 근거를 확보하지 못한 값, `해당 없음`은 적용되지 않는 값이다.

신규 등록은 아래와 같은 필드 순서로 작성한다. `STARTING`에는 승인 근거, 담당자, 대상 저장소와 선점 ID를 채우고, `IN_PROGRESS` 갱신에는 실제 실행 ID 또는 시작 근거를 채운다. 승인·시작·완료 시각은 그 이벤트가 확인됐을 때 기록한다.

## 작업 기록

아래 항목은 GitHub의 실제 병합 상태와 `main` 반영 커밋을 대조해 복원했다. 확인되지 않은 이전 실행의 시작 또는 승인 시각은 복원하지 않았다.

### DOCS-01

| 항목 | 값 |
| --- | --- |
| 작업 제목 | 공식 문서 체계 구축과 Obsidian 이관 |
| 우선순위 | 해당 없음 |
| 작업 상태 | `DONE` |
| 대상 저장소 | `fitlog-v2-docs` |
| 담당 에이전트 | Codex |
| Cloud 환경 | `fitlog-v2` |
| Cloud 실행 ID | 미확인 |
| 선점 ID | 해당 없음 |
| 작업 브랜치 | `docs/bootstrap-documentation` |
| 코드 PR | 해당 없음 |
| Docs PR | [docs #1](https://github.com/pby1360/fitlog-v2-docs/pull/1) |
| 승인 근거 | 미확인 |
| 승인 시각 | 미확인 |
| 시작 시각 | 미확인 |
| 실행 시작 근거 | 미확인 |
| 마지막 상태 갱신 시각 | `2026-11-19T08:51:27+09:00` |
| 완료 시각 | `2026-11-18T22:58:17+09:00` |
| 차단 사유 | 해당 없음 |
| 관련 BACKLOG | 해당 없음 |
| 관련 PRD | 해당 없음 |
| 관련 Tech Spec | 해당 없음 |
| 완료 근거 | [docs `06977e2`](https://github.com/pby1360/fitlog-v2-docs/commit/06977e26bfbf24536f784d7600369b0e58c06e83) |

### DOCS-02

| 항목 | 값 |
| --- | --- |
| 작업 제목 | 구현 현황 검증과 백로그 정리 |
| 우선순위 | 해당 없음 |
| 작업 상태 | `DONE` |
| 대상 저장소 | `fitlog-v2-docs` |
| 담당 에이전트 | Codex |
| Cloud 환경 | `fitlog-v2` |
| Cloud 실행 ID | 미확인 |
| 선점 ID | 해당 없음 |
| 작업 브랜치 | `docs/verify-current-status` |
| 코드 PR | 해당 없음 |
| Docs PR | [docs #2](https://github.com/pby1360/fitlog-v2-docs/pull/2) |
| 승인 근거 | 미확인 |
| 승인 시각 | 미확인 |
| 시작 시각 | 미확인 |
| 실행 시작 근거 | 미확인 |
| 마지막 상태 갱신 시각 | `2026-11-19T08:51:27+09:00` |
| 완료 시각 | `2026-11-18T23:27:35+09:00` |
| 차단 사유 | 해당 없음 |
| 관련 BACKLOG | [검증 결과가 반영된 백로그](BACKLOG.md) |
| 관련 PRD | 해당 없음 |
| 관련 Tech Spec | 해당 없음 |
| 완료 근거 | [docs `ded121a`](https://github.com/pby1360/fitlog-v2-docs/commit/ded121a4b7428b1aaefe59b3e9aa41a67eff76d2) |

### DEV-LOOP-01

| 항목 | 값 |
| --- | --- |
| 작업 제목 | 서버·웹 개발 규칙과 검증 루프 구축 |
| 우선순위 | 해당 없음 |
| 작업 상태 | `DONE` |
| 대상 저장소 | `fitlog-v2-server`, `fitlog-v2-web` |
| 담당 에이전트 | Codex |
| Cloud 환경 | `fitlog-v2` |
| Cloud 실행 ID | 미확인 |
| 선점 ID | 해당 없음 |
| 작업 브랜치 | 서버 `docs/fitlog-loop-server`, 웹 `docs/fitlog-loop-web` |
| 코드 PR | [server #40](https://github.com/pby1360/fitlog-v2-server/pull/40), [web #39](https://github.com/pby1360/fitlog-v2-web/pull/39) |
| Docs PR | 해당 없음 |
| 승인 근거 | 개발 규칙 PR 병합 요청 |
| 승인 시각 | 미확인 |
| 시작 시각 | 미확인 |
| 실행 시작 근거 | 미확인 |
| 마지막 상태 갱신 시각 | `2026-11-19T08:51:27+09:00` |
| 완료 시각 | `2026-11-18T23:53:49+09:00` |
| 차단 사유 | 해당 없음 |
| 관련 BACKLOG | 해당 없음 |
| 관련 PRD | 해당 없음 |
| 관련 Tech Spec | 해당 없음 |
| 완료 근거 | [server `52d93f3`](https://github.com/pby1360/fitlog-v2-server/commit/52d93f30add026b59fc7e48f591937e0a54bbe23), [web `29f4553`](https://github.com/pby1360/fitlog-v2-web/commit/29f4553c382296cd35ddd60df54e9618d17816cb) · 문서 저장소는 참조 범위 |

### V1-04

| 항목 | 값 |
| --- | --- |
| 작업 제목 | 운동 일지 캘린더 안정화 |
| 우선순위 | [P1](BACKLOG.md#p1) |
| 작업 상태 | `DONE` |
| 대상 저장소 | `fitlog-v2-web`, `fitlog-v2-docs` |
| 담당 에이전트 | Codex |
| Cloud 환경 | `fitlog-v2` |
| Cloud 실행 ID | 미확인 |
| 선점 ID | 해당 없음 |
| 작업 브랜치 | 웹 `fix/v1-04-calendar`, Docs `docs/docs-sync-automation` |
| 코드 PR | [web #40](https://github.com/pby1360/fitlog-v2-web/pull/40) |
| Docs PR | [docs #3](https://github.com/pby1360/fitlog-v2-docs/pull/3) |
| 승인 근거 | V1-04 코드 PR 및 후속 문서 PR 병합 요청 |
| 승인 시각 | 미확인 |
| 시작 시각 | 미확인 |
| 실행 시작 근거 | 미확인 |
| 마지막 상태 갱신 시각 | `2026-11-19T08:51:27+09:00` |
| 완료 시각 | `2026-11-19T08:48:25+09:00` |
| 차단 사유 | 해당 없음 |
| 관련 BACKLOG | [V1-04](BACKLOG.md#p1) |
| 관련 PRD | [운동 일지 PRD](../features/workout-history/PRD.md) |
| 관련 Tech Spec | [운동 일지 Tech Spec](../features/workout-history/TECH_SPEC.md) |
| 완료 근거 | [web `6f8cc4c`](https://github.com/pby1360/fitlog-v2-web/commit/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1), [docs `7313dac`](https://github.com/pby1360/fitlog-v2-docs/commit/7313dac365316a773c2890f9f502beb8fcaf9f71) · [로컬 Playwright 12개 통과 기록](../history/2026-11-19.md). 운영 배포·실데이터 검증은 확인 대기. |

### DOCS-SYNC-01

| 항목 | 값 |
| --- | --- |
| 작업 제목 | 코드·문서 동기화 워크플로 구축 |
| 우선순위 | 해당 없음 |
| 작업 상태 | `DONE` |
| 대상 저장소 | `fitlog-v2-docs`, `fitlog-v2-server`, `fitlog-v2-web` |
| 담당 에이전트 | Codex |
| Cloud 환경 | `fitlog-v2` |
| Cloud 실행 ID | 미확인 |
| 선점 ID | 해당 없음 |
| 작업 브랜치 | 세 저장소의 `docs/docs-sync-automation` |
| 코드 PR | [server #41](https://github.com/pby1360/fitlog-v2-server/pull/41), [web #41](https://github.com/pby1360/fitlog-v2-web/pull/41) |
| Docs PR | [docs #3](https://github.com/pby1360/fitlog-v2-docs/pull/3) |
| 승인 근거 | 문서 자동 동기화 설정 PR 병합 요청 |
| 승인 시각 | 미확인 |
| 시작 시각 | 미확인 |
| 실행 시작 근거 | 미확인 |
| 마지막 상태 갱신 시각 | `2026-11-19T08:51:27+09:00` |
| 완료 시각 | `2026-11-19T08:49:00+09:00` |
| 차단 사유 | 해당 없음 |
| 관련 BACKLOG | 해당 없음 |
| 관련 PRD | 해당 없음 |
| 관련 Tech Spec | [동기화 운영 설계](../operations/DOCS_SYNC.md) |
| 완료 근거 | [docs `7313dac`](https://github.com/pby1360/fitlog-v2-docs/commit/7313dac365316a773c2890f9f502beb8fcaf9f71), [server `31cc7eb`](https://github.com/pby1360/fitlog-v2-server/commit/31cc7eb95e4777cb8d73e7aba26d6ff74a7743ca), [web `a344499`](https://github.com/pby1360/fitlog-v2-web/commit/a3444992855406dc51ed3a5542f7c3dddd830b42) · GitHub App 설치 및 실제 연동 검증은 후속 설정. |

### V1-02-A

| 항목 | 값 |
| --- | --- |
| 작업 제목 | 핵심 사용자 흐름 자동 검증 강화 |
| 우선순위 | [P0](BACKLOG.md#p0) |
| 작업 상태 | `IN_PROGRESS` |
| 대상 저장소 | `fitlog-v2-web`, `fitlog-v2-server`(기존 테스트 재검증), `fitlog-v2-docs` |
| 담당 에이전트 | Codex |
| Cloud 환경 | `fitlog-v2` |
| Cloud 실행 ID | 미확인 (현재 Codex 세션을 계속 사용) |
| 선점 ID | `99a8452e1d9c` |
| 작업 브랜치 | 웹 `test/v1-02-a-core-flows` |
| 코드 PR | 해당 없음 |
| Docs PR | 해당 없음 |
| 승인 근거 | V1-02-A 작업 범위와 검증 계획을 보고한 대화에서 사용자가 “실행해”로 승인. 모의 API Playwright, 기존 서버 테스트 재검증, 검증 문서와 Draft PR에 한정 |
| 승인 시각 | `2026-11-19T13:32:06+09:00` (대화 승인 확인 시각) |
| 시작 시각 | `2026-11-19T13:36:02+09:00` |
| 실행 시작 근거 | [선점 PR #9](https://github.com/pby1360/fitlog-v2-docs/pull/9) main 반영 확인 후 13:36:02 KST에 현재 fitlog-v2 Cloud 환경에서 웹 검증용 브랜치 생성 |
| 마지막 상태 갱신 시각 | `2026-11-19T13:36:33+09:00` |
| 완료 시각 | 해당 없음 |
| 차단 사유 | 해당 없음 |
| 관련 BACKLOG | [V1-02](BACKLOG.md#p0) |
| 관련 PRD | [계정](../features/account/PRD.md), [운동 프로그램](../features/workout-program/PRD.md), [운동 세션](../features/workout-session/PRD.md), [운동 일지](../features/workout-history/PRD.md) |
| 관련 Tech Spec | [계정](../features/account/TECH_SPEC.md), [운동 프로그램](../features/workout-program/TECH_SPEC.md), [운동 세션](../features/workout-session/TECH_SPEC.md), [운동 일지](../features/workout-history/TECH_SPEC.md) |
| 완료 근거 | 해당 없음 |

## 문서 추적 정보

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Docs 중심 작업 상태 관리 요청, 각 작업의 GitHub PR과 병합 커밋 |
| 관련 기능 또는 Issue | [백로그](BACKLOG.md), [현재 상태](CURRENT_STATUS.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [개발 작업 등록과 실행](../operations/DEVELOPMENT_WORKFLOW.md), [문서 관리 규칙](../AGENTS.md) |
