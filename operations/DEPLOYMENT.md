# 배포 구성과 절차

이 문서는 승인된 운영 담당자의 절차와 저장소의 배포 구성을 기록한다. Codex의 운영 환경 접근 및 배포는 [문서 관리 규칙](../AGENTS.md)에 따라 금지한다.

## 프런트엔드

[웹 워크플로](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/.github/workflows/deploy.yml)의 PR 경로는 Node 20에서 `npm ci`, 린트, 타입 검사를 실행한다. `main` 푸시 또는 수동 실행의 배포 잡은 검사 뒤 `VITE_API_BASE_URL`을 빌드에 주입하고 `npm run build`를 실행한다. `out/`과 API 주소가 들어간 빌드를 점검하고 Google Workload Identity Federation(WIF)으로 인증해 Firebase Hosting에 릴리스를 만든다.

[Vite](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/vite.config.ts)와 [Firebase Hosting](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/firebase.json)의 출력 경로는 `out`이다. 직접 진입 경로는 `/index.html`로 리라이트한다. 해시 자산은 장기 캐시하고 HTML 및 서비스 워커는 캐시를 제한한다. 생성된 소스맵은 Hosting 업로드에서 제외한다. 사이트 ID와 프로젝트 ID가 다를 수 있으므로 승인된 담당자가 목표 사이트를 확인한다.

## 백엔드

[서버 워크플로](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/.github/workflows/deploy.yml)는 Java 21에서 Gradle 테스트를 실행한다. `main` 푸시 또는 수동 실행의 배포 잡은 브랜치 최신 커밋 여부를 검사하고 WIF 인증을 수행한다. [Dockerfile](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/Dockerfile)에서 amd64 이미지를 만들고, 로컬·백업 설정의 비포함과 운영 프로필 패키징을 검사한 뒤 Artifact Registry에 SHA 태그와 `latest`를 푸시한다. Cloud Run은 해당 SHA 이미지로 갱신하며 서비스의 별도 설정을 재기입하지 않는다. 컨테이너는 비루트 사용자로 실행된다.

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
