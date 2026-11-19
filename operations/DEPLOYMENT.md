# 배포 구성과 절차

이 문서는 GitHub Actions의 배포 정책과 승인된 운영 담당자의 절차를 기록한다. 에이전트는 운영 환경에 접근하거나 배포를 직접 실행하지 않는다. [문서 관리 규칙](../AGENTS.md)

## CI와 자동 배포 정책

새 정책은 웹·서버의 해당 워크플로 변경 PR이 승인되고 병합된 뒤 적용한다. 코드 PR은 사용자가 승인한 뒤 수동으로 병합한다. 기능 변경·버그 수정의 커밋 또는 병합 메시지에는 `[skip ci]` 등 CI 생략 문구를 넣지 않는다. CI의 필수 잡은 PR의 파일 유형과 무관하게 보고되며, 운영 배포는 승인된 변경이 `main`에 반영돼 필수 검사를 통과하면 GitHub Actions가 수행한다.

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

V1-04를 반영한 웹 PR #40은 PR 검사에 성공했고 배포 잡은 생략됐다. `main` 병합 커밋 `6f8cc4c`의 CI 생략 표시 이후 해당 기능을 포함한 Firebase Hosting 릴리스 SHA는 확인되지 않았다. 실제 릴리스에서 포함 여부를 확인하고 미반영이면 승인된 운영 담당자가 최신 `main`을 대상으로 배포한다. [PR 검사](https://github.com/pby1360/fitlog-v2-web/actions/runs/44332492330) · [병합 커밋](https://github.com/pby1360/fitlog-v2-web/commit/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1)

[Vite](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/vite.config.ts)와 [Firebase Hosting](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/firebase.json)의 출력 경로는 `out`이다. 직접 진입 경로는 `/index.html`로 리라이트한다. 해시 자산은 장기 캐시하고 HTML 및 서비스 워커는 캐시를 제한한다. 생성된 소스맵은 Hosting 업로드에서 제외한다. 사이트 ID와 프로젝트 ID가 다를 수 있으므로 승인된 담당자가 목표 사이트를 확인한다.

## 백엔드

[서버 워크플로](https://github.com/pby1360/fitlog-v2-server/blob/main/.github/workflows/deploy.yml)는 Java 21에서 Gradle 테스트를 실행한다. 배포 잡은 브랜치 최신 커밋을 검사하고 기존 WIF로 인증한다. [Dockerfile](https://github.com/pby1360/fitlog-v2-server/blob/main/Dockerfile)에서 amd64 이미지를 만들고, 이미지의 JAR 목록을 검사해 로컬·백업 설정과 누락된 운영 프로필을 차단한다. Artifact Registry에는 SHA 태그와 `latest`를 푸시하고 Cloud Run은 SHA 이미지로 갱신한다. 서비스에 설정된 환경변수와 Secret Manager 참조를 유지한다. 컨테이너는 비루트 사용자로 실행된다.

- 서버 설정은 환경변수와 Google Secret Manager 참조를 사용한다. 비밀값과 설정 백업은 저장소에서 관리하지 않는다. 원본 PowerShell 절차는 값의 BOM·후행 줄바꿈을 피하고 기존 항목에 새 버전을 추가하는 방식이었다.
- 백엔드와 웹의 배포 계정을 분리하고 WIF 조건으로 대상 저장소와 배포 가능한 ref를 제한한다. 배포 권한과 실행 중 Secret Manager 읽기 권한의 역할을 분리한다.
- 운영 이관 기록의 DB는 Supabase PostgreSQL(서울)이다. 기록에는 트랜잭션 풀러와 `prepareThreshold=0` 사용이 남아 있다. 현행 서버 프로필은 연결 설정을 주입받고 Flyway와 JPA 스키마 검증을 사용한다. 운영 인스턴스 설정은 확인 대상이다.
- 원본 운영 기준에는 Cloud Run 최소 0·최대 2 인스턴스, 로드 밸런서·VPC Connector·NAT 고정비 회피, 예산 경보, 무료 DB 일시정지 대응이 있다. [정리 정책 파일](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/artifact-cleanup-policy.json)은 최근 6개 버전 보존과 14일 경과 삭제를 정의한다. 8월 백로그의 ‘2개 보존’은 과거 계획이며 실제 정책 적용 여부는 별도 확인이 필요하다.

## 승인된 배포 담당자 확인 순서

1. 대상 저장소와 커밋, 필요한 배포 변수·WIF·서비스 계정, 직전 안정 릴리스와 Flyway 호환성을 확인한다.
2. 워크플로의 검사 및 배포 잡 결과, 실제 제공 중인 웹 릴리스와 서버 리비전을 확인한다.
3. 헬스체크, SPA 하위 경로 새로고침, Google·Kakao 로그인 및 CORS, 프로그램→세션→일지 흐름을 확인한다.
4. 실패 시 [런북](RUNBOOK.md)의 징후와 롤백 기준으로 대응하고 관련 변경·검증 근거를 남긴다.

Firebase Hosting·Cloud Run 이관 및 도메인 전환은 8월 원본의 기록이다. 자동 배포 실행 결과와 운영 리소스 상태를 이번 이관에서 확인하지 않았다. 과거 Vercel 설정 파일은 웹에 남아 있으며 Render·Vercel 정리와 예전 OAuth 등록 URI 정리 상태는 [백로그](../status/BACKLOG.md)에 있다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `배포.md`(2026-10-07 수정), `TASKS.md` P1, `fitlog-v2-MoC.md` 및 서버·웹 main |
| 관련 기능 또는 Issue | M2–M4, [배포 ADR](../decisions/0003-gcp-hosting.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [시스템 개요](../architecture/SYSTEM_OVERVIEW.md), [런북](RUNBOOK.md) |
