# 운동 세션 설계

## 개요 및 관련 PRD

[요구사항](PRD.md)을 기준으로 정리한다.

## 기술 설계

`/workout`에서 프로그램을 선택하고 시작 전 종목과 세트를 조정할 수 있다. 활성 세션은 `/workout/session`에서 읽어 이어간다. 세트 완료 응답 후 웹이 휴식 타이머를 시작한다. 웹은 종목 추가와 남은 종목 순서 변경을 연결한다. `DELETE .../exercises/{exerciseId}`의 세션 중 제거는 서버 계약만 확인했다.

서버는 회원별 활성 세션을 하나로 제한한다. 시작과 변경은 서비스 트랜잭션으로 처리하고, 변경 시 소유 세션 조회에 잠금을 사용한다. 상태는 `IN_PROGRESS`, `PAUSED`, `COMPLETED`, `CANCELLED`다. 실제 운동시간은 일시정지 누적 시간을 제외한다.

## 설계 대안

원본의 `WorkoutRoutine` 이름은 현행의 `WorkoutSession`으로 이어졌다. 현재 화면은 프로그램에 세션별 편집을 더한다. 제품에서 완전한 무프로그램 세션을 제공할지는 [백로그](../../status/BACKLOG.md)에서 추적한다.

## 데이터 모델 및 API 계약

세션은 프로그램과 별도로 종목과 세트의 목표·실측 값 및 이름 스냅샷을 갖는다. 상세 동작은 [데이터 모델](../../architecture/DATA_MODEL.md)과 [API 목록](../../api/README.md)에 있다.

## 예외 처리 및 보안

`409` 활성 세션 충돌에서 웹은 진행 중 화면으로 이동한다. 서버에서 세션 상태 전이, 쓰기 소유권, 순서 변경 및 세트 입력 값을 검증한다. 세트 번호와 세션 종료 시각은 서버 기준이다.

## 테스트 계획

`WorkoutSessionIntegrationTest`, `WorkoutSessionServiceTest`, `WorkoutSessionTest`, `WorkoutSessionDtoValidationTest`를 확인한다. 모바일 화면의 타이머·오류 복구·새로고침 동작은 실제 흐름에서 재검증한다.

## 위험 및 롤백

다중 탭과 기기의 중복 시작, 조회 후 쓰기 경쟁, 표시 타이머와 서버 시각의 차이를 변경 후 확인한다. 활성 세션 유일성 제약은 구버전 배포 전 호환성을 확인한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `기획.md`, `TECH_SPEC.md`, `TASKS.md`, `history/2026-02-11.md` 및 서버·웹 main |
| 관련 기능 또는 Issue | C-1–C-3, [웹 PR #36](https://github.com/pby1360/fitlog-v2-web/pull/36) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [백엔드](../../architecture/BACKEND.md), [데이터 모델](../../architecture/DATA_MODEL.md) |
