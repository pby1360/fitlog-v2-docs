# 배포 구성과 절차

이 문서는 GitHub Actions의 배포 정책과 승인된 운영 담당자의 절차를 기록한다. 에이전트는 운영 환경에 접근하거나 배포를 직접 실행하지 않는다. [문서 관리 규칙](../AGENTS.md)

## CI와 자동 배포 정책

현행 정책은 웹·서버의 워크플로 변경 PR #42부터 적용됐다. [웹 #42](https://github.com/pby1360/fitlog-v2-web/pull/42) · [서버 #42](https://github.com/pby1360/fitlog-v2-server/pull/42) 코드 PR은 사용자가 승인한 뒤 수동으로 병합한다. 기능 변경·버그 수정의 커밋 또는 병합 메시지에는 `[skip ci]` 등 CI 생략 문구를 넣지 않는다. CI의 필수 잡은 PR의 파일 유형과 무관하게 보고되며, 운영 배포는 승인된 변경이 `main`에 반영돼 필수 검사를 통과하면 GitHub Actions가 수행한다.

| 변경 유형 | PR 및 `main` 검사 | 자동 운영 배포 |
| --- | --- | --- |
| Markdown, `AGENTS.md`, `.agents/`, Docs 동기화 워크플로만 변경 | 웹 설치·린트·타입 검사, 서버 Gradle 테스트 | 생략 |
| 테스트·테스트 설정만 변경 | 웹 빌드·Playwright까지 검사, 서버 Gradle 테스트 | 생략 |
| 기능·UI·버그 수정·런타임 리팩터링·서비스 빌드 입력 | 전체 검사. 문서가 함께 바뀌어도 기능 변경으로 분류 | `main` 반영과 필수 검사 성공 후 배포 |
| 승인된 Flyway 마이그레이션 | Gradle 테스트. PR에서 기존 스키마 호환성과 롤백 영향 검토 | 필수 검사 통과 후 서버 배포 |
| 배포 워크플로·운영 설정·인증·인프라·분류가 불분명한 경로 | 전체 검사와 검토 대상 경고 | 자동 차단. 영향과 적용 방법을 승인된 담당자가 검토 |
| 변경 이력을 조회 또는 검증할 수 없음 | 실패로 보고 | 차단 |

PR은 두 브랜치의 공통 조상부터 PR head까지, `main` Push는 이전 `main`부터 새 커밋까지 비교한다. 여러 커밋 및 머지 커밋을 포함한 Push 전체를 비교하고, 이동이나 이름 변경은 양쪽 경로를 평가한다. 검토 대상 파일이 포함되면 기능 파일과 함께 변경돼도 자동 배포를 보류한다. PR을 열거나 갱신하는 이벤트에서는 운영 배포를 실행하지 않는다. Docs 자동 병합에 쓰이는 `Docs-Sync-Kind`, `Docs-Sync-PR`, `Docs-Sync-Head`와 동기화 이벤트는 기존 계약을 따른다. [코드·문서 동기화](DOCS_SYNC.md)

배포 잡은 저장소별로 한 번에 하나씩 실행한다. 시작할 때와 게시 직전 원격 `main` SHA를 다시 확인하고, 더 최신 커밋이 있거나 조회가 실패하면 해당 실행으로 배포하지 않는다. 그 사이 문서 전용 변경이 들어오면 새 실행도 자동 배포 대상이 아니므로, 마지막 배포 SHA와 현행 런타임 차이를 확인해 필요 시 승인된 운영 담당자가 최신 `main`의 워크플로를 실행한다. 수동 실행에서 `confirm_deploy`를 명시적으로 활성화하며 같은 필수 검사와 최신 SHA 확인을 적용한다.

## 프런트엔드

