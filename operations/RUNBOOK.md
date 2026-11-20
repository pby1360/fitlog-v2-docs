# 운영 런북

아래는 승인된 운영 담당자가 사용할 진단 기준이다. 이번 문서 작업의 운영 접속·배포·복구 실측은 수행 대상에서 제외했다.

## 배포 또는 API 장애

| 징후 | 확인 순서 |
| --- | --- |
| 페이지는 열리지만 API만 실패 | 웹 릴리스의 API 주소, 서버 헬스체크, 응답의 `X-Request-Id` 및 같은 ID의 서버 로그, 브라우저 CORS 오류 확인 |
| 배포 잡 인증 실패 | 최근 변경된 WIF 저장소·ref 조건, 별도 배포 계정 권한, 웹 빌드용 변수 확인 |
| 도메인 연결 뒤 `Site Not Found` | Hosting 사이트 매핑과 DNS 전파를 확인한다. Cloudflare의 DNS-only 설정과 서비스 워커 캐시 영향을 분리해 확인한다. |
| 로그인 후 예전 주소로 이동 | 백엔드의 `FRONTEND_URL`과 `CORS_ALLOWED_ORIGINS`, 공급자에 등록된 백엔드 콜백, 브라우저의 웹 릴리스 확인. 여러 오리진이 있으면 배포 도구가 쉼표를 값의 일부로 전달했는지 점검한다. |
| 서버 시작 실패 또는 인증 실패 | Flyway 버전, 운영 프로필, DB 풀러/일시정지 상태, Secret Manager의 버전·개행·인코딩, 컨테이너 리소스와 Cold start를 확인한다. 확인 기록에는 비밀값 대신 버전 상태만 남긴다. |
| 429 또는 응답 시간 초과 | `Retry-After`와 요청 ID를 수집하고 Cloud Run 요청·인스턴스, PostgreSQL 연결 수, 웹의 20초 제한을 확인한다. |
| 이미지 저장 비용 증가 | Artifact Registry 보존 설정과 직전 안정 SHA 이미지 존재 여부 확인. 삭제 여부는 필요한 롤백 버전과 사용량을 확인한 뒤 운영 담당자가 판단한다. |

2026년 7~8월 개발 기록은 로컬 설정이 Docker 이미지에 포함된 뒤 자격증명을 교체하고, 이미지 검사에 로컬·백업 설정 파일을 제외하는 절차를 추가했다고 설명한다. [배포](DEPLOYMENT.md)의 현행 워크플로에는 파일 제외 및 패키징 검사가 있다.

## 롤백과 회복 확인

- 웹은 최근 호환되는 Firebase Hosting 릴리스를 확인하고 복원한다. HTML과 PWA 서비스 워커가 이전 자산만 참조하는지 점검한다.
- 서버는 이전 Cloud Run 리비전 또는 SHA 이미지가 현재 Flyway 스키마·인증 형식과 호환되는지 먼저 확인한다. 코드나 이미지를 되돌려도 적용된 스키마는 자동으로 되돌아가지 않는다.
- 비밀값 주입이 원인이면 기존 설정을 확인하고 승인 절차에 따라 참조 버전을 복구한다. 값은 티켓이나 로그에 남기지 않는다.
- 복구 후 헬스체크와 핵심 흐름을 확인하고, 증상·발생 시각·요청 ID·영향·관련 커밋·검증 결과를 남긴다. 구 인프라는 실제 가용 상태의 확인을 거친다.

### OPS-01 롤백 검증

