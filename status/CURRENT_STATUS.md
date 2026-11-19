# 현재 구현 및 검증 상태

2026-11-19 웹 main에서 V1-04 코드 병합을 확인했다. 캘린더 수용 기준은 로컬 Playwright 12개를 통과했다. 운영 배포와 실제 데이터 검증은 확인 대기다. 출시 판정은 [DoD-1과 DoD-2](../product/RELEASE_CRITERIA.md)를 따른다.

| 저장소 | 원격 `main` 기준 |
| --- | --- |
| 문서 | [`7313dac`](https://github.com/pby1360/fitlog-v2-docs/tree/7313dac365316a773c2890f9f502beb8fcaf9f71), 문서 동기화 설정과 V1-04 기록 병합 |
| 서버 | [`31cc7eb`](https://github.com/pby1360/fitlog-v2-server/tree/31cc7eb95e4777cb8d73e7aba26d6ff74a7743ca), 문서 동기화 설정 병합. 런타임 검사 기준은 `1154a06`. |
| 웹 | [`a344499`](https://github.com/pby1360/fitlog-v2-web/tree/a3444992855406dc51ed3a5542f7c3dddd830b42), 문서 동기화 설정 병합. V1-04 검증 기준은 [`6f8cc4c`](https://github.com/pby1360/fitlog-v2-web/tree/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1). |

| 판정 | 기준 |
| --- | --- |
| 구현 완료 | 기준 커밋에서 요구 동작의 코드 경로를 확인했다. 테스트를 실행한 범위는 아래에 적는다. |
| 일부 구현 | 일부 경로가 있거나 수용 기준에 미달하는 부분을 확인했다. |
| 미구현 | 요구된 API·UI·데이터 모델을 기준 커밋에서 확인할 수 없다. |
| 버그 및 기술 부채 | 재현한 동작 결함 또는 코드에서 확인한 품질·유지보수 문제다. |
| 확인 필요 | 출시·운영 관측이나 제품 범위 결정의 근거가 더 필요하다. |

## 요구사항별 판정

| 요구사항 | 판정 | 구현·검증 근거 및 남은 조건 |
| --- | --- | --- |
| A-1 Google·Kakao 로그인 | 구현 완료 | 로그인 모달, 콜백의 일회용 코드 교환, 갱신·로그아웃이 연결되어 있다. 서버 통합 테스트는 교환 코드 일회성 및 갱신 회전을 검사한다. 실제 두 공급자 로그인을 [V1-02](BACKLOG.md#p0)에서 확인한다. [로그인 모달](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/components/feature/LoginModal.tsx), [웹 콜백](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/auth/callback/page.tsx#L17-L39), [인증 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/auth/AuthIntegrationTest.java) |
| A-2 기본 프로필 및 닉네임 | 구현 완료 | `GET/PATCH /api/members/me`와 화면 저장이 연결되어 있다. 전화번호·생년월일은 V7에서 제거됐다. 선택형 신체 정보의 제품 범위는 [V1-11](BACKLOG.md#p2)에서 확인한다. [회원 컨트롤러](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/member/controller/MemberController.java#L26-L51), [프로필 화면](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/profile/page.tsx#L78-L106), [개인정보 ADR](../decisions/0005-member-privacy-and-withdrawal.md) |
| B-1 공용 운동 종목 | 일부 구현 | Flyway V2에 부위 7개·종목 23개가 있다. [PRD](../features/workout-program/PRD.md)의 50~100개 및 M5 목표 80개와 차이가 있다. 운영 DB 총수와 별개로 [V1-05](BACKLOG.md#p1)에서 추적한다. [시드 SQL](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration/V2__seed_master_data.sql) |
| B-2 프로그램 CRUD | 구현 완료 | 목록·생성·수정·소프트 삭제를 웹과 서버에서 확인했다. 소프트 삭제는 기존 세션 참조를 보존한다. [웹 API](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/services/api.ts#L282-L339), [서버 서비스](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutprogram/service/WorkoutProgramService.java#L28-L67) |
| B-3 다중 부위·종목·세트 구성 | 구현 완료 | 웹이 부위·종목·세트 배열을 저장하고 서버가 배열 순서를 보존한다. 통합 테스트는 저장된 부위 순서와 마스터 보관 후 이력 보존을 검사한다. [편집 저장](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/programs/page.tsx#L343-L388), [서버 구성 저장](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutprogram/service/WorkoutProgramService.java#L70-L105), [마스터 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/workout/WorkoutMasterIntegrationTest.java) |
| C-1 프로그램으로 세션 시작 | 구현 완료 | 시작 전 구성 편집과 프로그램 복사 경로가 있다. 서버 테스트에서 회원당 활성 세션 1개 및 기존 세션 조회를 확인했다. [웹 시작](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/workout/page.tsx#L106-L142), [서버 시작](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/service/WorkoutSessionService.java#L50-L115), [세션 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/workoutsession/WorkoutSessionIntegrationTest.java) |
| C-2 세트 기록과 자동 휴식 | 구현 완료 | 실측 무게·횟수 저장 후 미완료 세션에 휴식 타이머를 시작한다. 일시정지·재개 시간 제외는 서버 테스트로 확인했다. 물리 모바일 기기에서의 타이머 검증은 [V1-02](BACKLOG.md#p0)로 남긴다. [웹 세트·타이머](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/workout/session/page.tsx#L501-L530), [시간 계산 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/workoutsession/entity/WorkoutSessionTest.java) |
| C-3 세션 완료 저장 | 구현 완료 | 모든 세트를 처리하면 서버가 완료 상태를 기록한다. 서버 통합 테스트가 마지막 세트 이후 완료 및 백분율을 확인한다. [세션 서비스](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/service/WorkoutSessionService.java#L123-L138), [완료 통합 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/workoutsession/WorkoutSessionIntegrationTest.java#L143-L174) |
| D-1 월간 캘린더 | 구현 완료 | 최신 월 응답만 반영하고 상세에서 복귀할 때 월을 유지한다. UTC 브라우저의 KST 월·연도 경계, 오늘 강조, 윤년을 검증했다. [일지 UI](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/src/pages/history/page.tsx), [회귀 테스트](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/tests/history-calendar.spec.ts) |
| D-2 날짜별 기록 및 세트 상세 | 구현 완료 | 월별 페이지의 201번째 기록과 모바일에서 하루 세 번째 기록을 열었다. 빈 결과와 실패 후 재시도 및 목록 필터도 검증했다. [일지 설계](../features/workout-history/TECH_SPEC.md), [회귀 테스트](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/tests/history-calendar.spec.ts) |
| M4 약관·개인정보·탈퇴 | 일부 구현 | 두 정책 페이지와 탈퇴 API/UI 경로가 있다. 서버 통합 테스트에서 탈퇴와 레거시 교차 참조의 409 롤백을 확인했다. 화면의 운영자명·문의처 자리표시자와 운영 검증은 [V1-01·02](BACKLOG.md#p0)에 남는다. [약관](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/legal/TermsPage.tsx), [개인정보](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/legal/PrivacyPolicyPage.tsx), [탈퇴 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/member/MemberWithdrawalIntegrationTest.java) |
| M5 세션 편집 확장 | 일부 구현 | 시작 전 편집과 진행 중 세트·종목 추가, 남은 종목 순서 변경은 연결됐다. 서버 종목 제거는 통합 테스트가 있으나 웹에서 호출하지 않는다. [V1-09](BACKLOG.md#p2), [웹 세션 편집](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/workout/session/page.tsx#L533-L646), [제거 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/workoutsession/WorkoutSessionIntegrationTest.java#L89-L107) |
| M5 무프로그램 시작 | 미구현 | 시작 요청에 본인 프로그램 ID가 필수다. [요청 DTO](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/dto/WorkoutSessionDto.java#L28-L34), [V1-10](BACKLOG.md#p2) |
| E-1–E-4 스쿼트 분석 | 미구현 | 현재 웹에 업로드·피드백 진입점, 서버에 분석 호출·결과 저장 계약이 없다. 엔티티와 Flyway V1–V7에도 `analysis_result`가 없다. 검증 범위는 위 두 저장소다. [AI 설계](../features/ai-coaching/TECH_SPEC.md), [데이터 모델](../architecture/DATA_MODEL.md), [AI-01·02](BACKLOG.md#p3) |

## 이전 백로그에서 해소된 항목

| 과거 문제 또는 항목 | 현행 근거 |
| --- | --- |
| `/workout/list/{id}` 수정·삭제 경로 불일치 | 웹과 서버가 `/api/workout/workouts/{id}`를 사용한다. [웹 호출](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/services/api.ts#L241-L255), [서버 컨트롤러](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workout/controller/WorkoutController.java) |
| 회원 단위 갱신 토큰과 전화·생년월일 수집 | OAuth 상태, 일회용 교환 코드와 기기별 갱신 세션으로 변경됐다. [인증 ADR](../decisions/0004-oauth-session-redesign.md), [개인정보 ADR](../decisions/0005-member-privacy-and-withdrawal.md) |
| 캘린더·시작 전 조정·건너뛰기·세션 순서 변경 부재 | 캘린더 화면과 조정·건너뛰기 코드가 있고, 남은 종목 순서 변경은 웹 PR #36으로 연결됐다. 캘린더 수정은 V1-04에서 로컬 검증했고 세션 중 종목 제거 UI는 [V1-09](BACKLOG.md#p2)에 남아 있다. [일지 화면](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/history/page.tsx), [세션 조정 이슈](https://github.com/pby1360/fitlog-v2-web/issues/8), [웹 PR #36](https://github.com/pby1360/fitlog-v2-web/pull/36) |
| 대시보드 평균 완료율 1% | 저장소 비율을 서비스에서 백분율로 한 번 변환한다. 분모 0을 제외하는 집계 정책은 [V1-12](BACKLOG.md#p2)에서 확인한다. [집계 쿼리](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/repository/WorkoutSessionRepository.java#L109-L123), [백분율 변환](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/dashboard/service/DashboardService.java#L69-L77) |
| 법적 링크·탈퇴 API·입력 검증·헬스체크 부재 | 사이트 내 링크와 탈퇴 경로, 핵심 DTO 제약, Actuator 헬스체크와 요청 ID가 추가됐다. 실제 공개 문구와 관측 운영은 P0으로 남긴다. [웹 PR #26](https://github.com/pby1360/fitlog-v2-web/pull/26), [서버 PR #28](https://github.com/pby1360/fitlog-v2-server/pull/28), [요청 ID 필터](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/global/logging/RequestIdFilter.java) |
| 공유 이미지 파일 누락·템플릿 흔적·미사용 SDK | PNG 로고를 공유 메타데이터에 연결했다. Font Awesome 플레이스홀더·Readdy DNS 조회 및 이전 미사용 SDK는 빠졌다. 공유 전용 1200×630 이미지는 후보로 남는다. [HTML](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/index.html#L28-L43), [의존성](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/package.json) |
| V1-04 캘린더 응답 경합·복귀·날짜·누락 | 코드 병합 및 로컬 검증 완료. 기준 커밋에서는 최신 월 요청만 반영하고, 선택 월과 일별 전체 기록을 열 수 있다. [변경 이력](../history/2026-11-19.md), [웹 PR #40](https://github.com/pby1360/fitlog-v2-web/pull/40) |
| 기본 검증·일지 인덱스 부재 | 서버 Gradle 테스트와 웹 린트·타입 검사 잡이 있다. Flyway V3에 회원·상태·시작 시각 인덱스가 있다. 실제 운영 배포와 쿼리 성능은 별도 확인한다. [서버 CI](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/.github/workflows/deploy.yml), [웹 CI](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/.github/workflows/deploy.yml), [V3](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration/V3__workout_session_integrity.sql#L65-L70) |

React·JPA·배포의 옛 기술 기록과 현재 구성의 차이는 [프런트엔드](../architecture/FRONTEND.md), [백엔드](../architecture/BACKEND.md), [GCP ADR](../decisions/0003-gcp-hosting.md)에 보존했다.

## 버그 및 기술 부채

| 항목 | 관측 및 분류 |
| --- | --- |
| 웹 회귀 검증 | **기술 부채.** Playwright가 추가됐다. 기존 PR 검사에는 린트·타입 검사가 있다. Playwright와 번들 빌드의 PR CI 연결은 QUAL-01에 남아 있다. [검사](BACKLOG.md#p1), [웹 테스트](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/playwright.config.ts) |
| 오래된 서버 경로 | **기술 부채.** `SecurityConfig`와 `structure.txt`에 과거 `workoutroutine`이 남아 있다. 현재 컨트롤러는 `workoutsession`이다. [TECH-01](BACKLOG.md#p2), [보안 구성](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/global/config/SecurityConfig.java#L77-L86), [구조 파일](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/structure.txt#L48) |

## 확인 필요

- **M3 배포 및 운영 환경.** 두 저장소의 배포 정의와 필수 검사를 읽었다. 조회 가능한 PR 실행 목록에서 기준 커밋의 실행 증거를 확인하지 못했다. 실제 배포 SHA, 롤백, 비용 정책 적용, 공용 시드 운영 수량과 구 인프라는 [운영 백로그](BACKLOG.md#p0)에 남긴다. [배포 구성](../operations/DEPLOYMENT.md)
- **DoD-1과 사용자 경험.** 승인된 정책 게시·문의처, 공급자 로그인·탈퇴, 실제 휴대폰의 첫 기록 3분, 가입 10명과 2주 유지 5명, 오류·이탈 관측, 개입 없이 1주 운영은 출시 판정 근거가 필요하다. [출시 기준](../product/RELEASE_CRITERIA.md), [V1-02·03](BACKLOG.md#p0), [V1-06·07](BACKLOG.md#p1)
- **제품 범위.** 개인 종목 관리, 기본 대시보드, 선택형 프로필은 구현됐다. 이를 공식 출시 범위로 확정한 승인 근거와 0세트 완료율 기준은 [V1-11·12](BACKLOG.md#p2)에서 확인한다. [제품 요구사항](../product/REQUIREMENTS.md)

## 실행 검증

- V1-02-A는 웹 브랜치에서 Playwright 21개(기존 캘린더 12개 포함)를 통과했다. 모의 API로 로그인·토큰 갱신·로그아웃, 세트 저장 실패 후 복구·휴식·운동 완료·일지, 계정 탈퇴 204·409를 확인했다. 서버 `6d1c7ba`의 내장 PostgreSQL 테스트 91개도 통과했다. 실제 OAuth와 휴대폰 검증은 V1-02에 남는다. [인증·탈퇴 테스트](https://github.com/pby1360/fitlog-v2-web/blob/a0300f1dfd3a89117db88b45a87f650a671cd9fa/tests/auth-account.spec.ts), [운동 흐름 테스트](https://github.com/pby1360/fitlog-v2-web/blob/a0300f1dfd3a89117db88b45a87f650a671cd9fa/tests/workout-flow.spec.ts), [수동 검증](../features/account/TECH_SPEC.md#실제-oauth-및-휴대폰-수동-검증-체크리스트)

- 서버는 기준 커밋 복사본에서 Java 21과 로컬 Gradle 캐시로 `./gradlew test --offline --no-daemon`을 실행했다. 17개 테스트 클래스, 91개 통과, 실패·오류·건너뛰기 0개다.
- V1-04는 Node 20.20.2에서 깨끗한 설치, 린트, 타입 검사, 빌드, Playwright 12개를 통과했다. 린트 오류는 0건이고 기존 경고 3건이 남았다. GitHub PR 검사는 통과했다.
- V1-04 병합 커밋에는 `[skip ci]`가 적용됐다. 이력 갱신 시점에는 운영 배포 성공을 확인하지 못했다. Playwright는 로컬 Chromium·모의 API 검증이며 실제 운영 데이터나 기기는 별도 검증한다. [변경 이력](../history/2026-11-19.md)

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | 최초 이관 PR #1, Obsidian `기획.md`·`TECH_SPEC.md`·`TASKS.md`·`ROADMAP.md`, 서버·웹 main과 이번 실행 검증 |
| 관련 기능 또는 Issue | A-1–E-4, M1–M6, DoD-1·2, [백로그](BACKLOG.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [기능 목록](../features/README.md), [API 목록](../api/README.md), [시스템 개요](../architecture/SYSTEM_OVERVIEW.md) |
