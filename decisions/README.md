# 아키텍처 결정 기록

| ADR | 결정 시점 또는 근거 |
| --- | --- |
| [0001 개인 운동 일지로 전환](0001-b2c-workout-log.md) | 2025-10-27, 기획 및 MoC |
| [0002 PostgreSQL 선택](0002-postgresql.md) | 2025-11-06, MoC의 결정 이력 |
| [0003 GCP 호스팅 전환](0003-gcp-hosting.md) | 2026-07-30, 8월 운영 이관 기록 |
| [0004 OAuth 계정 식별 및 기기별 세션](0004-oauth-session-redesign.md) | 2026-09-24 변경, 서버 PR #28 |
| [0005 회원 개인정보 최소화 및 탈퇴](0005-member-privacy-and-withdrawal.md) | 2026-09-24 변경, 서버 PR #28·웹 PR #26 |
| [0006 운동 기록 스냅샷과 날짜 경계](0006-workout-record-integrity.md) | 2026-09-24 변경, Flyway V5–V6 |

위 결정은 원본 또는 병합 코드에서 확인한 이관 기록이다. 제품 일정과 범위에 관한 2026-08-27 결정은 [출시 기준](../product/RELEASE_CRITERIA.md)에 보존했다. 후속 결정에는 [ADR 템플릿](../templates/ADR_TEMPLATE.md)을 사용하고 해당 문서와 이 인덱스를 갱신한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `fitlog-v2-MoC.md`, `ROADMAP.md`, `TASKS.md`, `history/` 및 서버·웹 main |
| 관련 기능 또는 Issue | [전체 기능](../features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [시스템 개요](../architecture/SYSTEM_OVERVIEW.md) |