[웹 워크플로](https://github.com/pby1360/fitlog-v2-web/blob/main/.github/workflows/deploy.yml)는 Node 20에서 `npm ci`, 린트, 타입 검사를 실행한다. 기능·빌드·테스트 변경과 배포 검토 대상 변경은 로컬 API 주소로 번들을 빌드하고 Chromium·시스템 의존성을 설치해 Playwright를 실행한다. 배포 잡에서는 운영 `VITE_API_BASE_URL`을 빌드에 주입한다. `out/`과 API 주소가 들어간 번들을 점검한 뒤 기존 Google Workload Identity Federation(WIF) 설정으로 인증해 Firebase Hosting에 릴리스를 만든다.

V1-04의 병합 `6f8cc4c`에는 당시 CI 생략 표시가 있었다. 해당 커밋은 아래에서 확인한 마지막 성공 배포보다 이후의 변경이다. 운영 Hosting 릴리스의 현재 V1-04 포함 여부는 사이트 릴리스와 대조한다. [V1-04 병합](https://github.com/pby1360/fitlog-v2-web/commit/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1)

[Vite](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/vite.config.ts)와 [Firebase Hosting](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/firebase.json)의 출력 경로는 `out`이다. 직접 진입 경로는 `/index.html`로 리라이트한다. 해시 자산은 장기 캐시하고 HTML 및 서비스 워커는 캐시를 제한한다. 생성된 소스맵은 Hosting 업로드에서 제외한다. 사이트 ID와 프로젝트 ID가 다를 수 있으므로 승인된 담당자가 목표 사이트를 확인한다.

## 백엔드

[서버 워크플로](https://github.com/pby1360/fitlog-v2-server/blob/main/.github/workflows/deploy.yml)는 Java 21에서 Gradle 테스트를 실행한다. 배포 잡은 브랜치 최신 커밋을 검사하고 기존 WIF로 인증한다. [Dockerfile](https://github.com/pby1360/fitlog-v2-server/blob/main/Dockerfile)에서 amd64 이미지를 만들고, 이미지의 JAR 목록을 검사해 로컬·백업 설정과 누락된 운영 프로필을 차단한다. Artifact Registry에는 SHA 태그와 `latest`를 푸시하고 Cloud Run은 SHA 이미지로 갱신한다. 서비스에 설정된 환경변수와 Secret Manager 참조를 유지한다. 컨테이너는 비루트 사용자로 실행된다.

- 서버 설정은 환경변수와 Google Secret Manager 참조를 사용한다. 비밀값과 설정 백업은 저장소에서 관리하지 않는다. 원본 PowerShell 절차는 값의 BOM·후행 줄바꿈을 피하고 기존 항목에 새 버전을 추가하는 방식이었다.
- 백엔드와 웹의 배포 계정을 분리하고 WIF 조건으로 대상 저장소와 배포 가능한 ref를 제한한다. 배포 권한과 실행 중 Secret Manager 읽기 권한의 역할을 분리한다.
- 운영 이관 기록의 DB는 Supabase PostgreSQL(서울)이다. 기록에는 트랜잭션 풀러와 `prepareThreshold=0` 사용이 남아 있다. 현행 서버 프로필은 연결 설정을 주입받고 Flyway와 JPA 스키마 검증을 사용한다. 운영 인스턴스 설정은 확인 대상이다.
- 원본 운영 기준에는 Cloud Run 최소 0·최대 2 인스턴스, 로드 밸런서·VPC Connector·NAT 고정비 회피, 예산 경보, 무료 DB 일시정지 대응이 있다. [정리 정책 파일](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/artifact-cleanup-policy.json)은 최근 6개 버전 보존과 14일 경과 삭제를 정의한다. 8월 백로그의 ‘2개 보존’은 과거 계획이며 실제 정책 적용 여부는 별도 확인이 필요하다.

## OPS-01 배포 증거

2026-11-19 KST 기준이다. `VERIFIED`는 해당 행의 직접 증거를 확인했다는 의미다. `UNVERIFIED`는 현재 운영 메타데이터나 검증 기록이 필요함을 뜻한다. 검사에서 오류를 확인한 경우 `FAILED`로 기록한다. Actions의 전체 성공과 실제 게시 단계는 별도로 확인한다.

| 항목 | Web · Firebase Hosting | Server · Cloud Run |
| --- | --- | --- |
| `VERIFIED` 최신 `main` 및 CI | [`4ae88e1`](https://github.com/pby1360/fitlog-v2-web/commit/4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6). 분류·check·Playwright 성공, deploy skipped. [실행](https://github.com/pby1360/fitlog-v2-web/actions/runs/44462060250) | [`6d1c7ba`](https://github.com/pby1360/fitlog-v2-server/commit/6d1c7ba7f227b3b6087e2033b1e74213f25fa708). 분류·Gradle test 성공, deploy skipped. [실행](https://github.com/pby1360/fitlog-v2-server/actions/runs/44450257913) |
| `VERIFIED` 마지막으로 확인한 배포 성공 | `2026-11-13T00:19:17+09:00`에 `3d6412ec605ed6f83f86b1e51d6b740df9db25d2`를 사이트 `fitlog-505315-5af8e`에 게시했다. [배포 실행](https://github.com/pby1360/fitlog-v2-web/actions/runs/43246172583/job/131280123077) | `2026-10-07T23:13:37+09:00`에 `1154a06268b0336ab5154c9c2c0d8b405bad8717` 이미지로 `fitlog-server-00005-8tn`을 배포했다. 이미지 digest는 `sha256:2eb78030502b7f98e4e73def7283a4f2d13573a4232d7fe320007499cf169729`다. [배포 실행](https://github.com/pby1360/fitlog-v2-server/actions/runs/37634291023/job/112836889433) |
| `VERIFIED` 마지막 성공 배포 SHA와 현재 Git 차이 | V1-04 캘린더는 마지막 확인 성공 배포 SHA에 포함되지 않았다. 최신 `main`에는 캘린더, 빌드 입력, 테스트 및 워크플로 변경이 있다. 이후 확인한 Actions는 배포를 생략했다. [Git 비교](https://github.com/pby1360/fitlog-v2-web/compare/3d6412ec605ed6f83f86b1e51d6b740df9db25d2...4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6) | 서버 `main`과 마지막 확인 배포 SHA 사이 변경은 워크플로·스크립트·개발 지침이다. 서버 실행 코드와 Flyway V1–V7 파일 차이는 없다. [Git 비교](https://github.com/pby1360/fitlog-v2-server/compare/1154a06268b0336ab5154c9c2c0d8b405bad8717...6d1c7ba7f227b3b6087e2033b1e74213f25fa708) |
| `UNVERIFIED` 현재 운영 메타데이터 | `fit2log.com` 사이트 매핑, 현재 live 릴리스 버전 ID·생성 시각, 실제 V1-04 반영, 직전 안정 버전 보존. Firebase CLI 읽기 조회는 사용 가능한 인증이 없어 실패했다. | 현재 제공 리비전과 traffic, 현재 및 직전 안정 리비전·이미지 digest, Artifact Registry 이미지 및 정리 정책 적용 상태, 현재 Flyway 적용 버전. Cloud Run·Artifact Registry 읽기 자격증명을 확인할 수 없었다. |
| `UNVERIFIED` 롤백 실행과 서비스 검증 | 이전 호환 릴리스와 앱 셸·PWA 캐시 확인, 실제 휴대폰에서 캘린더 월 변경 및 일지 상세 복귀. | 이전 리비전·이미지 보존, 실제 스키마 역호환성, 헬스체크·Google/Kakao 로그인·세션 생성·기록 조회. |

승인된 담당자는 **Firebase Console → Hosting → 사이트 → Release history**에서 `fit2log.com`에 연결된 사이트의 현재 live와 직전 릴리스의 ID·시각을 조회한다. Actions 로그와 시각·사이트를 대조한다. SHA를 직접 노출하지 않는 릴리스는 버전의 파일 manifest나 알려진 빌드 산출물의 해시 등 추가 근거로 연결한다. 시각만 맞는 경우 SHA는 미확인으로 남긴다. V1-04 미반영이 운영에서 확인되면 현재 `main`을 배포할지 별도 승인으로 결정한다. [Firebase Hosting 릴리스 관리](https://firebase.google.com/docs/hosting/manage-hosting-resources)

승인된 담당자는 `roles/run.viewer` 및 해당 저장소의 `roles/artifactregistry.reader`가 있는 계정으로 Cloud Run 트래픽과 리비전 메타데이터, 이미지 보존을 확인한다. 정책 조회가 권한 오류로 끝나면 필요한 조회 권한만 관리자에게 요청한다. 운영 DB와 Secret은 이 명령에 필요 없다.

```sh
gcloud run services describe fitlog-server --project=fitlog-505315 --region=asia-northeast3 \
  --format='json(status.latestReadyRevisionName,status.traffic)'
gcloud run revisions list --service=fitlog-server --project=fitlog-505315 --region=asia-northeast3 \
  --format='table(metadata.name,metadata.creationTimestamp,spec.containers[0].image,status.imageDigest)'
gcloud artifacts docker images list \
  asia-northeast3-docker.pkg.dev/fitlog-505315/fitlog/fitlog-server --include-tags
gcloud artifacts repositories list-cleanup-policies fitlog --project=fitlog-505315 --location=asia-northeast3
```

[롤백 판단과 검증](RUNBOOK.md#ops-01-롤백-검증) · [Cloud Run 리비전](https://cloud.google.com/run/docs/managing/revisions) · [Artifact Registry 정리 정책](https://cloud.google.com/artifact-registry/docs/repositories/cleanup-policy)

### 배포 정책 오프라인 검증

웹·서버 각각 14개 변경 분류·게이트, 잘못된 이벤트 5개, 최신 SHA 확인 3개가 통과했다. 기능+문서, 테스트 전용, 인증·운영 경로 검토, 다중 커밋·병합·이름 변경, 검사 실패, 수동 실행 확인값 및 최신 SHA 조회 실패를 포함한다. 두 워크플로의 배포 잡은 동일 저장소 안에서 직렬화되고 실제 게시 직전 최신 SHA를 다시 검사한다. 운영 배포를 발생시키는 검증은 별도 승인 대상이다.

## 승인된 배포 담당자 확인 순서

1. 대상 저장소와 커밋, 필요한 배포 변수·WIF·서비스 계정, 직전 안정 릴리스와 Flyway 호환성을 확인한다.
2. 워크플로의 검사 및 배포 잡 결과, 실제 제공 중인 웹 릴리스와 서버 리비전을 확인한다.
3. 헬스체크, SPA 하위 경로 새로고침, Google·Kakao 로그인 및 CORS, 프로그램→세션→일지 흐름을 확인한다.
4. 실패 시 [런북](RUNBOOK.md)의 징후와 롤백 기준으로 대응하고 관련 변경·검증 근거를 남긴다.

Firebase Hosting·Cloud Run 이관 및 도메인 전환은 8월 원본의 기록이다. 최신 Actions 근거는 위 OPS-01 표에 기록했다. 운영 리소스 메타데이터 대조는 남아 있다. 과거 Vercel 설정 파일은 웹에 남아 있으며 Render·Vercel 정리와 예전 OAuth 등록 URI 정리 상태는 [백로그](../status/BACKLOG.md)에 있다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `배포.md`(2026-10-07 수정), `TASKS.md` P1, `fitlog-v2-MoC.md` 및 서버·웹 main |
| 관련 기능 또는 Issue | M2–M4, [배포 ADR](../decisions/0003-gcp-hosting.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [시스템 개요](../architecture/SYSTEM_OVERVIEW.md), [런북](RUNBOOK.md) |
