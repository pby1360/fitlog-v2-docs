# 백엔드 구조

## 스택과 패키지

Java 21, Spring Boot 3.5.7, Gradle Wrapper 8.14.3, Spring Data JPA(Hibernate), Spring Security OAuth2 Client, Bean Validation, Actuator, Flyway, PostgreSQL, JJWT 0.11.5를 사용한다. [Gradle 구성](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/build.gradle), [Wrapper](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/gradle/wrapper/gradle-wrapper.properties)

`com.fitlog.fitlogv2server` 아래에서 기능별로 패키지를 구성한다.

| 영역 | 책임 |
| --- | --- |
| `domain.auth` | 교환 코드, 로그인 세션, 갱신·로그아웃 |
| `domain.member` | 회원 프로필 및 탈퇴 |
| `domain.workout` | 공용·개인 운동 부위와 종목 |
| `domain.workoutprogram` | 운동 프로그램과 템플릿 세트 |
| `domain.workoutsession` | 진행·일시정지·기록·완료·일지 |
| `domain.dashboard` | 주간·월간·부위별 통계, 연속일, 완료율 |
| `global` | 구성·시간대·검증 한계·보안·예외·요청 ID·요청 제한 |

컨트롤러가 인증 주체와 요청 DTO를 서비스 또는 파사드에 넘긴다. 도메인 서비스가 트랜잭션 및 규칙을 관리한다. JPA 저장소와 인증·탈퇴용 JDBC가 PostgreSQL에 접근한다. Flyway가 스키마를 관리하고 JPA는 `ddl-auto: validate`로 확인한다. 운영 프로필은 기존 스키마를 V1로 기준화할 수 있고 HikariCP 풀 상한은 5다. 연결 값은 환경 설정으로 주입한다. [마이그레이션](https://github.com/pby1360/fitlog-v2-server/tree/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration)

## 보안과 오류

JWT 요청은 세션 없이 Spring Security에서 인증한다. OAuth2 인가 요청 상태는 JDBC 저장소를 사용한다. CORS 허용 목록은 환경 설정에서 주입한다. 인증과 쓰기 요청에 인스턴스별 제한을 적용한다. Actuator의 헬스체크와 요청 ID가 있다. 오류 응답은 [API 목록](../api/README.md)을 따른다. 7월 Tech Spec에 기록된 `/api/workoutroutine/**`의 과거 매처는 현재도 `SecurityConfig`에 남아 있다. 대응 컨트롤러는 `workoutsession`의 `/api/workout-sessions`다. [SecurityConfig](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/global/config/SecurityConfig.java)

## 테스트와 자동화

Gradle의 JUnit Platform에서 단위 및 Spring 통합 테스트를 실행한다. 통합 테스트는 임베디드 PostgreSQL 17.6과 Flyway를 사용한다. 인증·탈퇴·마스터 소유권·세션 상태와 동시성·KST 경계·통계·오류 계약·요청 제한의 테스트 코드가 있다. [테스트 목록](https://github.com/pby1360/fitlog-v2-server/tree/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test), [실행 결과](../status/CURRENT_STATUS.md)

워크플로 PR 경로에서는 테스트만 수행한다. Cloud Run용 이미지와 배포 경로는 [배포](../operations/DEPLOYMENT.md)를 따른다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `TECH_SPEC.md` §4, `TASKS.md` 및 서버 main |
| 관련 기능 또는 Issue | [전체 기능](../features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [데이터 모델](DATA_MODEL.md), [API 목록](../api/README.md), [인증 설계](../features/account/TECH_SPEC.md) |
