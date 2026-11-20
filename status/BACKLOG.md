# 작업 백로그

새 기능은 [아이디어 등록](../product/FEATURE_IDEAS.md)과 사용자 승인 이후 `FEAT-NNNN` ID로 P0~P3 중 한 곳에 등록한다. 기존 `V1`, `OPS`, `QUAL`, `TECH`, `AI` ID는 그대로 사용한다. 각 신규 행은 기능 ID로 시작하고 PRD·Tech Spec, 완료 조건·검증 방법, 선행 작업 ID 또는 `없음`을 연결한다. 자동 개발 허용과 대기 상태는 [작업 대기열](WORK_QUEUE.yaml)에서 확인한다.

2026-11-18 [현황 검증](CURRENT_STATUS.md)을 바탕으로 한 **우선순위 제안**이다. `P0`은 사용자 모집 전 안전한 출시 흐름을 확인하는 작업, `P1`은 v1 수용 기준과 첫 사용자 검증을 마무리하는 작업, `P2`는 후속 품질·범위 정리, `P3`는 v2 프로토타입이다. 이 우선순위는 기존 PRD의 P0/P1 요구사항 표기를 바꾸지 않는다. 각 ID의 상태는 완료 조건을 이행하고 검증 근거를 연결했을 때 갱신한다.

## P0

