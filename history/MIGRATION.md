# Obsidian 이관 기록

원본 위치는 Obsidian Vault의 `01.Project/fitlog-v2/`다. Google Drive에서 원본 본문 21개를 읽고 파일 목록 크기와 읽은 바이트 수를 대조했다. 설정 백업 1개는 목록에서 확인했다. 분석 대상 본문은 루트 6개, 날짜별 이력 14개, 개발 프롬프트 1개다.

## 원본과 공식 문서의 대응

| Obsidian 원본 | 반영 위치 | 이관 방식 |
| --- | --- | --- |
| `fitlog-v2-MoC.md` (2026-08-27 내용 기준) | [탐색 허브](../README.md), [로드맵](../product/ROADMAP.md), [현재 상태](../status/CURRENT_STATUS.md), [ADR](../decisions/README.md) | 문서 지도·운영 주기·결정 이력 이관. 현재 상태는 코드 근거로 다시 확인. |
| `기획.md` | [비전](../product/VISION.md), [요구사항](../product/REQUIREMENTS.md), [기능 PRD](../features/README.md) | 대상 사용자, 초기 범위와 제외 범위, A-1–E-4 추적. |
| `ROADMAP.md` (2026-08-27) | [로드맵](../product/ROADMAP.md), [출시 기준](../product/RELEASE_CRITERIA.md), [백로그](../status/BACKLOG.md), [AI 설계](../features/ai-coaching/TECH_SPEC.md) | 당시 기간·DoD 및 후속 과제의 근거 보존. 일정 경과와 달성 증거를 구분. |
| `TASKS.md` (2026-08-27 내용 기준) | [백로그](../status/BACKLOG.md), [현재 상태](../status/CURRENT_STATUS.md), [배포](../operations/DEPLOYMENT.md), [런북](../operations/RUNBOOK.md), [ADR](../decisions/README.md) | 과거 체크박스를 현재 코드 및 최신 결정과 대조. 운영 이관 당시 중복 단계와 후속 계획 통합. |
| `TECH_SPEC.md` (2026-07-01 내용 기준) | [시스템](../architecture/SYSTEM_OVERVIEW.md), [프런트엔드](../architecture/FRONTEND.md), [백엔드](../architecture/BACKEND.md), [데이터](../architecture/DATA_MODEL.md), [API](../api/README.md), [기능 Tech Spec](../features/README.md) | 계약의 현재 기준을 두 `main` 커밋으로 고정. [현재 상태](../status/CURRENT_STATUS.md)의 차이 표에 기존 명세와 변경 설명 유지. |
| `배포.md` (2026-10-07 Drive 수정일) | [배포](../operations/DEPLOYMENT.md), [런북](../operations/RUNBOOK.md), [GCP ADR](../decisions/0003-gcp-hosting.md) | CLI 메모의 단계·권한·캐시·인코딩·롤백 원리를 보존하고 현재 워크플로에 연결. |
| `개발프롬프팅/운동 프로그램 WorkoutProgram.md` | [프로그램 PRD](../features/workout-program/PRD.md), [프로그램 Tech Spec](../features/workout-program/TECH_SPEC.md) | 4단계 생성 흐름, 다중 부위·종목과 세트 필드 이관. |
| `history/` (14개) | [날짜별 이력](README.md) | 원본 날짜 이름과 당시 작업·후속 목록을 보존. 본문에 다른 작업일이 있으면 둘 다 표기. |
| `백업/application.yml.md` | 제외 | 설정 백업은 파일 목록에서만 확인. |

## 링크와 중복 처리

- 프로젝트 범위의 위키 링크는 허브, 요구사항, 로드맵, 백로그, 설계 개요, 배포의 상대 링크로 바꿨다. 원본이 참조하던 외부 Vault 노트 `02.Area/창업/창업-MoC`와 단축명 `창업-MoC`는 이관 범위 밖이다. 원본의 프로젝트 종료 후 운영·사업 전환 및 보관 경로 `04.Archive/fitlog-v2/`는 이 기록에 남긴다.
- MoC의 현재 상태와 다음 작업, TASKS의 체크박스, ROADMAP의 마일스톤 및 TECH_SPEC의 구현 현황은 반복될 때 각 영역의 기준 문서 하나에 둔다. 동일 작업의 오래된 체크 상태는 날짜별 이력 또는 [코드 차이 표](../status/CURRENT_STATUS.md)에 보존한다.
- 기획은 제품 의도, 날짜별 기록은 당시 관측, 승인·결정은 근거를 찾을 수 있는 이력, 현재 기술 상태는 기준 커밋의 계약을 따른다.
- 공개 문서에는 설정 백업, 비밀값, 개인 작업 경로와 운영 자원 식별자·원본 비공개 공유 링크를 포함하지 않았다. 운영 및 비용 실측 수치는 원본의 과거 관측임을 표시했다.
- [문서 관리 규칙](../AGENTS.md)과 [PRD](../templates/PRD_TEMPLATE.md)·[Tech Spec](../templates/TECH_SPEC_TEMPLATE.md)·[ADR](../templates/ADR_TEMPLATE.md) 템플릿은 이번 구축 요청을 근거로 추가했다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `01.Project/fitlog-v2/` 원본 목록 및 이관 요청 |
| 관련 기능 또는 Issue | [전체 기능](../features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [시스템 개요](../architecture/SYSTEM_OVERVIEW.md), [ADR](../decisions/README.md) |
