# 데이터 모델

## 집합과 관계

| 영역 | 현재 모델과 제약 |
| --- | --- |
| 계정 | `member`에 이메일·닉네임·이미지·역할·제공자 식별자 및 선택 프로필(키·몸무게·목표·경력). `(provider, provider_id)`와 이메일은 각각 고유하다. |
| 인증 | `auth_session`은 기기별 세션 및 갱신 토큰 해시를, `auth_login_code`는 일회용 코드 해시를 관리한다. `oauth2_authorization_request`는 만료되는 OAuth 상태를 관리한다. |
| 운동 마스터 | `workout_part` → `workout`. 공용은 `member_id IS NULL`, 개인은 회원 소유다. 이름 유일성은 공용·개인 및 부위의 범위를 따르며 사용 중인 마스터는 보관할 수 있다. |
| 프로그램 | 회원 → `workout_program` → `workout_program_part` → `workout_program_exercise` → `workout_program_set`. 부위·종목은 마스터를 참조하고 세트에는 목표 무게·횟수·휴식·메모를 둔다. `deleted_at`으로 삭제를 표시한다. |
| 세션 | 회원과 프로그램 → `workout_session` → `workout_session_exercise` → `workout_session_set`. 프로그램명, 종목명, 부위명 스냅샷을 사용한다. 세트는 목표값, 실측값, 완료 여부와 시각을 보관한다. |
| 세션 무결성 | 회원별 활성 세션은 하나다. 세트 번호는 세션 운동 내에서 유일하다. 회원·상태·시작 시각 및 FK 조회용 인덱스가 있다. |
| 날짜 | 일지·통계 기준일은 `Asia/Seoul`이다. 감사 시각과 삭제 시각에 `timestamptz`를 사용한다. |
| 수명 주기 | 운동 프로그램의 일반 삭제는 소프트 삭제다. 탈퇴는 개인 데이터와 관련 인증 데이터를 트랜잭션에서 물리 삭제한다. [탈퇴 ADR](../decisions/0005-member-privacy-and-withdrawal.md) |

## Flyway 변경 역사

| 버전 | 역할 |
| --- | --- |
| V1 | 계정·마스터·프로그램·세션 기준 스키마와 FK |
| V2 | 공용 부위 7개와 종목 23개의 누락분 시드 |
| V3 | 활성 세션 유일성, 세트 제약 및 조회 인덱스 |
| V4 | 제공자 식별자·기기별 세션·로그인 코드·OAuth 상태 테이블, 회원의 기존 갱신 토큰 컬럼 제거 |
| V5 | 마스터 소유권 및 보관, 운동 일지의 이름 스냅샷 |
| V6 | 감사·삭제 시각의 시간대 변환 |
| V7 | 전화번호, 생년월일 컬럼 제거 |

원본의 `WorkoutRoutine`은 현재 `WorkoutSession`에 해당한다. 과거 Tech Spec에서 예약돼 있다고 설명한 `analysis_result`는 기준 커밋의 엔티티나 V1–V7에 없다. [마이그레이션 SQL](https://github.com/pby1360/fitlog-v2-server/tree/1154a06268b0336ab5154c9c2c0d8b405bad8717/src/main/resources/db/migration), [AI 계획](../features/ai-coaching/TECH_SPEC.md)

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `TECH_SPEC.md` §4, `기획.md` §§4–5, `history/2026-03-17.md` 및 서버 main |
| 관련 기능 또는 Issue | [전체 기능](../features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [백엔드](BACKEND.md), [API 목록](../api/README.md) |
