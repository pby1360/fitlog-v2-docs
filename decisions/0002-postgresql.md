# ADR 0002 · PostgreSQL 선택

## 배경

회원·프로그램·세션의 연관 관계가 필요하며 v2에서 구조화된 분석 결과를 저장할 가능성이 있었다.

## 결정

2025-11-06 결정 이력에서 PostgreSQL을 선택했다. 현재 서버는 Flyway와 JPA로 스키마를 다룬다.

## 고려한 대안

이관 원본에 2025-11-06 결정의 후보 DB 목록은 없다. 이후 배포 검토에서 Supabase 유지와 별도 관리형 DB 이관을 비교했다.

## 결정 근거

관계형 제약과 통계 처리, 향후 가변 분석 레코드의 JSONB 사용 가능성이다. 서울 리전의 Supabase를 유지한 이유는 기존 연결 검증과 이관 비용이었다.

## 영향

애플리케이션의 관계·제약과 테스트를 PostgreSQL 기준으로 관리한다. AI용 JSONB는 현재 계획에 속한다.

## 관련 문서

[데이터 모델](../architecture/DATA_MODEL.md), [AI 설계](../features/ai-coaching/TECH_SPEC.md), [호스팅 ADR](0003-gcp-hosting.md)

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 확정 (이관 기록) |
| 원본 출처 | Obsidian `fitlog-v2-MoC.md`의 2025-11-06 결정, `기획.md`, `TASKS.md` |
| 관련 기능 또는 Issue | B-1–E-4 |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [데이터 모델](../architecture/DATA_MODEL.md) |
