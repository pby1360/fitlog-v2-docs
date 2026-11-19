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
4. **훈련 기록.** 대상·영향 범위·합격 기준·원상 복구 조건을 승인 요청에 남긴다. 리비전 및 릴리스 ID, 시작/종료 시각(KST), 검증 시나리오와 결과를 기록한다. Web과 Server 모두 현재 안정 대상과 실제 롤백 실행이 `UNVERIFIED`다. [배포 증거](DEPLOYMENT.md#ops-01-배포-증거) · [Cloud Run 트래픽 관리](https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration)

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

성공 행의 마지막 버전과 각 체크섬을 후보 이미지의 마이그레이션과 비교한다. 현재 서버 소스의 마지막 버전은 V7이다. 실제 운영 적용 버전은 이력 조회 전까지 `UNVERIFIED`다. V7이 제거한 회원 컬럼 값은 이미지 롤백으로 복원되지 않는다. 운영 스키마 버전을 재현한 격리 DB에서 이전 이미지의 기동·스키마 검증·OAuth 세션·운동 기록 읽기/쓰기를 통과해야 후보를 안정 리비전으로 판정한다. [V7 마이그레이션](https://github.com/pby1360/fitlog-v2-server/blob/6d1c7ba7f227b3b6087e2033b1e74213f25fa708/src/main/resources/db/migration/V7__privacy_minimize_member_data.sql)

운영 지표와 사용자 흐름의 관측 상태는 [백로그](../status/BACKLOG.md)에서 추적한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `배포.md`, `TASKS.md` P1의 이관·장애 메모, `ROADMAP.md` M3–M4 및 서버·웹 main |
| 관련 기능 또는 Issue | M2–M4, DoD-1 |
| 최종 검증일 | 2026-11-20 |
| 관련 설계 | [배포](DEPLOYMENT.md), [API 오류 계약](../api/README.md), [데이터 모델](../architecture/DATA_MODEL.md) |
