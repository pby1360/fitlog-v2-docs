# 운동 프로그램 및 종목 설계

## 개요 및 관련 PRD

[요구사항](PRD.md)을 기준으로 정리한다.

## 기술 설계

`ProgramsPage`에서 부위·종목·프로그램 목록을 불러온다. 사용자는 프로그램을 구성해 저장하거나 `ManageWorkoutsView`에서 개인 부위와 종목을 관리한다. 각 ID는 서버에서 사용자에게 사용 가능한 마스터인지 검증한다. 서버는 요청의 부위·종목 배열 순서를 각각 저장한다. 삭제된 프로그램은 목록에서 제외된다.

## 설계 대안

2026-01 개발 이력에서 이름 기반 마스터 조회가 ID 기반 계약으로 바뀌었다. 현재는 프로그램 삭제 시 세션의 참조를 보존하는 소프트 삭제를 쓰고, 이미 사용된 개인 마스터는 보관할 수 있다.

## 데이터 모델 및 API 계약

구성은 `WorkoutProgram → WorkoutProgramPart → WorkoutProgramExercise → WorkoutProgramSet`으로 저장한다. 현재 CRUD의 요청 구조와 응답은 [API 목록](../../api/README.md)에, 공용과 개인 마스터의 소유권 규칙은 [데이터 모델](../../architecture/DATA_MODEL.md)에 있다.

## 예외 처리 및 보안

서버에서 입력과 소유권을 검증한다. 자기 소유가 아닌 프로그램을 변경할 수 없다. 보관 처리 뒤에도 과거의 세션 기록은 운동명 스냅샷으로 표시한다.

## 테스트 계획

`WorkoutMasterIntegrationTest`와 `WorkoutServiceTest`를 확인한다. 다중 부위나 종목 조합, 정렬 보존, 삭제 후 기존 일지 접근은 변경 시 UI 흐름으로 재확인한다.

## 위험 및 롤백

`V2__seed_master_data.sql`에는 공용 부위 7개와 운동 23개가 있다. 과거 문서의 30개 추정과 기획 목표는 [백로그](../../status/BACKLOG.md)에 근거와 함께 남긴다. 마스터 및 프로그램 마이그레이션의 롤백은 FK와 기존 세션을 함께 검토한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `기획.md`, `TECH_SPEC.md`, `개발프롬프팅/운동 프로그램 WorkoutProgram.md`, `history/2026-01-07.md` 및 서버·웹 main |
| 관련 기능 또는 Issue | B-1–B-3 |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [백엔드](../../architecture/BACKEND.md), [데이터 모델](../../architecture/DATA_MODEL.md) |
