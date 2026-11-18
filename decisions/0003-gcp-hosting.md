# ADR 0003 · GCP 호스팅 전환

## 배경

초기 배포는 Vercel·Render 기반이었다. 2026-01-06에는 Render의 지연을 근거로 AWS EC2 전환을, 03-22에는 웹 S3·CloudFront 전환을 기록했다. 이후 고정비와 운영 복잡도가 다시 검토됐다.

## 결정

2026-07-30 Cloud Run, Artifact Registry, Firebase Hosting, Secret Manager로 전환하고 PostgreSQL은 Supabase에서 유지하기로 결정했다. 8월 이관 기록은 Cloudflare를 통한 커스텀 도메인 연결을 남겼다.

## 고려한 대안

Render·Vercel 유지, AWS EC2와 S3·CloudFront, 관리형 DB 이관, 오브젝트 스토리지와 별도 외부 로드 밸런서. 단일 환경과 로컬 검증을 선택하고 별도 알파 환경은 보류했다.

## 결정 근거

낮은 트래픽에서 Cloud Run의 0 인스턴스까지 축소, Firebase Hosting의 CDN·TLS, 기존 서울 DB 재사용으로 운영 고정비를 줄인다.

## 영향

프런트와 서버의 배포 경로를 분리하고 WIF를 사용한다. 구 플랫폼 정리는 롤백 경로를 확인한 후에 하도록 기록됐다. 구 플랫폼 정리 및 현행 정책 적용 여부는 추가 확인 항목이다.

## 관련 문서

[배포](../operations/DEPLOYMENT.md), [런북](../operations/RUNBOOK.md), [백로그](../status/BACKLOG.md)

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 확정 (이관 기록) |
| 원본 출처 | Obsidian `fitlog-v2-MoC.md`, `TASKS.md` P1 및 폐기된 결정, `배포.md` |
| 관련 기능 또는 Issue | M2–M3 |
| 최종 검증일 | 2026-11-18 |
| 관련 설계 | [시스템 개요](../architecture/SYSTEM_OVERVIEW.md), [배포](../operations/DEPLOYMENT.md) |
