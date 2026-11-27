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

## 7. 2026-11-27 후속 실측

이 점검은 아래 원격 `main`의 격리 복사본에서 수행했다. Docs의 OPS-01과 DOCS-SYNC-02는 `PROPOSED`, V1-02-A는 `DONE`이고 실행 대기열은 0건이다. V1-02와 V1-03은 P0 백로그에 있다. 열린 후속 PR은 이 조사 Draft #19이며 열린 Web·Server 코드 PR은 조회되지 않았다. 별도 Codex Cloud 실행 목록은 확인하지 못했다. [TASKS](../status/TASKS.md) · [BACKLOG](../status/BACKLOG.md#p0)

| 저장소 | 검증한 원격 `main` | 실제 실행 결과 |
| --- | --- | --- |
| Docs | [`e0b1b546ad51b3d57e8c2cf2b44c8effe7c76d2c`](https://github.com/pby1360/fitlog-v2-docs/commit/e0b1b546ad51b3d57e8c2cf2b44c8effe7c76d2c) | 동기화 회귀 24개, 작업 대기열 테스트 22개 통과. 해당 커밋을 대상으로 스키마와 승인 상태 검사 통과 |
| Web | [`4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6`](https://github.com/pby1360/fitlog-v2-web/commit/4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6) | Node 20.20.2에서 `npm ci`, 린트(기존 경고 3건), 타입 검사, 로컬 API 주소로 빌드, Playwright 21개 통과. 브라우저 다운로드가 차단돼 기존 설정의 실행 파일 지정 옵션으로 시스템 Chromium을 사용했다. [Web main CI](https://github.com/pby1360/fitlog-v2-web/actions/runs/44462060250) |
| Server | [`445e0999c7d4e61c839388b69bc38f625b2378f4`](https://github.com/pby1360/fitlog-v2-server/commit/445e0999c7d4e61c839388b69bc38f625b2378f4) | JDK 21.0.13에서 `./gradlew test --no-daemon` 실행. 내장 PostgreSQL을 사용한 통합 테스트 포함 91개 통과, 실패·건너뜀 0개. [Server main CI](https://github.com/pby1360/fitlog-v2-server/actions/runs/45988479704) |

### OPS-01 배포 및 복구

- 마지막으로 확인된 성공 Firebase 게시 SHA는 `3d6412ec605ed6f83f86b1e51d6b740df9db25d2`다. Web `main`은 10커밋 앞서며 V1-04를 포함한다. 11월 20일 수동 실행은 `confirm_deploy=false`가 원인이었고 게시 잡을 시작하지 않았다. 실제 병합 범위에서 Web #44는 `tests`, Server #44는 `review`로 분류됨을 로컬에서 재현했다. 수동 확인 `false`는 거부되고 `true`는 배포 후보로 분류됨도 로컬 스크립트로 확인했다. [Web 커밋 비교](https://github.com/pby1360/fitlog-v2-web/compare/3d6412ec605ed6f83f86b1e51d6b740df9db25d2...4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6) · [마지막 성공 게시](https://github.com/pby1360/fitlog-v2-web/actions/runs/43246172583) · [수동 실행 실패](https://github.com/pby1360/fitlog-v2-web/actions/runs/44727034127)
- 마지막으로 확인한 Cloud Run 게시 SHA는 `1154a06268b0336ab5154c9c2c0d8b405bad8717`이며 로그의 리비전은 `fitlog-server-00005-8tn`이다. 그 SHA부터 현재 Server `main`까지 애플리케이션 코드와 Flyway 파일의 변경은 없다. #44의 `recovery-` 보존 파일 변경은 병합됐으며 운영 Registry 정책과 태그 적용 여부는 조회하지 못했다. [Cloud Run 배포 로그](https://github.com/pby1360/fitlog-v2-server/actions/runs/37634291023) · [Server 커밋 비교](https://github.com/pby1360/fitlog-v2-server/compare/1154a06268b0336ab5154c9c2c0d8b405bad8717...445e0999c7d4e61c839388b69bc38f625b2378f4)
- 로컬 빌드의 `/history/42`와 `/auth/callback` 직접 요청은 SPA 셸을 반환했다. Chromium에서 서비스 워커 활성화, 새로고침 후 제어, 앱 셸과 해시가 붙은 자산의 캐싱을 확인했다. Firebase 설정 파일에서 SPA 재작성과 자산·서비스 워커 캐시 지시문을 확인했다. 실제 Live 배포 간 캐시 갱신은 미검증이다.
- Hosting 관리 API, Cloud Run, Artifact Registry와 공개 웹 호스트 요청은 실행 환경 프록시가 거부했다. 11월 20일 운영 담당자 관측의 Hosting Live `49b946ad2b8aa4d8`와 직전 `8106f0d437872a4e`, Cloud Run `00005-8tn` 트래픽 100%, 운영 이미지 격리 재기동 증거는 보존한다. 현재 Live의 파일 해시와 SHA 대응, 직전 릴리스 복구 적합성, 최신 Cloud Run 트래픽과 digest 보존 여부는 미확인이다. 운영 담당자의 읽기 전용 출력으로 먼저 대조한다. [배포 증거](DEPLOYMENT.md#ops-01-배포-증거) · [복구 검증](RUNBOOK.md#00005-격리-검증-결과)

### V1-02 자동 검증과 남은 실기기 검증

- Web은 모의 OAuth 콜백·일회성 코드 교환·실패/만료, 동시 401 갱신 및 실패, 로그아웃, 탈퇴 확인과 204·409를 검증했다. 준비된 프로그램 선택부터 세션 시작, 세트 저장 실패 후 재시도, 휴식, 완료, 일지 상세로 이어지는 흐름도 통과했다. Server는 공급자 식별자와 이메일 충돌, 갱신 토큰 회전과 기기별 세션, 탈퇴 시 데이터 파기 및 409 트랜잭션 롤백을 테스트했다. [Web 검증 코드](https://github.com/pby1360/fitlog-v2-web/tree/4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6/tests) · [Server 검증 코드](https://github.com/pby1360/fitlog-v2-server/tree/445e0999c7d4e61c839388b69bc38f625b2378f4/src/test)
- 브라우저의 실제 프로그램 생성부터 시작하는 전체 흐름, 모바일 백그라운드·네트워크 재접속, 탭 간 갱신, 실제 OAuth 공급자 콜백과 물리 기기 검증이 남았다. 승인된 비운영 Web/API/격리 DB, 공급자별 전용 계정, iOS Safari·Android Chrome을 준비한다. 각 공급자 첫 로그인·취소·재로그인 → 만료/갱신 → 프로그램 직접 생성 → 시작/첫 세트/휴식/복귀/완료 → 일지 실측 확인 → 로그아웃/재접속 순으로 확인한다. 탈퇴는 별도 전용 계정의 204와 격리 충돌 데이터의 409를 확인한다. 기기·OS·브라우저·SHA·KST 시각 및 결과만 기록한다. [공식 수동 체크리스트](../features/account/TECH_SPEC.md#실제-oauth-및-휴대폰-수동-검증-체크리스트)

### DOCS-SYNC-02 발신·수신·중복 검증

- 두 발신 워크플로의 실제 검사 스텝에 GitHub API 모의를 연결해 저장소별 정상 트레일러, 트레일러 누락, PR 본문 필드 삽입 차단을 검증했다(6개). Server #44의 실제 병합 메시지에는 승인 트레일러가 없었으며 토큰 발급·Dispatch 정상 생략을 Actions에서 확인했다. [Server 발신 실행](https://github.com/pby1360/fitlog-v2-server/actions/runs/45988480781)
- Web 발신 및 Docs 수신의 기존 성공 실행을 확인했다. Docs 수신 로그에는 이미 수동 병합한 #11을 확인하고 종료한 결과가 남았다. 실제 Server 발신과 신규 Docs PR 자동 병합은 미검증이다. Docs PR은 개발 루프에서 준비하고, Actions는 승인된 기존 PR을 찾는다. [Web 발신 실행](https://github.com/pby1360/fitlog-v2-web/actions/runs/44462060315/attempts/2) · [Docs 수신 로그](https://github.com/pby1360/fitlog-v2-docs/actions/runs/44508885506/job/135510769314)
- 수신 회귀 테스트에서 승인된 SHA 1회 병합, 중복 이벤트 무변경, SHA·승인 불일치, 문서 범위, 검증 중 base 이동 차단을 확인했다. 같은 코드 PR의 실행은 Actions가 직렬화한다. 다른 Docs PR이 마지막 base 확인과 병합 API 호출 사이에 병합되는 경우까지 보장하려면 최신 base를 강제하는 보호 규칙 또는 저장소 단위 직렬 병합이 필요하다. 실제 보호·App 설치 설정은 관리자 확인이 필요하다. 승인된 비운영 PR에서 SHA를 고정하고 최초 자동 병합과 재전송 무변경을 실측한다. [동기화 운영 절차](DOCS_SYNC.md#docs-sync-02-후속-검증)

### V1-03 최소 관측 스키마 초안

- 현재 서버 Request ID 필터·Actuator와 프런트엔드 API 오류에 요청 단위 추적 근거가 있다. 서버 로그 일부에는 내부 회원·세션 ID나 DB의 원문 예외 메시지가 남을 수 있으며, Web의 네트워크 오류와 콜백 중단은 서버 로그만으로 확인할 수 없다. 수집 전 오류 필드를 허용 목록으로 제한한다. [요청 ID 필터](https://github.com/pby1360/fitlog-v2-server/blob/445e0999c7d4e61c839388b69bc38f625b2378f4/src/main/java/com/fitlog/fitlogv2server/global/logging/RequestIdFilter.java) · [서버 예외 처리](https://github.com/pby1360/fitlog-v2-server/blob/445e0999c7d4e61c839388b69bc38f625b2378f4/src/main/java/com/fitlog/fitlogv2server/global/exception/GlobalExceptionHandler.java)
- 이벤트는 `login_result`, `signup_result`, `program_created`, `first_set_recorded`, `workout_completed`, `api_error`로 제안한다. 공통 필드는 `schema_version`, 서버 관측 시각, 환경, 앱 릴리스이며, 인증은 제공자와 성공/실패/취소, 오류는 허용된 작업명·오류 코드·HTTP 상태 및 요청 ID만 사용한다. 성공 이벤트는 커밋된 도메인 전이 기준으로 중복을 제거한다. 원문 URL·쿼리·헤더·본문, 이메일, IP, 회원·세션 식별자, OAuth 코드·토큰, 운동 상세는 보내지 않는다.
- Cloud Logging 기반 집계는 신규 외부 SDK 없이 서버 건수와 오류 진단을 우선 제공하며 로그 용량·보존·IAM을 관리해야 한다. 단계별 총건수는 동시 이용자의 코호트 이탈률을 측정할 수 없다. GA4는 퍼널 기능이 있으나 수집 설정과 쿠키·보존 검토가 필요하다. Plausible은 쿠키 없는 집계와 Business 플랜의 퍼널을 제공하며 구독과 외부 처리 검토가 필요하다. Sentry는 오류 분류·릴리스 추적에 적합하며 발생량과 스크러빙을 관리해야 한다. [Cloud Logging](https://cloud.google.com/products/observability/pricing) · [GA4](https://support.google.com/analytics/answer/9327974) · [Plausible](https://plausible.io/docs/funnel-analysis) · [Sentry](https://sentry.io/pricing/)
- 승인 후 비운영에서 합성 전환 성공·중도 이탈·실패·중복 요청·네트워크 단절을 주입한다. 이벤트 수, 중복 미집계, 오류와 요청 ID의 대조, 개인정보 테스트 문자열 미기록을 확인한다. 출시 기준에 코호트 연결이 필요하면 식별 방식·보존 기간·열람 권한과 실험 범위를 별도 승인한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 후속 조사 기록·검토용 Draft |
| 원본 출처 | Docs TASKS/BACKLOG, GitHub PR #44 병합, 서버/웹 Actions 로그, 관련 Tech Spec과 운영 문서 |
| 관련 작업 | OPS-01, OPS-02, V1-02, DOCS-SYNC-02, V1-03 |
| 최종 검증일 | 2026-11-27 |
| 관련 설계 | [개발 절차](DEVELOPMENT_WORKFLOW.md), [배포](DEPLOYMENT.md), [Docs 동기화](DOCS_SYNC.md), [계정](../features/account/TECH_SPEC.md) |
