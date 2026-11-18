# FitLog 문서 관리 규칙

## 작업 전

1. [기능 목록](features/README.md)에서 해당 PRD와 Tech Spec을 읽고 관련 ADR과 Issue를 확인한다. 여러 기능에 걸친 계약은 [시스템 개요](architecture/SYSTEM_OVERVIEW.md)와 [API 목록](api/README.md)을 함께 확인한다.
2. 제품 범위는 [요구사항](product/REQUIREMENTS.md)과 PRD에서 확인한다. 사용자 승인 전에는 신규·변경 요구사항을 초안으로 기록한다. 기획과 구현이 다르면 원본 날짜, 결정 근거, 코드 커밋을 남긴다.

## 작업 중

3. 코드 변경으로 영향받는 원본 문서를 갱신한다. 제품 범위는 `product/`, 기능별 행위와 설계는 `features/`, 공유 기술 계약은 `architecture/`와 `api/`, 배포와 대응 절차는 `operations/`에 둔다. 다른 문서는 상대 링크로 연결한다.
4. 유지 비용, 보안, 데이터 수명, 인터페이스 또는 아키텍처에 장기 영향을 주는 결정은 [ADR 템플릿](templates/ADR_TEMPLATE.md)으로 작성한다. 기존 결정이 바뀌면 후속 ADR을 연결한다.
5. 코드 저장소의 `main`을 직접 수정하지 않는다. 운영 환경 접근 및 배포를 금지한다.

## 작업 후

6. 구현 상태를 변경할 때 코드 커밋, 확인한 경로, 테스트 범위를 [현재 상태](status/CURRENT_STATUS.md)에 남긴다. 실행 검증이 빠진 범위는 명시하고, 근거가 없는 항목을 완료로 표시하지 않는다.
7. [백로그](status/BACKLOG.md)에는 남은 일과 추가 확인 사항을 유지하고, 결정과 날짜별 변경은 [개발 이력](history/README.md)에 남긴다. PR에 변경 문서, 관련 기능 또는 Issue, 근거, 검증 결과와 미확인 항목을 기록한다.
8. 문서에 상태, 원본 출처, 관련 기능 또는 Issue, 최종 검증일, 관련 설계를 기록한다. 신규 문서는 [PRD](templates/PRD_TEMPLATE.md), [Tech Spec](templates/TECH_SPEC_TEMPLATE.md), [ADR](templates/ADR_TEMPLATE.md) 템플릿 중 해당 양식을 사용한다.
9. 공개 문서 게시 전 로컬 상대 링크, 상호 참조, 템플릿, 중복과 충돌, 코드 정합성, 비밀정보 포함 여부를 확인한다. 설정 백업과 자격증명은 저장소에 이관하지 않는다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | 문서 체계 구축 요청 및 Obsidian `fitlog-v2-MoC.md`의 유지 루틴 |
| 관련 기능 또는 Issue | [전체 기능](features/README.md) |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [시스템 개요](architecture/SYSTEM_OVERVIEW.md), [이관 기록](history/MIGRATION.md) |