1. **Web.** 현재 live와 직전 안정 릴리스의 버전 ID·시각·사이트·Git 근거를 확인한다. 승인된 훈련은 격리 사이트에서 먼저 진행한다. 실제 장애 대응이 별도로 승인되면 Firebase Hosting Release history에서 호환되는 버전을 선택한다. PWA 업데이트 전후의 HTML·서비스 워커·해시 자산과 API 주소, SPA 직접 진입, 캘린더 월 변경·상세 복귀를 확인한다.
2. **Server.** 현재 트래픽 분배와 롤백 후보 리비전·이미지 digest를 기록한다. Cloud Run에 후보가 남아 있는지, 이미지가 정리 정책의 삭제 대상인지 확인한다. 승인된 담당자는 스키마·인증 호환 검토를 마친 뒤 후보 리비전으로 트래픽을 전환한다. 후보 리비전이 없으면 보존된 digest로 새 리비전이 필요하므로 별도 승인 범위에 포함한다. 실패 시 미리 기록한 원래 트래픽 분배를 복원한다.
3. **Flyway.** 마지막으로 확인한 서버 배포 SHA와 최신 `main`의 V1–V7 마이그레이션은 동일하다. 더 이전 후보는 V4 인증 전환과 V7 개인정보 컬럼 제거 이후의 스키마를 사용할 수 있는지 확인한다. 승인된 운영 담당자가 적용 migration 버전·checksum 메타데이터만 제공하고, 데이터나 자격증명 없이 그 버전을 재현한 격리 DB에서 후보 이미지의 시작·인증·세션 기능을 검증한다. Cloud Run 트래픽 전환은 DB 스키마를 되돌리지 않는다.
4. **훈련 기록.** 대상·영향 범위·합격 기준·원상 복구 조건을 승인 요청에 남긴다. 리비전 및 릴리스 ID, 시작/종료 시각(KST), 검증 시나리오와 결과를 기록한다. Server `00005`는 격리 복구 기준으로 검증됐다. Web 안정 복구 릴리스와 운영 트래픽 롤백 훈련은 `UNVERIFIED`다. [배포 증거](DEPLOYMENT.md#ops-01-배포-증거) · [Cloud Run 트래픽 관리](https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration)

### Server 이미지 복구 기준

- `00003`과 `00004`(`98d6c98`)는 현재 V7 스키마의 롤백 대상에서 제외한다. 운영 담당자의 격리 DB 재현에서 기존 Member 매핑이 요구하는 `refresh_token`(V4 제거), `phone`·`birth_date`(V7 제거)가 없었고 SQLSTATE `42703`이 발생했다. 이전 소스의 Hibernate는 `ddl-auto: validate`다. 운영 트래픽 전환, 과거 컨테이너 기동 및 전체 사용자 흐름은 수행되지 않았다. [이전 소스](https://github.com/pby1360/fitlog-v2-server/commit/98d6c98b26f2511285d5eeb3f38be731e87ca794) · [V4](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration/V4__auth_redesign.sql) · [V7](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration/V7__privacy_minimize_member_data.sql)
- **검증된 Server 복구 기준.** `fitlog-server-00005-8tn` 이미지의 불변 digest `sha256:2eb78030502b7f98e4e73def7283a4f2d13573a4232d7fe320007499cf169729`를 기준으로 삼는다. [격리 검증 결과](#00005-격리-검증-결과) · [운영 배포 증거](DEPLOYMENT.md#ops-01-배포-증거)

#### 00005 격리 검증 결과

2026-11-20 운영 담당자의 Google Cloud Shell 검증 결과다. GCP 프로젝트 `fitlog-505315`의 운영 이미지 원본을 격리 Docker 네트워크에서 Java 21.0.12.1, Spring Boot 3.5.7, PostgreSQL 17.6으로 실행했다. 운영 DB와 실제 OAuth는 사용하지 않았다.

| 단계 | 판정과 증거 |
| --- | --- |
| 현재 운영 정상 | `VERIFIED`. 운영 담당자 증거에서 Ready, 트래픽 100%, HTTP 200 / UP. [운영 증거](DEPLOYMENT.md#ops-01-배포-증거) |
| PostgreSQL 17.6·소스 호환성 | `VERIFIED`. `1154a06`의 별도 소스 복사본에서 PostgreSQL 17.6을 실행했다. V1 DDL로 기존 스키마를 만들고 `baseline-on-migrate=true` 및 baseline version 1을 주입했다. V1 BASELINE/NULL, V2–V7 성공, Hibernate validate, Flyway validate, 이전 컬럼 3개 부재를 확인했다. `./gradlew test --no-daemon --offline` 92개 통과. 기존 운동·인증 통합 검사와 기준선 전용 검사 1개를 포함한다. |
| 로컬 V2–V7 체크섬 | 순서대로 `-1233443391`, `-1067780021`, `-1750642191`, `-1017112054`, `-1135251280`, `871620929`. 로컬 Flyway가 소스와 대조했다. 운영 담당자가 자신의 운영 기록과 소스의 일치를 보고했으며 이 작업은 운영 DB를 직접 조회하지 않았다. |
| 실제 운영 digest 격리 재기동 | `VERIFIED`. 운영 이미지를 Pull하고 `RepoDigests` 일치를 확인했다. V1 초기 스키마 생성, Flyway V1 `BASELINE`과 V2–V7 적용, 기존 증거와 V2–V7 체크섬 일치, Hibernate 초기화, Spring Boot 기동, Actuator Health `UP`을 확인했다. |
| 핵심 운동 API | `VERIFIED`. 미인증 요청 HTTP 401, HS512 테스트 토큰 인증, 운동 부위 7개와 종목 23개 조회, 운동 프로그램 생성·조회, 운동 세션 시작, 세트 완료와 자동 종료를 확인했다. 완료 상태에서 중복 요청이 성공했고, 일지 목록과 상세의 `actualWeight=42.5` 및 `actualReps=12`를 확인했다. |
| 실제 Google/Kakao OAuth·운영 트래픽 롤백 훈련 | `UNVERIFIED`. 실제 공급자 로그인 및 운영 트래픽 전환 훈련은 수행하지 않았다. |
| 이미지 장기 보존 | 사용자 결정으로 보류. 운영 정리 정책에 장기 보존 규칙은 적용되지 않았다. [보존 승인안](DEPLOYMENT.md#안정-이미지-보존-승인안) |

**새 복구 기준의 재검증.** 후보가 바뀌면 전체 digest로 Pull하고 `RepoDigests`를 대조한다. 격리 PostgreSQL 17.6에 V1 스키마와 V1 `BASELINE`, V2–V7을 재현한다. 테스트 설정으로만 이미지 기동·Health·Flyway·Hibernate와 인증·운동 API를 확인한다. 대상 digest, 스키마, 필수 시나리오가 일치할 때 기준을 교체한다. 종료 시 격리 테스트 자원만 정리한다.

신규 Cloud Run 시험 서비스가 필요할 경우 비용·격리 네트워크와 서비스 계정·운영 DB 연결 차단·삭제 기준을 따로 승인받는다. 운영 장애 대응 또는 훈련에서 트래픽 전환을 수행할 때는 별도 승인과 현재 digest 보존 확인이 필요하다.

### Flyway 이력 증빙

운영 담당자가 승인된 읽기 전용 세션으로 Flyway 이력 테이블의 메타데이터만 확인한다. 필요한 앱 DB 권한은 대상 스키마 `USAGE`와 이력 테이블 `SELECT`다. 배포 설정에서 별도 스키마를 사용한다면 아래 `public`을 해당 스키마로 바꾼다. DB 접속 문자열이나 회원 데이터는 증빙에 포함하지 않는다.

```sql
BEGIN TRANSACTION READ ONLY;
SELECT installed_rank, version, checksum, success
FROM public.flyway_schema_history
WHERE version IS NOT NULL
ORDER BY installed_rank;
ROLLBACK;
```

성공 행의 마지막 버전과 각 체크섬을 후보 이미지의 마이그레이션과 비교한다. 현재 서버 소스의 마지막 버전은 V7이다. 운영 담당자의 실제 조회에서 V7 적용과 V2–V7 체크섬 일치가 보고됐다. 격리 검증은 `BASELINE` 행을 포함한 운영 적용 방식을 재현한다. V7이 제거한 회원 컬럼 값은 이미지 롤백으로 복원되지 않는다. 운영 스키마 버전을 재현한 격리 DB에서 이전 이미지의 기동·스키마 검증·OAuth 세션·운동 기록 읽기/쓰기를 통과해야 후보를 안정 리비전으로 판정한다. [V7 마이그레이션](https://github.com/pby1360/fitlog-v2-server/blob/6d1c7ba7f227b3b6087e2033b1e74213f25fa708/src/main/resources/db/migration/V7__privacy_minimize_member_data.sql)

운영 지표와 사용자 흐름의 관측 상태는 [백로그](../status/BACKLOG.md)에서 추적한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `배포.md`, `TASKS.md` P1의 이관·장애 메모, `ROADMAP.md` M3–M4 및 서버·웹 main, 2026-11-20 운영 담당자 제공 이미지 복구 검증 결과 |
| 관련 기능 또는 Issue | M2–M4, DoD-1 |
| 최종 검증일 | 2026-11-20 |
| 관련 설계 | [배포](DEPLOYMENT.md), [API 오류 계약](../api/README.md), [데이터 모델](../architecture/DATA_MODEL.md) |
