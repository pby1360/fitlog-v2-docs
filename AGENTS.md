# FitLog 문서 관리 규칙

## 작업 전

1. [기능 목록](features/README.md)에서 해당 PRD와 Tech Spec을 읽고 관련 ADR과 Issue를 확인한다. 여러 기능에 걸친 계약은 [시스템 개요](architecture/SYSTEM_OVERVIEW.md)와 [API 목록](api/README.md)을 함께 확인한다.
2. 제품 범위는 [요구사항](product/REQUIREMENTS.md)과 PRD에서 확인한다. 사용자 승인 전에는 신규·변경 요구사항을 초안으로 기록한다. 기획과 구현이 다르면 원본 날짜, 결정 근거, 코드 커밋을 남긴다.
3. 작업의 요구사항·우선순위는 [BACKLOG](status/BACKLOG.md)에서 확인한다. 실행 상태는 `main`의 [TASKS](status/TASKS.md)를 원본으로 삼는다. 착수 전에 Task를 등록하고 승인 범위, 최신 `main` SHA와 동일 Task의 선점·진행 여부를 확인한다. [개발 작업 등록과 실행](operations/DEVELOPMENT_WORKFLOW.md)
4. 상태 PR이 `main`에 반영돼 자신의 `STARTING` 선점과 커밋을 확인한 뒤에 Cloud 실행을 시작한다. 선점 확인이 실패하거나 다른 실행이 먼저 선점하면 중단한다. `IN_PROGRESS`에는 실제 실행 ID 또는 실행 시작 근거를 연결한다.

로드맵에 없던 요청은 [신규 기능 아이디어](product/FEATURE_IDEAS.md)에 고유 ID로 등록한다. 사용자 요청에 따라 PRD·Tech Spec을 구체화하고, 승인된 범위를 같은 ID로 BACKLOG에 등록한다. [작업 대기열](status/WORK_QUEUE.yaml)의 `READY`는 사용자 승인 근거, 명세 SHA, 선행 작업 완료, 명시적인 자동 개발 허용이 모두 확인된 작업에만 사용한다. 예약 점검은 읽기 전용으로 유지한다. [대기열 등록과 실행 조건](operations/DEVELOPMENT_WORKFLOW.md#신규-기능과-실행-대기열)

## 작업 중

5. 코드 변경으로 영향받는 원본 문서를 갱신한다. 제품 범위는 `product/`, 기능별 행위와 설계는 `features/`, 공유 기술 계약은 `architecture/`와 `api/`, 배포와 대응 절차는 `operations/`에 둔다. 다른 문서는 상대 링크로 연결한다.
6. 유지 비용, 보안, 데이터 수명, 인터페이스 또는 아키텍처에 장기 영향을 주는 결정은 [ADR 템플릿](templates/ADR_TEMPLATE.md)으로 작성한다. 기존 결정이 바뀌면 후속 ADR을 연결한다.
7. Draft PR이 열리면 `PR_OPEN`을 기록하고 코드 PR과 필요한 Docs PR을 상호 연결한다. 실패·추가 승인·중단 확인이 필요한 경우 `BLOCKED`와 사유를 남긴다. 상태 갱신은 별도 브랜치와 PR을 사용한다. 에이전트는 운영 환경에 접근하거나 배포를 직접 실행하지 않는다. 승인된 `main` 변경의 자동 배포는 GitHub Actions가 수행한다. [배포 절차](operations/DEPLOYMENT.md)

## 작업 후

8. 실제 코드 병합 SHA, 확인한 경로와 테스트 범위를 [현재 상태](status/CURRENT_STATUS.md)에 남긴다. 영향받은 Tech Spec과 [백로그](status/BACKLOG.md)를 갱신하고 결정과 변경은 [개발 이력](history/README.md)에 기록한다. 코드와 필요한 Docs 병합을 확인한 다음 TASKS를 `DONE`으로 갱신한다. 운영 검증은 별도 증거가 있어야 완료로 표시한다.
9. 문서에 상태, 원본 출처, 관련 기능 또는 Issue, 최종 검증일, 관련 설계를 기록한다. 신규 문서는 [PRD](templates/PRD_TEMPLATE.md), [Tech Spec](templates/TECH_SPEC_TEMPLATE.md), [ADR](templates/ADR_TEMPLATE.md) 템플릿 중 해당 양식을 사용한다. PR에 변경 문서, 관련 기능 또는 Issue, 검증 결과와 미확인 항목을 기록한다.
10. 코드 PR은 사용자 승인 후 수동 병합한다. 구현 Docs PR은 [자동 병합 조건](operations/DOCS_SYNC.md)을 따른다. TASKS 상태의 사전 승인 범위는 [개발 절차](operations/DEVELOPMENT_WORKFLOW.md#자동화와-수동-개입)의 전이로 한정하며 해당 자동화가 활성화되기 전에는 승인된 담당자가 상태 PR을 병합한다. 요구사항·보안 정책·제품 범위·아키텍처 결정은 별도 승인을 받는다.
11. `main`은 PR로 변경한다. 공개 문서 게시 전 상대 링크, 상호 참조, 구조, 중복·충돌, 코드 정합성과 비밀정보 포함 여부를 확인한다. 설정 백업과 자격증명은 저장소에 이관하지 않는다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | 문서 체계 및 Docs 중심 작업 상태 관리 요청, Obsidian `fitlog-v2-MoC.md`의 유지 루틴 |
| 관련 기능 또는 Issue | [전체 기능](features/README.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [시스템 개요](architecture/SYSTEM_OVERVIEW.md), [이관 기록](history/MIGRATION.md) |
