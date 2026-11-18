# 프런트엔드 구조

## 스택과 진입점

React 19, React Router 7, TypeScript 5.8, Vite 7, Tailwind CSS 3.4, PostCSS, i18next, Recharts를 사용한다. React SWC 플러그인과 `vite-plugin-pwa`를 사용한다. `main.tsx`가 앱을 마운트하고, `App.tsx`는 `ThemeProvider`, `BrowserRouter` 및 `navigationService` 등록을 관리한다. 페이지는 `router/config.tsx`에서 lazy import를 사용한다. [빌드 구성](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/package.json), [Vite 설정](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/vite.config.ts), [라우팅](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/router/config.tsx)

| 경로 | 화면 및 기능 |
| --- | --- |
| `/` | 홈과 로그인 진입, 개인정보처리방침·약관 링크 |
| `/dashboard` | 통계 카드, 주간 차트, 최근 운동 |
| `/programs` | 프로그램 목록·편집·개인 종목 관리 |
| `/workout`, `/workout/session` | 프로그램 선택·시작 전 구성, 세션 진행·타이머 |
| `/history`, `/history/:id` | 기간 목록·월간 캘린더, 일지 상세 |
| `/profile` | 프로필 조회·수정과 탈퇴 |
| `/privacy`, `/terms` | 개인정보처리방침, 이용약관 |
| `/auth/callback`, `*` | OAuth 코드 교환 진입, 없는 경로 안내 |

## 컴포넌트와 상태

`components/base`에 `Button`, `Card`, `Input`, `components/feature`에 `Header`와 `LoginModal`이 있다. 프로그램 페이지 내부의 `ManageWorkoutsView`가 마스터를 관리한다. 페이지별 폼·조회·타이머 상태는 React 훅으로 관리한다. 테마는 `ThemeContext`와 `localStorage`를 사용한다. 브라우저의 최초 토큰 유효성 확인은 백그라운드에서 동작한다.

`services/api.ts`가 `VITE_API_BASE_URL`과 `/api`를 결합해 요청한다. 요청 시간 제한은 20초이며 요청 ID와 공통 오류 메시지를 처리한다. 401이면 동시 갱신을 합치고 한 번 재시도한다. 인증 실패가 지속되면 토큰을 정리하고 홈으로 이동한다. 인증 토큰과 표시용 프로필은 `localStorage`에 저장한다. [API 요청 코드](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/services/api.ts), [인증 설계](../features/account/TECH_SPEC.md)

## 검증과 배포

`npm ci`, `npm run lint`, `npm run typecheck`, `npm run build`를 사용한다. 빌드는 `tsc -b`를 실행한 뒤 Vite가 `out/`을 생성한다. `npm test`로 Playwright의 Chromium 회귀 테스트를 실행한다. 처음 실행할 때 `npx playwright install chromium`으로 브라우저를 준비한다. V1-04에서는 로컬 Vite와 모의 API를 사용했고 기존 PR 워크플로의 검사 범위는 유지됐다. [테스트 설정](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/playwright.config.ts) 배포 및 SPA·PWA 캐시는 [배포](../operations/DEPLOYMENT.md)에서 관리한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `TECH_SPEC.md` §3 및 웹 main |
| 관련 기능 또는 Issue | [계정](../features/account/PRD.md), [운동 프로그램](../features/workout-program/PRD.md), [세션](../features/workout-session/PRD.md), [일지](../features/workout-history/PRD.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [시스템 개요](SYSTEM_OVERVIEW.md), [API 목록](../api/README.md) |
