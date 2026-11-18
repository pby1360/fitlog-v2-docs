# 현재 구현 및 검증 상태

2026-11-18 기준 [서버·웹 main 커밋](../architecture/SYSTEM_OVERVIEW.md)을 확인했다. 이 표의 구현 완료는 해당 범위의 코드 경로를 확인했다는 뜻이다. 테스트는 아래 실행 범위를 따른다. 출시 판정은 [DoD](../product/RELEASE_CRITERIA.md)의 별도 증거가 필요하다.

| 상태 | 판정 기준 |
| --- | --- |
| 구현 완료 및 코드 검증 | 기준 커밋에 해당 동작의 경로가 있고 코드로 확인했다. |
| 일부 구현 | 일부 흐름만 연결됐거나 수용 조건에 차이가 있다. |
| 문서에만 존재하는 계획 | 원본에 목표나 설계만 기록돼 있다. |
| 미구현 | 구체적인 기능을 기준 커밋의 대상 코드에서 확인할 수 없다. |
| 추가 확인 필요 | 운영, 제품 승인, 실행 결과 등 확인 근거가 더 필요하다. |

## 기능별 판정

| 범위 | 판정 | 기준 커밋에서 확인한 내용 |
| --- | --- | --- |
| A-1–A-2 로그인·기본 프로필 | 구현 완료 및 코드 검증 | 두 OAuth 공급자 경로, 인증 코드 교환, 닉네임 조회·수정. 개인정보 범위는 [계정 설계](../features/account/TECH_SPEC.md)에 기록했다. |
| B-1 시드 | 일부 구현 | 공용 부위 7개와 종목 23개를 시드한다. 기획은 50~100개, M5는 80개를 목표로 했다. 현재 운영 DB 종목 수는 별도 확인이 필요하다. [시드 SQL](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration/V2__seed_master_data.sql) |
| B-2–B-3 프로그램 | 구현 완료 및 코드 검증 | 목록·생성·수정·소프트 삭제, 부위별 종목과 세트 구성, 정렬. 개인 종목도 구현돼 있다. [프로그램 설계](../features/workout-program/TECH_SPEC.md) |
| C-1–C-3 세션 | 구현 완료 및 코드 검증 | 프로그램 기반 시작, 기록·타이머·일시정지·재개·건너뛰기·종료, 추가 세트·종목과 세션 순서 변경. [세션 설계](../features/workout-session/TECH_SPEC.md) |
| 세션 중 제거·즉석 운동 | 일부 구현 | 서버에 제거가 있고 웹에는 삭제 호출이 없다. 웹은 시작 전 프로그램에 기반한 편집을 제공한다. |
| 완전한 무프로그램 시작 | 미구현 | 시작 DTO와 서버 서비스가 사용자 소유 프로그램을 요구한다. [세션 설계](../features/workout-session/TECH_SPEC.md) |
| D-1–D-2 일지 및 대시보드 | 구현 완료 및 코드 검증 | 월간 캘린더, 기간 목록과 상세, KST 경계, 평균 완료율. [일지 설계](../features/workout-history/TECH_SPEC.md) |
| 약관·개인정보 및 탈퇴 | 구현 완료 및 코드 검증 | 법적 페이지·라우트·푸터 링크, 회원 탈퇴 UI와 DELETE API. 실제 게시·문의처와 배포 후 흐름은 추가 확인 필요. |
| E-1–E-4 AI | 문서에만 존재하는 계획 | 분석·업로드 API, 저장 컬럼, FE 업로드 및 피드백 UI 미구현. [AI 설계](../features/ai-coaching/TECH_SPEC.md) |
| M3 배포, DoD-1 출시 | 추가 확인 필요 | CI와 배포 정의는 양쪽 `main`에 있다. 실제 배포 성공, 운영 설정, 가입·유지·관측·무중단 기준은 이 작업에서 확인 범위 밖이었다. |

## 이전 문서와의 차이

