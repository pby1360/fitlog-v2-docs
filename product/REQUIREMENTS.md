# 제품 요구사항

| ID | 우선순위와 범위 | 요구사항 |
| --- | --- | --- |
| A-1–A-2 | v1 P0 | Google·Kakao 소셜 로그인과 닉네임 설정. 기본 프로필의 수집 범위를 최소화한다. [회원 PRD](../features/account/PRD.md) |
| B-1–B-3 | v1 P0 | 공용 운동 종목 50~100개, 개인 프로그램 CRUD, 여러 운동 부위와 종목의 구성·순서·세트 목표 설정. [운동 프로그램 PRD](../features/workout-program/PRD.md) |
| C-1–C-3 | v1 P0 | 프로그램에서 오늘의 운동 시작, 세트별 무게·횟수 기록 및 자동 휴식 타이머, 완료 상태 저장. [운동 세션 PRD](../features/workout-session/PRD.md) |
| D-1–D-2 | v1 P1 | 완료 운동을 캘린더에 표시하고 날짜별 운동·세트 상세를 조회. [운동 일지 PRD](../features/workout-history/PRD.md) |
| E-1–E-4 | v2 구상 | 세트 영상 업로드, 영상 분석 요청, 결과 저장, 일지에서 피드백 확인. 프로젝트 완료 범위는 스쿼트 1종목 프로토타입이다. [AI 자세 분석 PRD](../features/ai-coaching/PRD.md) |

## 제품 범위와 코드 차이

- 초기 v1에서 이메일·비밀번호 가입, 트레이너·회원 관리, 커뮤니티·공부하기, 심화 리포트·통계, 직접 종목 추가 및 타이머 외 부가기능을 제외했다.
- 개인 종목 관리와 기본 대시보드는 실제 코드에 포함되어 있다. 선택형 신체 정보도 현재 프로필에 남아 있다. 변경된 범위의 제품 승인 근거는 [백로그](../status/BACKLOG.md)에서 추적한다.
- 초기 유료 구상인 AI 분석 횟수 제한·구독, 다종목 AI, 심화 리포트, 챗봇은 후속 검토 항목이다. [출시 기준](RELEASE_CRITERIA.md)에서 프로토타입 완료 범위를 정의한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `기획.md` §§3–5, `ROADMAP.md` §§2–3, `TASKS.md` P2–P3 |
| 관련 기능 또는 Issue | A-1–E-4, [기능 목록](../features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [시스템 개요](../architecture/SYSTEM_OVERVIEW.md), [현재 상태](../status/CURRENT_STATUS.md) |
