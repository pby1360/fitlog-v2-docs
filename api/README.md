# API 목록

기준은 [서버 커밋](../architecture/SYSTEM_OVERVIEW.md)이다. 업무 API는 `/api` 아래에 있고 운동·회원·통계 요청에는 `Authorization: Bearer <access-token>`을 사용한다. OAuth2 개시와 공급자 콜백은 Spring Security에서 처리한다. 열린 토큰 관련 경로는 요청의 일회용 코드 또는 갱신 토큰으로 검증한다.

## 인증 및 회원

| 메서드 | 경로 | 요청 및 성공 응답 |
| --- | --- | --- |
| POST | `/api/auth/token` | `code` 교환 → 토큰 쌍, `imageUrl`, `provider` |
| POST | `/api/auth/refresh` | `refreshToken` → 회전한 토큰 쌍 |
| POST | `/api/auth/logout` | `refreshToken`으로 세션 폐기 → 204 |
| GET | `/api/members/me` | 프로필 및 운동 통계 → 200 |
| PATCH | `/api/members/me` | `nickname`, `height`, `weight`, `goal`, `experience` → 갱신 프로필 |
| DELETE | `/api/members/me` | 회원 및 관련 데이터 파기 → 204 |

[AuthController](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/auth/controller/AuthController.java), [MemberController](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/member/controller/MemberController.java)

## 운동 종목 및 프로그램

| 메서드 | 경로 | 요청 및 성공 응답 |
| --- | --- | --- |
| GET | `/api/workout/parts` | 공용·본인 부위 목록 |
| POST | `/api/workout/parts` | `name` → 200 빈 본문 |
| PUT | `/api/workout/parts/{workoutPartId}` | `name` → 200 빈 본문 |
| DELETE | `/api/workout/parts/{workoutPartId}` | 개인 부위 삭제 또는 보관 → 200 빈 본문 |
| GET | `/api/workout/workouts` | 공용·본인 종목 목록 |
| POST | `/api/workout/workouts` | `name`, `workoutPartId` → 200 빈 본문 |
| PUT | `/api/workout/workouts/{workoutId}` | `name`, `workoutPartId` → 200 빈 본문 |
| DELETE | `/api/workout/workouts/{workoutId}` | 개인 종목 삭제 또는 보관 → 200 빈 본문 |
| GET | `/api/workout-programs` | 본인 프로그램 목록 |
| POST | `/api/workout-programs` | 프로그램 구성 → 200 빈 본문 |
| PUT | `/api/workout-programs/{programId}` | 프로그램 전체 구성 갱신 → 200 빈 본문 |
| DELETE | `/api/workout-programs/{programId}` | 프로그램 소프트 삭제 → 200 빈 본문 |

프로그램 요청은 `name`, `description`, `parts[]`를 가진다. 각 부위에는 `workoutPartId`와 `exercises[]`, 각 종목에는 `workoutId`와 `sets[]`가 있다. 세트 필드는 `setNumber`, `weight`, `reps`, `restTime`, `memo`다. 부위와 운동은 요청 배열 순서로 저장한다. [WorkoutController](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workout/controller/WorkoutController.java), [WorkoutProgramController](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutprogram/controller/WorkoutProgramController.java), [WorkoutProgramDto](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutprogram/WorkoutProgramDto.java)

## 운동 세션·일지 및 대시보드

| 메서드 | 경로 | 요청 및 성공 응답 |
| --- | --- | --- |
| POST | `/api/workout-sessions` | 필수 `workoutProgramId`, 선택 `customExercises[]` → 세션 |
| GET | `/api/workout-sessions/latest` | 활성 세션 → 200, 없으면 204 |
| PATCH | `/api/workout-sessions/{sessionId}/complete-set` | 종목·세트 ID, 실측 무게·횟수·메모 → 세션 |
| PATCH | `/api/workout-sessions/{sessionId}/pause` | 일시정지 → 세션 |
| PATCH | `/api/workout-sessions/{sessionId}/resume` | 재개 → 세션 |
| PATCH | `/api/workout-sessions/{sessionId}/skip-exercise` | 세션 종목 ID와 `skipped` → 세션 |
| PATCH | `/api/workout-sessions/{sessionId}/reorder-exercises` | `exercises[]`의 세션 종목 ID와 순서 → 세션 |
| POST | `/api/workout-sessions/{sessionId}/exercises` | 마스터 종목 ID, 순서, 세트 구성 → 세션 |
| DELETE | `/api/workout-sessions/{sessionId}/exercises/{exerciseId}` | 세션 종목 제거 → 세션 |
| PATCH | `/api/workout-sessions/{sessionId}/exercises/{exerciseId}/start` | 종목 시작 처리 → 세션 |
| POST | `/api/workout-sessions/{sessionId}/exercises/{workoutSessionExerciseId}/sets` | 목표 무게·횟수·휴식·메모 → 세션 |
| PATCH | `/api/workout-sessions/{sessionId}/end` | 종료 상태 `COMPLETED` 또는 `CANCELLED` → 세션 |
| GET | `/api/workout-sessions/logs` | `page`, `size`, `sort`, 선택 `startDate`·`endDate` → 일지 페이지와 통계 |
| GET | `/api/workout-sessions/logs/{sessionId}` | 세트 기록을 담은 일지 상세 |
| GET | `/api/dashboard/stats` | 주간·월간·부위별 통계, 연속일, 평균 완료율, 최근 운동 |

날짜 입력은 `YYYY-MM-DD`이고 조회 날짜 기준은 한국 시간이다. 목록 기본값은 페이지 크기 10과 `startTime,desc`다. 서버는 세션 종료 시각과 추가 세트 번호를 결정한다. [WorkoutSessionController](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/controller/WorkoutSessionController.java), [WorkoutSessionDto](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/dto/WorkoutSessionDto.java), [DashboardController](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/dashboard/controller/DashboardController.java)

## 오류와 운영 응답

업무 API 오류 본문은 `code`, `message`, `requestId`를 사용한다. 400은 요청·입력 검증, 401은 미인증, 403은 금지, 404는 대상 없음, 409는 충돌, 429는 요청 제한, 500은 내부 오류다. 응답의 `X-Request-Id`로 로그를 찾고 제한 응답에서 `Retry-After`를 확인한다. 헬스체크 경로는 `/actuator/health`다. [오류 코드](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/global/exception/ErrorCode.java), [런북](../operations/RUNBOOK.md)

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `TECH_SPEC.md` §§3–4 및 서버·웹 main |
| 관련 기능 또는 Issue | [전체 기능](../features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [백엔드](../architecture/BACKEND.md), [데이터 모델](../architecture/DATA_MODEL.md), [프런트엔드](../architecture/FRONTEND.md) |
