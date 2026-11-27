# FitLog V2 후속 실행 준비 및 검증 근거 — 2026-11-27

이 문서는 [TASKS](../status/TASKS.md)의 실행 상태나 [BACKLOG](../status/BACKLOG.md)의 우선순위를 대체하지 않는 **비운영 사전 점검 기록**이다. 사용자로부터 남은 업무 진행 요청을 받았으나, 운영 배포·트래픽 전환·OAuth 실계정/휴대폰 검증·운영 DB 접근은 이 문서만으로 승인·실행되지 않는다. 실제 Codex Cloud 실행 ID, Docs 작업 선점 및 운영 콘솔의 최신 상태는 확인하지 않았다.

## 1. OPS-02 코드 병합 완료와 운영 미적용의 구분

- [Server PR #44](https://github.com/pby1360/fitlog-v2-server/pull/44)는 2026-11-27 20:11:55 KST에 병합됐다. Server main 병합 SHA는 `445e0999c7d4e61c839388b69bc38f625b2378f4`이다.
- 변경은 `artifact-cleanup-policy.json`의 `fitlog-server` 패키지 + `recovery-` 태그에 대한 Keep 조건이며, 기존 최근 6개/14일 규칙을 유지한다.
- [병합 후 Server Actions](https://github.com/pby1360/fitlog-v2-server/actions/runs/45988479704): `changes`, `test` 성공, `deploy` 생략. **운영 Cloud Run 배포나 Artifact Registry 정리 정책 적용의 증거가 아니다.**
- [병합 후 Docs 알림 Actions](https://github.com/pby1360/fitlog-v2-server/actions/runs/45988480781): 워크플로 성공이지만 실제 Dispatch App 토큰 발급·Docs 이벤트 전송 단계는 생략됐다. 구현 승인 트레일러 없는 PR이므로 이것을 Server → Docs E2E 통과로 기록하지 않는다.
- 별도 운영 승인 전까지 이미지 태그 추가, Registry 정리 정책 적용·dry-run 설정 변경 및 롤백을 실행하지 않는다.

## 2. OPS-01 — 배포와 복구 증거 (P0, TASKS: PROPOSED)

**확인한 근거:** [배포 절차](DEPLOYMENT.md#ops-01-배포-증거), [롤백 런북](RUNBOOK.md#ops-01-롤백-검증).

- GitHub Web main `4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6`의 코드/CI는 확인 가능하다. Firebase Hosting의 **현재 Live 릴리스·파일 해시**는 이 점검에서 직접 읽지 못했다. 11월 20일 관측 기록과 현재 실제 릴리스가 같다고 가정하지 않는다.
- [11월 20일 Web 수동 Actions](https://github.com/pby1360/fitlog-v2-web/actions/runs/44727034127)는 `CONFIRM_DEPLOY=false`로 실행되었으며, `Manual production deployment requires main and explicit confirmation.` 오류로 배포 전 중단됐다. 이는 명시적 확인이 없는 수동 운영 배포를 막은 **의도된 안전 게이트**로, 앱 빌드/Playwright 테스트 실패 증거가 아니다.
- Server PR #44 병합 후 배포 잡도 건너뛰었으므로 이 병합만으로 운영 서버가 변경됐다고 판정하지 않는다. 마지막으로 기록된 Cloud Run `00005-8tn` 운영 상태와 digest는 새 읽기 전용 관측이 필요하다.

**후속 절차(운영 담당자 실행 필요):**
1. Firebase Hosting 사이트 `fit2log.com`의 현행/직전 릴리스 ID·게시 시각·파일 manifest 또는 해시를 읽기 전용으로 확인하고, Web main 빌드와 대조한다.
2. Cloud Run `fitlog-server`의 현재 리비전·트래픽·실제 이미지 digest 및 복구 대상 `00005` digest 보존 여부를 읽기 전용으로 확인한다.
3. 복구 후보의 V7/Flyway 호환성 및 캐시·콜백·SPA 복귀 테스트 계획을 승인된 담당자와 확정한다.
4. **실제 Hosting 게시, 복구 릴리스 활성화, Cloud Run 트래픽 전환은 별도 명시 승인과 사전 원복 계획 없이 실행하지 않는다.**

## 3. V1-02 — 실제 사용자 플로우 검증 (P0, 로컬 자동 검증과 별개)

[계정 Tech Spec 체크리스트](../features/account/TECH_SPEC.md#실제-oauth-및-휴대폰-수동-검증-체크리스트)와 [BACKLOG](../status/BACKLOG.md#p0)에 따른다. V1-02-A의 로컬 Playwright/서버 테스트 완료를 실제 OAuth·휴대폰 검증 완료로 확대하지 않는다.

| 비운영 검증 | 완료 판정 기준 | 이번 확인 |
| --- | --- | --- |
| Google·Kakao | 첫 로그인, 재로그인, 공급자 취소, 토큰 갱신·로그아웃 | 미실행: 테스트 계정 및 브라우저 세션 미제공 |
| 실기기 운동 흐름 | 프로그램 선택 → 세트/휴식 → 완료 → 캘린더·일지 상세 | 미실행: 실기기 접근 없음 |
| 전용 테스트 계정 탈퇴 | 취소, 완료 후 재접속 차단, 독립 데이터로 409 롤백 | 미실행: 테스트 계정과 격리 데이터 미제공 |

수행 시 계정·세션 토큰·회원 데이터가 로그나 문서에 노출되지 않도록 한다. 테스트 기기, OS/브라우저, Web/Server SHA, 실행 시각, 성공/실패 증거만 기록한다.

## 4. DOCS-SYNC-02 — 교차 저장소 E2E (TASKS: PROPOSED)

[동기화 규칙](DOCS_SYNC.md#docs-sync-02-후속-검증) 기준, 과거 Web → Docs 인증·발신·수신은 검증됐다. 이번 Server PR #44의 성공한 알림 워크플로는 실제 발신이 생략됐으므로 미검증 상태를 바꾸지 않는다.

- 사전 검사: 두 GitHub App의 설치 범위·최소 권한, 서버의 발신 설정과 Docs 수신 설정, Docs 필수 검사 및 브랜치 보호를 비밀값 없이 확인한다.
- 비운영 E2E: **새로 승인받은 구현 PR 및 정확히 지정된 Docs PR head SHA**에 대해서만 코드 병합 승인 트레일러를 사용한다. Server 발신 토큰 → Dispatch → Docs 인증/검사 → 승인 head의 정확한 1회 병합 → 중복 이벤트 무변경 종료까지 확인한다.
- 제품 범위·보안·아키텍처 변경, OPS-02와 같은 운영 정책 변경, 기존 병합 PR의 트레일러 소급 삽입은 자동 병합 시험에 사용하지 않는다.
- 현재는 새 승인 구현 PR/Docs head 및 실행 가능한 Codex/Work 인터페이스를 확보하지 못해 **Cloud 실행 상태 미확인**, `PROPOSED` 유지.

## 5. V1-03 — 오류·이탈 관측 (P0 후보, 신규 구현 미착수)

[BACKLOG](../status/BACKLOG.md#p0)과 [CURRENT_STATUS](../status/CURRENT_STATUS.md)의 기존 확인에서는 Actuator 헬스체크 및 요청 ID가 존재하지만 가입·프로그램 생성·세션 완료 전환, 구조화 로그 및 오류 대시보드의 종단 간 운영 검증은 부족하다.

**승인 전 설계 검토 범위:**
- 가입 성공·프로그램 생성·세션 완료의 최소 이벤트 스키마와 합법적 수집 목적·보유 기간·동의 요구 여부를 확정한다. 이메일, 이름, 토큰, 운동 상세 기록은 이벤트 속성에 넣지 않는다.
- 선택할 관측 도구(GA4/Plausible/Sentry 또는 기존 로깅 활용)의 비용·권한·데이터 이전·보존 정책을 비교한다. 도구 선택 전 신규 운영 계정/SDK/시크릿을 만들지 않는다.
- 비운영 테스트 이벤트 하나와 오류 하나에서 집계 값, 요청 ID의 연계, 중복 전송, 개인정보 마스킹을 확인하는 완료 기준을 작성한다.
- 구현 승인 후에만 별도 TASKS 선점과 코드 Draft PR·테스트 절차를 수행한다.

## 6. 진행 및 중단 조건

1. **SSOT:** TASKS의 OPS-01·DOCS-SYNC-02는 이 문서 작성 당시 `PROPOSED`이며 승인·선점·시작 시각 및 실행 ID가 없다. V1-02와 V1-03은 BACKLOG의 P0 후속 과제이다. 동일 Task의 선점·실행·PR 중복 여부를 실제 실행 직전 재검증한다.
2. 직접 Codex Cloud 실행과 Firebase Hosting/Cloud Run 콘솔 조회 인터페이스가 이 점검 환경에 제공되지 않았다. 실행이 확인되지 않은 업무는 `IN_PROGRESS`나 `DONE`으로 변경하지 않는다.
3. 사용자가 보류한 **V1-01은 자동 착수하지 않는다.** 공개 법률 고지 미확정은 출시 차단 요인으로 유지한다.
4. 각 구현은 기존 `AGENTS.md`, `fitlog-loop` 및 [선점 절차](DEVELOPMENT_WORKFLOW.md#승인과-선점)를 따른다. 대상 변경·운영 영향·정책 승인은 사용자의 별도 결정이 필요하다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 후속 조사 기록·검토용 Draft |
| 원본 출처 | Docs TASKS/BACKLOG, GitHub PR #44 병합, 서버/웹 Actions 로그, 관련 Tech Spec과 운영 문서 |
| 관련 작업 | OPS-01, OPS-02, V1-02, DOCS-SYNC-02, V1-03 |
| 최종 검증일 | 2026-11-27 |
| 관련 설계 | [개발 절차](DEVELOPMENT_WORKFLOW.md), [배포](DEPLOYMENT.md), [Docs 동기화](DOCS_SYNC.md), [계정](../features/account/TECH_SPEC.md) |