| 원본 기록 | 최신 근거와 해석 |
| --- | --- |
| 7월 `TECH_SPEC`의 React 18·Router 6, JPA `ddl-auto: update`, Vercel·EC2 | React 19·Router 7, Flyway V1–V7 + `validate`, Firebase Hosting·Cloud Run 워크플로. [프런트](../architecture/FRONTEND.md), [백엔드](../architecture/BACKEND.md), [배포](../operations/DEPLOYMENT.md) |
| 옛 `/workout/list/{id}` 수정·삭제 경로 불일치 | 두 저장소가 `/api/workout/workouts/{workoutId}`를 사용한다. [웹 API](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/services/api.ts), [서버 계약](../api/README.md) |
| `TECH_SPEC`의 이전 JWT 콜백·회원 단위 토큰, `dev` 프로필 확장 | V4의 OAuth 상태·교환 코드와 기기별 갱신 세션, `main`의 프로필 수정 및 V7의 전화·생일 제거. [인증 ADR](../decisions/0004-oauth-session-redesign.md), [탈퇴 ADR](../decisions/0005-member-privacy-and-withdrawal.md) |
| 4월·7월 자료의 캘린더 미확인 또는 UX 미완 | 8월 정정 및 현재 코드에서 월간 캘린더 확인. UX는 별도 작업이다. [일지 화면](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/history/page.tsx) |
| 8월 M4의 정책 링크, 탈퇴 API, 입력 검증 부재 | 라우트와 링크, 트랜잭션 탈퇴, `@Valid`와 DTO 제약이 있다. [웹 PR #26](https://github.com/pby1360/fitlog-v2-web/pull/26), [서버 PR #28](https://github.com/pby1360/fitlog-v2-server/pull/28) |
| 8월 대시보드 평균 완료율 1% | 저장소는 0~1 비율을 반환하고 서비스가 0~100으로 한 번 변환한다. 0세트 제외 정책은 확인 대상이다. [DashboardService](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/dashboard/service/DashboardService.java) |
| 8월 M5 세션 순서 변경 웹 미연동 | 웹 PR #36에서 연결했다. [웹 PR #36](https://github.com/pby1360/fitlog-v2-web/pull/36) |
| 8월 공유 이미지 파일 누락·템플릿 흔적·미사용 의존성 | `og:image`는 실제 PNG 로고를 사용한다. 1200×630 전용 이미지는 TODO다. Font Awesome 플레이스홀더, Readdy DNS 조회 및 세 SDK는 확인되지 않았다. [HTML](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/index.html), [의존성](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/package.json) |
| 8월 CI 실행 대기·서버 테스트 15개·헬스체크 부재 | 양쪽 워크플로 PR 검사가 있으며, 서버 테스트 91개 통과 및 Actuator·요청 ID·제한 확인. 웹 PR 잡은 린트·타입 검사를 하고 빌드는 배포 잡에서 실행한다. [배포](../operations/DEPLOYMENT.md) |
| `analysis_result` 예약, 일지 인덱스 부재 | 현재 Flyway에 AI 컬럼은 없고, 일지 회원·상태·시각 복합 인덱스는 V3에서 확인된다. [데이터 모델](../architecture/DATA_MODEL.md) |

## 검증 수행

- 서버는 코드 복사본과 로컬 Gradle 캐시에서 `./gradlew test --offline --no-daemon`을 실행했다. Java 21, 17개 테스트 클래스, 테스트 91개 중 실패·오류·건너뛰기 0개다.
- 웹은 코드 복사본에서 Node 24로 `npm ci`, `npm run lint`, `npm run typecheck`, `npm run build`를 실행했다. 빌드는 로컬용 API 주소를 사용했다. 린트는 오류 0개와 React 훅 의존성 경고 4개를 반환했다. GitHub 워크플로의 Node는 20이다.
- 실제 공급자 인증, 브라우저 E2E, 운영 접속, 운영 스키마, 운영 배포 및 GitHub Actions 실행 상태는 추가 검증 범위로 남긴다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `기획.md`, `TECH_SPEC.md`, `TASKS.md`, `ROADMAP.md`, `fitlog-v2-MoC.md`, `history/` 및 서버·웹 main |
| 관련 기능 또는 Issue | A-1–E-4, M1–M6, DoD-1·2 |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [백로그](BACKLOG.md), [API 목록](../api/README.md), [시스템 개요](../architecture/SYSTEM_OVERVIEW.md) |
