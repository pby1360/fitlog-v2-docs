# 작업 백로그

우선순위는 8월 원본의 출시 준비, 첫 사용 경험, 후속 구상을 기준으로 가져왔다. 세부 일정은 [로드맵](../product/ROADMAP.md), 근거와 해소된 차이는 [현재 상태](CURRENT_STATUS.md)에서 관리한다. 새 제품 범위는 승인 대기다.

## 출시 준비 및 운영 확인

| 항목 | 상태와 다음 확인 | 근거 |
| --- | --- | --- |
| M3 CI·CD 실행과 롤백 | 양쪽 정의 확인. 최근 성공 실행, WIF 권한, 배포된 SHA/릴리스와 안정 롤백 가능 여부 확인. 8월 GitHub 장애는 당시 이력이다. | [배포](../operations/DEPLOYMENT.md) |
| 이미지 정리 및 비용 | 8월의 2개 보존 계획과 현재 정책 파일(6개·14일) 차이 확인. 정책 적용, 실제 사용량·예산 경보·인스턴스·DB 풀 상한·무료 DB 일시정지 대응 확인. | [런북](../operations/RUNBOOK.md) |
| 구 인프라와 도메인 잔여 설정 | Render·Vercel 정리, 남은 OAuth 리디렉션 URI와 전환기 CORS 오리진 제거 여부 확인. 운영 롤백 경로 확보 후 진행. 같은 도메인 API 리라이트는 옵션이다. | [GCP ADR](../decisions/0003-gcp-hosting.md) |
| 법적 페이지와 탈퇴 | 출시 전 실제 문의처 및 개인정보 문구 확인. 실제 흐름에서 정책 게시·모바일 진입·두 공급자 로그인·탈퇴 검증. 409 예외 대응 경로 확인. | [계정 설계](../features/account/TECH_SPEC.md) |
| 사용자·오류 관측 | 코드에 헬스체크·요청 ID가 있다. GA4/Plausible 선택, 가입·프로그램 생성·세션 완료 이벤트, Sentry 및 구조화 로그는 계획으로 확인했다. 실제 운영 관측 상태 확인. | [출시 기준](../product/RELEASE_CRITERIA.md), [런북](../operations/RUNBOOK.md) |
| 배포 위생과 품질 | 1200×630 공유 전용 이미지 검토. PR 빌드 단계·Vitest·Preview는 원본의 후속 후보. 린트 경고 4건과 현행 브랜치 정리 필요성 확인. | [프런트엔드](../architecture/FRONTEND.md) |
| 저장소 정리 | 서버 `/api/workoutroutine/**` 보안 매처와 옛 `structure.txt` 현행화 여부 확인. | [백엔드](../architecture/BACKEND.md) |

## 첫 사용자와 v1 경험

| 항목 | 상태와 다음 확인 | 근거 |
| --- | --- | --- |
| 공용 종목 | 시드 23개. 50~100개 제품 범위 및 M5 목표 80개 대비 증설 검토. 운영 데이터 수는 미확인이다. | [프로그램 PRD](../features/workout-program/PRD.md) |
| 첫 3분·프리셋 | 가입 후 프로그램 만들기 유도, 2~3개 분할 프리셋, 첫 세트까지 시간 측정과 사용자 모집·유지 결과. | [비전](../product/VISION.md), [출시 기준](../product/RELEASE_CRITERIA.md) |
| 모바일·로딩·세션 | 하단 운동·휴식 동작 UI, 로딩 표시 범위, 완전한 무프로그램 시작, 세션 중 삭제 연결. 시작 전 편집과 세션 중 추가·순서 변경은 코드에서 확인했다. | [세션 PRD](../features/workout-session/PRD.md), [현재 상태](CURRENT_STATUS.md) |
| 일지·집계 | 캘린더 전환 및 점 표시 UX. 기존 API 재사용과 전용 월간 API는 수요로 판단한다. 0세트 제외 동작의 제품 의도 확인. | [일지 설계](../features/workout-history/TECH_SPEC.md) |
| 성능 | 콜드스타트 과거 기록 약 8.6초의 재측정, CPU boost·스켈레톤·레이어드 JAR/CDS 검토, 일지 N+1 실측. V3 복합 인덱스가 있으므로 실제 쿼리 기준으로 확인한다. | [데이터 모델](../architecture/DATA_MODEL.md), [런북](../operations/RUNBOOK.md) |
| 제품 범위 확인 | 개인 종목·선택 신체 정보·기본 대시보드 사용 범위 승인 근거 확인. 계정 알림·데이터 백업은 후속 구상. | [제품 요구사항](../product/REQUIREMENTS.md) |

## v2 및 이후 후보

- 스쿼트 AI 프로토타입은 [기능 설계](../features/ai-coaching/TECH_SPEC.md)에 있다. 영상 보존과 처리 비용, 크레딧과 예산 경보, 상품화 시점이 미결정이다.
- 분석 횟수 제한·결제·Free/Pro, 월간 볼륨·종목별 최고기록, 부위별 리포트, 챗봇·인플루언서 루틴·음성으로 운동 진행은 후속 아이디어다.
- Terraform, 예산 초과 시 서비스 자동 중단, 상표·소셜 핸들 검토는 원본의 후순위 항목이다. IaC 미도입의 배경은 [GCP ADR](../decisions/0003-gcp-hosting.md)에 연결한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `TASKS.md` P0–P3 및 결정 목록, `ROADMAP.md` M3–M6, `fitlog-v2-MoC.md`, `history/2026-04-28.md` 및 서버·웹 main |
| 관련 기능 또는 Issue | M3–M6, DoD-1·2, [기능 목록](../features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [현재 상태](CURRENT_STATUS.md), [제품 로드맵](../product/ROADMAP.md), [배포](../operations/DEPLOYMENT.md) |