| 작업 | 현재 근거 또는 선행 조건 | 완료 조건 | 검증 방법 |
| --- | --- | --- | --- |
| V1-01 약관·개인정보 공개 문구와 문의처 | 두 경로에 운영자명과 이메일 자리표시자가 보인다. [약관](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/legal/TermsPage.tsx), [개인정보](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/legal/PrivacyPolicyPage.tsx) | 제품 담당자가 운영자·연락처·처리 항목·보관 정책을 확정한다. 공개 문구에 영향을 주는 V1-11 프로필 결정도 이 단계에서 반영한다. 두 페이지에서 승인 문구와 유효한 문의 방법을 제공한다. | 검토본과 페이지를 대조한다. 모바일 크기에서 홈 푸터 링크와 직접 진입을 확인한다. 실제 게시 여부와 문의 경로 테스트는 승인된 담당자가 증거를 기록한다. |
| V1-02 가입부터 첫 기록 및 탈퇴까지 검증 | [V1-02-A](TASKS.md#v1-02-a)의 모의 API Playwright와 기존 서버 통합 테스트는 로컬에서 통과했다. 실제 Google·Kakao OAuth 및 물리 휴대폰 종단 간 검증이 남는다. [웹 Draft PR](https://github.com/pby1360/fitlog-v2-web/pull/44), [수동 체크리스트](../features/account/TECH_SPEC.md#실제-oauth-및-휴대폰-수동-검증-체크리스트), [계정 설계](../features/account/TECH_SPEC.md), [세션 설계](../features/workout-session/TECH_SPEC.md) | Google·Kakao 각각 로그인·재로그인·갱신·로그아웃, 프로그램→세트 기록·휴식·완료→일지, 탈퇴·재접속 및 409 안내의 확인 결과가 있다. | 승인된 테스트 계정으로 실제 휴대폰에서 시나리오를 실행한다. 독립 테스트 데이터로 204 파기 및 409 롤백을 재검증하고, 기기·커밋·결과를 기록한다. |
| V1-03 오류·이탈 관측 | 헬스체크·요청 ID는 구현됐다. 가입·생성·세션 완료 이벤트, GA4/Plausible·Sentry·구조화 로그는 기존 후보이다. [요청 ID 필터](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/global/logging/RequestIdFilter.java), [런북](../operations/RUNBOOK.md) | 승인된 도구로 가입→프로그램 생성→세션 완료 전환과 오류를 볼 수 있다. 요청 ID로 오류를 찾을 수 있으며 확인 담당자가 정해진다. | 비운영 테스트 이벤트와 오류를 발생시켜 대시보드 집계와 요청 ID 연계를 대조한다. 승인된 담당자가 운영 관측 대시보드의 근거를 남긴다. |
| OPS-01 양쪽 배포와 롤백 증거 | Hosting Live·Cloud Run 100% 리비전·Flyway V7은 운영 담당자의 증거로 확인했다. Server `00003`·`00004`는 V7 비호환으로 복구에서 제외한다. [배포 증거](../operations/DEPLOYMENT.md#ops-01-배포-증거) | 실제 배포 SHA/릴리스, 안정 롤백 대상과 Flyway 호환성·격리 복구 검증이 기록된다. | Web Live hash 대조 및 캐시·콜백 검증, Server `00005` 정확한 digest 기동과 운영과 같은 기준선의 격리 검증이 남는다. [런북](../operations/RUNBOOK.md#ops-01-롤백-검증) |

## P1

| 작업 | 현재 근거 또는 선행 조건 | 완료 조건 | 검증 방법 |
| --- | --- | --- | --- |
| V1-04 일지 캘린더의 기록 누락·복귀·시간대 | **구현 완료·로컬 검증 완료.** 웹 PR #40이 main에 병합됐고 Playwright 12개가 통과했다. 운영 배포·실데이터 확인은 남아 있다. [웹 PR #40](https://github.com/pby1360/fitlog-v2-web/pull/40), [개발 이력](../history/2026-11-19.md) | 최신 월 응답만 반영하며 상세 왕복 시 월과 목록 필터를 보존한다. KST 경계, 빈 상태·오류 처리, 하루·월의 전체 기록 접근을 제공한다. | 월 응답 순서, 상세 복귀, UTC 월·연도 경계, 윤년, 201건, 하루 3건, 실패 후 재시도 및 목록 회귀를 자동 검증했다. [테스트](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/tests/history-calendar.spec.ts) |
| V1-05 공용 운동 종목 확충 | V2 시드는 종목 23개·부위 7개다. 원래 기획 범위는 50~100개, M5 목표는 80개다. [시드 SQL](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration/V2__seed_master_data.sql), [프로그램 PRD](../features/workout-program/PRD.md) | 승인된 공용 종목 목록과 마이그레이션이 M5의 80개 목표를 충족한다. 목표를 조정할 경우 승인 기록을 연결한다. 승인된 담당자가 실제 운영 수량도 별도 기록한다. | 빈 DB와 이전 시드가 있는 테스트 DB에서 Flyway를 적용한다. 공용 종목 수·중복·부위 및 프로그램 선택 노출을 확인하고 운영 수치는 담당자 기록과 대조한다. |
| V1-06 가입 후 첫 기록 3분 및 온보딩 | 완성된 프로그램·세션 경로가 있다. 신규 가입자의 프로그램 만들기 유도, 2~3개 분할 프리셋, 실측은 기존 후속 작업이다. [제품 비전](../product/VISION.md), [제품 로드맵](../product/ROADMAP.md) | 승인된 온보딩 범위에서 새 사용자가 가입 후 루틴을 만들고 3분 안에 첫 세트를 저장한다. 목표에 미달한 경우 병목을 기록하고 재측정한다. | 새 계정과 휴대폰으로 가입 완료→첫 세트 저장까지 시간을 재고, 단계별 소요 및 막히는 지점을 남긴다. 출시 기준의 로그인 후 측정 범위도 함께 기록한다. |
| V1-07 첫 사용자와 v1 출시 판정 | V1-01~03, OPS-01의 출시 전 증거와 V1-06의 첫 사용 결과가 선행한다. [DoD-1](../product/RELEASE_CRITERIA.md#v1-정식-출시-dod-1) | 기존 친분이 없는 가입자 10명 중 5명이 2주 이상 운동을 기록하고, 운영 개입 없이 1주 정상 동작을 포함한 DoD-1의 네 기준을 근거와 함께 충족한다. | 기간·대상 집계 기준과 운영 개입/장애 기록을 대조한다. 관측 대시보드·정책·탈퇴 증거를 함께 검토하고, 요건별 판정 및 사용자 피드백을 남긴다. |
| QUAL-01 웹 PR 회귀 확인 | 현재 웹 PR 잡에 린트·타입 검사가 있다. 빌드는 배포 잡에 있다. Playwright 테스트가 추가됐으며 PR 검사 연결은 남아 있다. [웹 워크플로](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/.github/workflows/deploy.yml#L16-L82), [스크립트](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/package.json#L6-L12) | 배포 없는 PR 잡에서 빌드 산출물과 핵심 흐름 회귀를 검증한다. 도구 선택은 구현 시 결정한다. | 테스트 PR에서 빌드·회귀 체크가 성공하고 의도한 실패에는 PR 체크가 실패하는지 확인한다. 배포 잡 로그가 실행되지 않았는지 검토한다. |
| OPS-02 이미지 보존·비용·DB 가용성 | 8월의 2개 보존은 과거 계획이다. 코드 정책은 최근 6개 보존 및 14일 경과 삭제다. [현재 정책](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/artifact-cleanup-policy.json), [배포](../operations/DEPLOYMENT.md) | 실제 정리 설정, 롤백 버전 보존, 예산 경보, 인스턴스·DB 풀 상한, 무료 DB 일시정지 대응이 기록된다. 코드와 운영 설정 차이의 처리 여부를 결정한다. | 승인된 담당자가 설정·보존 버전과 경보 기록을 대조하고, 장애 없이 확인할 수 있는 복구 증거를 남긴다. |

## P2

| 작업 | 현재 근거 또는 선행 조건 | 완료 조건 | 검증 방법 |
| --- | --- | --- | --- |
| V1-08 모바일 세션 버튼과 로딩 흐름 | 프로그램·대시보드·일지에 기본 로딩 표시가 있다. 모바일 하단 배치와 일관된 로딩/오류 UX는 후속이다. [프로그램 화면](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/pages/programs/page.tsx#L514), [세션 PRD](../features/workout-session/PRD.md) | 승인한 모바일 배치에서 운동 시작·휴식 조작이 가능하고, 조회·저장 지연과 오류 후 복구 흐름을 구별한다. | 모바일 뷰포트 또는 기기에서 긴 화면, 소프트 키보드, 느린 요청과 실패·재시도를 확인한다. |
| V1-09 진행 중 종목 삭제 웹 연결 | 서버에는 저장 후 재조회 테스트가 있고 웹은 추가와 순서 변경을 호출한다. [서버 제거 테스트](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/test/java/com/fitlog/fitlogv2server/domain/workoutsession/WorkoutSessionIntegrationTest.java#L89-L107), [웹 세션 API](https://github.com/pby1360/fitlog-v2-web/blob/3d6412ec605ed6f83f86b1e51d6b740df9db25d2/src/services/api.ts#L506-L539) | 제품이 허용할 삭제 상태를 승인하면 UI와 서버 계약을 연결한다. 재조회 뒤 삭제·정렬이 유지되며 실패 시 화면에 안내한다. | 활성 세션, 이미 기록한 세트가 있는 종목, 새로고침, 거부 응답을 테스트한다. |
| V1-10 프로그램 없는 즉석 세션 | 현재 시작 DTO는 프로그램 ID 필수다. [요청 DTO](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/dto/WorkoutSessionDto.java#L28-L34) | 범위 승인을 받은 경우 기존 프로그램 없이 시작·기록·완료·일지가 연결되고 기존 프로그램 흐름도 유지된다. | 프로그램 유무 각 경로에서 시작→기록→일지를 실행하고 동시 활성 세션 제한을 확인한다. |
| V1-11 구현된 범위에 대한 제품 결정 | 초기 범위와 달리 개인 종목·기본 대시보드·선택 신체 정보가 있다. [제품 요구사항](../product/REQUIREMENTS.md), [개인정보 ADR](../decisions/0005-member-privacy-and-withdrawal.md) | 제품 담당자가 각 항목의 유지·보류와 선택 프로필 수집 근거를 승인하고 PRD·정책·백로그에 반영한다. | 승인 기록과 데이터 모델·UI·공개 문구를 대조한다. |
| V1-12 0세트 완료율 규칙 | 평균에서 분모 0인 세션을 제외한다. [집계 쿼리](https://github.com/pby1360/fitlog-v2-server/blob/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/java/com/fitlog/fitlogv2server/domain/workoutsession/repository/WorkoutSessionRepository.java#L109-L123) | 제품이 0세트 포함 여부 및 빈 데이터의 기대값을 승인하고 사양·테스트가 같은 규칙을 따른다. | 0세트뿐인 경우와 일반 완료 세션이 섞인 경우를 계산하여 API 값과 화면을 대조한다. |
| TECH-01 린트 및 오래된 구조 정리 | V1-04 로컬 검증 기준 훅 의존성 경고 3건이 남았다. 서버 옛 경로도 확인했다. 웹 구조 리팩터링·브랜치 정리와 겹치는 범위도 확인한다. [현재 상태](CURRENT_STATUS.md#버그-및-기술-부채), [웹 #37](https://github.com/pby1360/fitlog-v2-web/issues/37) | 훅 경고의 해결 또는 유지 근거를 기록하고 실제 컨트롤러 구조와 보안 구성·구조 설명을 맞춘다. 구조 및 브랜치 정리는 영향 확인 후 범위를 확정한다. | ESLint와 인증 회귀 테스트를 재실행하고 실제 매핑 목록을 구조 문서와 대조한다. |
| TECH-02 콜드스타트·일지 성능 계측 | 과거 콜드스타트 약 8.6초는 재확인 필요. V3 복합 인덱스가 있으며 N+1은 미계측이다. [데이터 모델](../architecture/DATA_MODEL.md), [런북](../operations/RUNBOOK.md) | 반복 계측한 첫 응답 시간·일지 쿼리 수·실행 계획을 기록하고 CPU boost·로딩 UI·JAR/CDS 등 개선 착수 여부를 결정한다. | 테스트 데이터에서 목록을 비교하고 첫 요청과 이후 요청을 나눠 계측한다. 운영 지표는 승인된 담당자가 제공한다. |
| OPS-03 구 인프라·도메인 잔여 설정 | Render·Vercel, 예전 OAuth URI/CORS 정리 여부가 미확인이다. OPS-01의 복구 경로 증거가 선행한다. [GCP ADR](../decisions/0003-gcp-hosting.md), [런북](../operations/RUNBOOK.md) | 승인된 담당자가 활성 자원과 레거시 등록을 분류하고 보존 또는 정리 결정을 남긴다. | 자원·URI·오리진 목록을 대조하고 결정 후 양쪽 OAuth 콜백·SPA 접속을 확인한다. |

## P3

| 작업 | 현재 근거 또는 선행 조건 | 완료 조건 | 검증 방법 |
| --- | --- | --- | --- |
| AI-01 로컬 스쿼트 분석과 데이터·비용 결정 | v1 첫 사용자 피드백을 우선한다. 처리 위치, 영상 보존·삭제, 비용 한도·크레딧이 미확정이다. [AI 설계](../features/ai-coaching/TECH_SPEC.md) | 스쿼트 1종목의 로컬 분석 결과와 승인된 영상 처리·보존 정책, 실행당 비용 추정, 후속 착수 여부를 기록한다. | 승인된 테스트 클립으로 깊이·무릎 각도 결과를 확인하고 영상 보관·삭제 시점 및 비용 추정의 가정을 검토한다. |
| AI-02 E-1–E-4 종단 간 프로토타입 | 현재 저장소에 분석·업로드 UI/계약·결과 저장 경로가 없다. AI-01의 설계·범위 승인 후 진행한다. [AI PRD](../features/ai-coaching/PRD.md) | 스쿼트 세트 완료→영상 업로드→분석→같은 세트의 피드백 확인이 [DoD-2](../product/RELEASE_CRITERIA.md)를 충족한다. | 실제 휴대폰으로 정상 흐름을 확인하고, 분석 실패·재시도 및 승인된 삭제 정책을 테스트한다. 정확도 목표는 제품 결정이 있을 때 별도로 검증한다. |

## 승인 대기 후보

| 후보 | 완료 조건 | 검증 방법 |
| --- | --- | --- |
| 1200×630 공유 이미지, 계정 알림·데이터 백업 | v1 이후 우선순위와 착수 여부를 결정한다. 현행 공유 이미지 연결은 [이전 항목 검증](CURRENT_STATUS.md#이전-백로그에서-해소된-항목)을 따른다. | 공유 미리보기 샘플과 계정 기능 수요를 근거로 제품 승인 및 후속 작업 연결을 확인한다. |
| 같은 도메인 API 리라이트, PR Preview·Vitest, Terraform, 예산 초과 자동 중단 | 각 후보의 운영 비용·필요성 및 선행 조건을 검토하고 채택 시 승인된 작업으로 등록한다. | 현행 [배포](../operations/DEPLOYMENT.md)·복구 절차와 비교한 결정 기록을 확인한다. |
| Free/Pro·결제·구독, 다종목 AI, 월간 볼륨·최고기록·부위별 리포트, 챗봇·인플루언서 루틴·음성 진행, 상표·소셜 핸들 | 초기 아이디어를 보존한다. v1 피드백 후 채택 범위와 후속 우선순위를 승인한다. | 제품 회의 기록과 [출시 기준](../product/RELEASE_CRITERIA.md) 및 승인된 PRD를 대조한다. |

해결된 과거 항목과 근거는 [현재 상태](CURRENT_STATUS.md#이전-백로그에서-해소된-항목)에서 확인한다. 일정과 단계별 종료 조건은 [로드맵](../product/ROADMAP.md)이 기준이다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | 최초 이관 PR #1, Obsidian `TASKS.md`·`ROADMAP.md`·`fitlog-v2-MoC.md`, 이번 코드 및 실행 검증 |
| 관련 기능 또는 Issue | M3–M6, DoD-1·2, [기능 목록](../features/README.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [현재 상태](CURRENT_STATUS.md), [제품 로드맵](../product/ROADMAP.md), [배포](../operations/DEPLOYMENT.md) |
