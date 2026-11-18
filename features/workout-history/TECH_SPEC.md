# 운동 일지 및 대시보드 설계

## 개요 및 관련 PRD

[요구사항](PRD.md)을 기준으로 정리한다.

## 기술 설계

`/history`는 목록과 캘린더를 제공하며 `/history/:id`에서 세트 상세를 조회한다. 조회 기간·페이지와 선택 월은 URL에 보존한다. 캘린더에서 상세로 진입해 새로고침해도 같은 월로 돌아온다. 초기 월과 오늘은 `Asia/Seoul`의 날짜를 사용한다. [일지 화면](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/src/pages/history/page.tsx), [날짜 유틸리티](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/src/utils/date.ts)

캘린더는 기존 일지 API를 월별 날짜 범위와 페이지 크기 200으로 호출한다. 최초 응답의 페이지 수 안에서 이어서 조회하고 운동 ID로 중복을 제거한다. 효과가 종료되면 이전 월의 응답·오류와 후속 페이지 요청을 무시한다. 날짜 칸에 두 개의 미리보기를 보여 주고 더 보기에서 그날의 전체 기록을 연다. 빈 결과, 로딩, 오류 및 재시도를 구분한다.

대시보드는 주간·월간·부위별 통계, 연속일, 최근 운동 및 평균 완료율을 제공한다. 평균 완료율은 세션별 비율을 평균한 값에 서비스에서 백분율 변환을 한 번 적용한다. 분모가 0인 세션은 이 평균에서 제외한다.

## 설계 대안

캘린더는 기간별 일지 목록 API를 재사용한다. 전용 월간 API는 과거 백로그의 옵션이었다.

## 데이터 모델 및 API 계약

[API 목록](../../api/README.md)의 일지·대시보드 계약과 [데이터 모델](../../architecture/DATA_MODEL.md)의 스냅샷·시각 정의를 따른다.

## 예외 처리 및 보안

자기 기록만 조회한다. 캘린더는 실패 상태와 재시도를 표시한다. 없는 일지나 소유자가 다른 일지의 응답은 API 계약을 따른다.

## 테스트 계획

`KstBoundaryIntegrationTest`와 `DashboardServiceTest`로 날짜 경계 및 백분율을 확인한다. 월 전환 경쟁, 상세 복귀, KST 월·연도 경계와 윤년, 201건·하루 3건, 빈 결과·재시도, 기간 필터를 로컬 Playwright 12개에서 확인했다. 실제 운영 데이터와 운영 배포 상태는 별도 확인 항목이다. [회귀 테스트](https://github.com/pby1360/fitlog-v2-web/blob/6f8cc4c930bb8872cfc4ada71d2efabbbbf274e1/tests/history-calendar.spec.ts)

## 위험 및 롤백

과거 `LocalDateTime` 레코드의 시간대 변환 및 구버전 API의 날짜 해석 차이를 배포 전에 확인한다. 세트가 없는 세션의 완료율 제품 규칙과 캘린더 UX는 [백로그](../../status/BACKLOG.md)에 남긴다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `기획.md`, `TECH_SPEC.md`, `ROADMAP.md`, `TASKS.md` 및 서버·웹 main |
| 관련 기능 또는 Issue | D-1–D-2 |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [데이터 모델](../../architecture/DATA_MODEL.md), [현재 상태](../../status/CURRENT_STATUS.md) |
