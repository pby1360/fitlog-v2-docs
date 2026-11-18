# 계정 및 인증 설계

## 개요 및 관련 PRD

[요구사항](PRD.md)을 기준으로 정리한다.

## 기술 설계

`LoginModal`에서 Google·Kakao OAuth2를 시작한다. 서버가 인가 요청의 상태를 DB에 저장한다. 콜백 성공 시 웹의 `/auth/callback`으로 일회용 교환 코드를 전달한다. 웹은 이를 토큰으로 교환하고 요청에 Bearer 인증을 붙인다. 401에서 앱은 갱신을 직렬화하고 토큰 쌍을 교체한 뒤 한 번 재시도한다. 로그아웃은 현재 기기의 갱신 세션을 폐기한다.

## 설계 대안

정책 변경과 과거 방식은 [인증 ADR](../../decisions/0004-oauth-session-redesign.md)과 [개인정보 ADR](../../decisions/0005-member-privacy-and-withdrawal.md)에 있다.

## 데이터 모델 및 API 계약

회원 식별자는 `provider` + `providerId`다. 이메일 중복 정책과 프로필 필드는 [데이터 모델](../../architecture/DATA_MODEL.md), 인증 교환·조회·수정·탈퇴 계약은 [API 목록](../../api/README.md)에 있다.

## 예외 처리 및 보안

다른 제공자로 이미 가입한 이메일에는 별도 오류를 반환한다. 만료되거나 이미 사용된 교환 코드는 401이다. 탈퇴 시 저장된 운동·프로그램·개인 종목·인증 관련 데이터를 트랜잭션으로 정리한다. 기존 데이터에 남은 타인 참조가 있으면 409로 중단하고 전체를 롤백한다. 약관과 개인정보처리방침의 실제 문의처 값은 확인이 필요하다.

## 테스트 계획

`AuthIntegrationTest`, `OAuthLoginIntegrationTest`, `TokenProviderTest`, `MemberWithdrawalIntegrationTest`와 출시용 두 공급자 로그인 흐름을 확인한다.

## 위험 및 롤백

인증 포맷 및 마이그레이션이 바뀌는 배포의 호환성과 구버전 세션은 [런북](../../operations/RUNBOOK.md) 기준으로 검토한다. 탈퇴로 파기한 레코드에 대해 애플리케이션 복구 경로는 확인되지 않았다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Obsidian `기획.md`, `TECH_SPEC.md`, `history/2026-03-17.md` 및 서버·웹 main |
| 관련 기능 또는 Issue | A-1–A-2, [서버 PR #28](https://github.com/pby1360/fitlog-v2-server/pull/28), [웹 PR #26](https://github.com/pby1360/fitlog-v2-web/pull/26) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [백엔드](../../architecture/BACKEND.md), [프런트엔드](../../architecture/FRONTEND.md) |
