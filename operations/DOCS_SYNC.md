# 코드와 문서 동기화

## 개발과 병합 순서

1. 승인된 기능의 코드 PR을 연다. 영향을 받는 Tech Spec·API·아키텍처, 현재 상태·백로그, 한국 시간 날짜의 개발 이력을 갱신한다. 문서 영향이 없으면 코드 PR에 이유를 남긴다.
2. 코드 PR이 있으면 문서 저장소의 최신 `main`에서 `docs/sync/<code-repo>-<pr-number>` 브랜치를 사용한다. 같은 브랜치의 Docs PR이 있으면 기존 PR을 갱신한다. 같은 날짜 파일에는 코드 PR별 항목을 한 번만 작성한다.
3. 두 PR 본문에 서로의 실제 URL을 연결한다. Docs PR 본문에는 아래 두 줄을 정확히 한 번 작성한다. 기준 SHA는 문서를 작성할 때 확인한 코드 PR의 대상 브랜치 커밋이다.

   ```text
   Docs-Sync-Source: pby1360/fitlog-v2-web#<code-pr-number>
   Docs-Sync-Base: <40-character-code-base-sha>
   ```

4. 문서에 상태, 원본, 관련 기능 또는 Issue, 최종 검증일, 관련 설계를 적는다. 현재 상태와 날짜별 이력은 실제로 바뀐 코드 파일을 전체 커밋 SHA로 고정해 링크한다. 코드 PR의 head는 최종 병합 파일과 동일한 경우에 사용할 수 있다. 로컬 검사와 운영 검증을 구분한다.
5. 사용자가 코드를 승인하면 검토한 Docs PR의 정확한 SHA도 함께 확인한다. 구현 동기화만 포함된 Docs PR을 Ready로 전환하고, 승인된 사람이 코드 PR을 **Create a merge commit** 방식으로 병합한다. 코드 PR **본문**에는 링크만 둔다. 병합 메시지의 마지막 문단에 승인한 Docs PR 번호와 전체 SHA를 직접 기록한다.

   ```text
   Docs-Sync-Kind: implementation
   Docs-Sync-PR: <docs-pr-number>
   Docs-Sync-Head: <40-character-docs-head-sha>
   ```

   코드 병합 메시지에 위 항목이 없는 경우 Docs 자동 병합 요청이 발생하지 않는다. GitHub 병합 메시지 기본값은 PR 본문을 복사하지 않도록 설정한다. PR 제목이나 본문에 위 필드를 넣은 경우 자동 병합 검사가 차단한다. 새로운 요구사항, 제품 범위, 보안 정책, 설계 또는 아키텍처 결정이 포함되면 문서를 별도 승인 경로에 둔다.

## GitHub 설정

저장소 관리자가 자동화 PR을 검토하고 병합할 때 다음 GitHub App과 저장소 변수를 구성한다. 각 App의 설치 저장소를 표에 나온 범위로 제한한다. 개인 토큰을 사용하지 않으며 비공개 키는 GitHub Actions 시크릿에만 저장한다.

| App 역할 | 설치 범위와 저장소 권한 | 저장소 Variables 및 Secrets |
| --- | --- | --- |
| FitLog Docs Dispatch | `fitlog-v2-docs`만 설치. `Contents: write`는 GitHub의 `repository_dispatch` API에 필요하다. | 서버·웹 각각 `FITLOG_DOCS_DISPATCH_APP_ID`를 변수에, `FITLOG_DOCS_DISPATCH_APP_PRIVATE_KEY`를 시크릿에 등록한다. |
| FitLog Docs Read | 서버·웹에만 설치. `Contents: read`, `Pull requests: read`로 병합 커밋과 변경 파일을 읽는다. | Docs의 변수 `FITLOG_DOCS_READ_APP_ID`, 시크릿 `FITLOG_DOCS_READ_APP_PRIVATE_KEY`를 등록한다. |

발급 토큰은 사용 저장소 하나와 필요한 권한으로 한정한다. Docs 병합은 Docs 워크플로의 `GITHUB_TOKEN`으로 수행하며 그 저장소의 병합 규칙을 따른다. 코드 저장소의 쓰기 권한을 부여하지 않는다. Docs의 merge-commit 방식이 허용되어야 하고, 브랜치 보호가 추가 사람 리뷰나 별도 체크를 요구하면 GitHub가 자동 병합을 거부한다. 브랜치 보호의 최신 기준 요구는 검증 중 사람이 별도로 Docs main을 병합하는 경우도 막아 준다.

## 자동 검사 범위

- 코드의 main 병합 이벤트는 승인 표시가 있는 경우 Docs에 신호를 전송한다. Docs는 신호에 쓰인 코드 PR과 실제 병합 커밋·부모·main 이력을 GitHub에서 재검증한다.
- 자동 후보는 정확한 승인 SHA와 같은 저장소의 열린 Ready Docs PR이다. 현재 상태, 백로그 및 날짜별 이력 1개를 포함해야 한다. Tech Spec·API·지정된 아키텍처 문서는 승인된 구현 동기화로만 포함한다. 요구사항·정책·ADR·자동화 파일, 삭제·이름 변경과 실행 파일은 수동 승인 대상으로 남는다.
- 필수 문서 구조, 본문 상대 링크와 앵커, HTTPS 링크 형식, 병합된 코드 파일의 참조, 비밀정보 검사를 실행한다. 원시 HTML은 수동으로 검토하고 외부 HTTPS 링크는 형식만 확인한다. 코드 승인 시 Docs 후보가 구현 동기화만 포함하는지 확인한다.
- GitHub의 PR 병합 API에 검증한 Docs head SHA를 전달한다. 이전 이벤트가 이미 병합한 PR이면 그대로 종료한다. 자동화는 Docs PR이나 이력 파일을 생성하지 않는다.

## 실패 처리

Docs 브랜치나 main이 바뀌면 검증은 실패한다. 변경을 그대로 검토할 수 있으면 재실행한다. 검토 내용이나 SHA를 고쳐야 하면 승인된 수동 Docs PR로 처리한다. 이미 병합된 코드 PR을 다시 병합하지 않는다. 자동화 파일을 변경하는 PR은 읽기 전용 워크플로에서 GitHub API 픽스처를 실행한다. 로컬에서는 `scripts/docs-sync-requirements.txt` 설치 후 `python -m unittest discover -s scripts`로 같은 검사를 실행한다.

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | 문서 자동 동기화 요청 |
| 관련 기능 또는 Issue | [백로그](../status/BACKLOG.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [문서 규칙](../AGENTS.md), [시스템 개요](../architecture/SYSTEM_OVERVIEW.md) |
