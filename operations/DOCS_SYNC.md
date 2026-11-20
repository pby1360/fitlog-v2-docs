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

### 2026-11-19 동기화 장애 및 복구

- **FAILED.** 웹 #44의 병합 메시지에서 승인 표시는 인식됐다. 다음 단계인 토큰 발급에서 `[@octokit/auth-app] appId option is required`가 발생했고 Dispatch 단계가 생략됐다. 따라서 이 실행에서 Docs 수신·검증은 시작되지 않았다. Docs #11은 승인된 커밋을 재검증해 수동 병합했다. [웹 실패 실행](https://github.com/pby1360/fitlog-v2-web/actions/runs/44462060315) · [Docs #11](https://github.com/pby1360/fitlog-v2-docs/pull/11)
- **VERIFIED.** 웹·서버의 발신 잡은 `vars.FITLOG_DOCS_DISPATCH_APP_ID`를 고정 버전 토큰 액션의 `app-id`로 전달한다. 해당 액션은 이 입력을 읽어 Octokit에 전달한다. 실패한 실행에서 유효한 App ID 입력을 받지 못했다는 점은 확인됐다. 변수 자체의 미등록, 조직 정책의 저장소 제외, 잡에 연결되지 않은 Environment 범위 등 실제 설정은 관리자 권한으로 확인한다. [웹 발신 워크플로](https://github.com/pby1360/fitlog-v2-web/blob/4ae88e1333ef1d7d2af2d436f1a8df8ea2c2d5d6/.github/workflows/docs-sync.yml) · [서버 발신 워크플로](https://github.com/pby1360/fitlog-v2-server/blob/6d1c7ba7f227b3b6087e2033b1e74213f25fa708/.github/workflows/docs-sync.yml) · [토큰 액션의 입력 읽기](https://github.com/actions/create-github-app-token/blob/fee1f7d63c2ff003460e3d139729b119787bc349/main.js)
- **VERIFIED.** 발신 요청과 Docs 워크플로가 모두 `fitlog-code-merged`를 사용한다. payload의 저장소, PR 번호, 병합 SHA를 Docs 검증기가 다시 확인한다. 일반 병합의 발신 워크플로가 성공해도 토큰·Dispatch 단계가 생략됐다면 연동 성공 근거가 없다. [Docs 수신 워크플로](../.github/workflows/docs-sync.yml) · [서버 발신 생략 사례](https://github.com/pby1360/fitlog-v2-server/actions/runs/44450257956)
- **UNVERIFIED.** 세 저장소의 Actions 변수·Secret 이름 등록 여부, 두 App의 실제 설치·권한, 조직 정책, Docs main 보호와 워크플로 토큰의 병합 권한은 확인할 수 없었다. 연결 도구가 변수·Secret·설치 조회를 지원하지 않았고 branch protection은 403이었다. 기존 GitHub App 설정을 확인할 때까지 워크플로 수정 근거는 없다.

토큰 액션이 고정한 Octokit 8.2.0에서 App ID 누락과 개인 키 누락 메시지를 각각 오프라인에서 재현했다. 두 발신 스크립트의 정상 트레일러, 무승인, PR 제목·본문 삽입 차단과 수신 검증기의 SHA 불일치, 중복 이벤트, 잘못된 저장소·PR 및 HTTP 403 처리를 확인했다. 기존 Docs 동기화 픽스처는 19개가 통과했다.

#### 저장소 관리자 확인

1. GitHub App **Dispatch**를 Docs 저장소에만 설치하고 저장소 권한 `Contents: write`를 부여한다. Web과 Server의 **Settings → Secrets and variables → Actions**에서 각각 **Variables**에 `FITLOG_DOCS_DISPATCH_APP_ID`, **Secrets**에 해당 App의 `FITLOG_DOCS_DISPATCH_APP_PRIVATE_KEY`를 등록한다. GitHub App **App ID**를 사용한다. 조직 항목을 쓴다면 각 저장소가 허용 대상인지 확인한다. 현재 잡에는 `environment`가 없으므로 환경 전용 설정은 전달되지 않는다.
2. 별도 **Docs Read** App을 Web·Server에만 설치하고 `Contents: read`, `Pull requests: read`를 부여한다. Docs의 Actions 저장소 변수 `FITLOG_DOCS_READ_APP_ID`와 저장소 시크릿 `FITLOG_DOCS_READ_APP_PRIVATE_KEY`를 해당 App과 일치시킨다. Web·Server 코드 저장소의 쓰기 권한은 필요 없다.
3. Docs에서 merge commit 허용 및 Actions의 `GITHUB_TOKEN`에 요청한 `contents: write`를 허용하는 정책을 확인한다. 보호 규칙의 필수 리뷰, 최신 base, 필수 검사가 자동 병합 경로에서 충족되는지도 확인한다. 로그와 보고에는 설정 이름, 설치 대상, 권한만 남긴다.
4. 오류가 `privateKey` 입력 누락이면 Secret 등록 범위부터 확인한다. 토큰 발급의 401이면 App ID와 대응하는 키, 403·404이면 발급 또는 Dispatch 단계에서 거부된 저장소·App 설치·권한을 확인한다. Docs 병합 403·405·409이면 Docs 토큰 권한, 보호 규칙, base 및 승인 head를 확인한다. 실패한 요청의 본문이나 자격증명은 증빙에 포함하지 않는다.
5. 설정 확인 후 별도 승인된 테스트로 발신 토큰 발급, HTTP 204 Dispatch, 수신 검증, 정확한 Docs SHA 병합까지 확인한다. 해당 실험은 비운영 테스트 저장소에서 하며, 운영 코드 PR을 실험용으로 병합하지 않는다. 이미 병합된 Docs #11은 수동 복구 이력으로 보존한다. [검증 절차](DEVELOPMENT_WORKFLOW.md) · [GitHub App 권한](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app)

## DOCS-SYNC-02 후속 검증

| 검증 항목 | 판정과 근거 |
| --- | --- |
| Web → Docs 발신·수신 | `VERIFIED`. Web 발신 2회차에서 Dispatch App 발급 및 이벤트 전송, Docs 수신 3회차에서 Read App 발급과 입력 검증이 성공했다. [Web 발신](https://github.com/pby1360/fitlog-v2-web/actions/runs/44462060315/attempts/2) · [Docs 수신](https://github.com/pby1360/fitlog-v2-docs/actions/runs/44508885506/attempts/3) |
| 기존 병합·중복 처리 | `VERIFIED`. 실제 재실행의 Docs #11은 이미 병합됨을 확인하고 변경 없이 종료했다. 로컬에서는 같은 이벤트를 두 번 전달해 최초 요청만 정확한 SHA로 한 번 병합하는 것을 검증했다. [실행](https://github.com/pby1360/fitlog-v2-docs/actions/runs/44508885506/attempts/3) |
| Server → Docs 실전 발신 | `UNVERIFIED`. 확인한 서버 실행에서 Dispatch 토큰 발급과 전송이 생략됐다. 승인 트레일러가 있는 기존 병합이나 열린 구현 PR을 찾지 못했다. Server 응답을 모의한 수신 검증은 정확한 Docs SHA로 한 번만 병합을 요청한다. [Server 실행](https://github.com/pby1360/fitlog-v2-server/actions/runs/44450257956) |
| 신규 Docs PR 실전 병합 | `UNVERIFIED`. Web·Server 양쪽의 승인 근거와 정확한 SHA는 로컬에서 확인했다. 실제 새 PR과 Docs `GITHUB_TOKEN`의 보호 규칙 통과는 다음 승인된 구현 PR에서 확인한다. |
| 실패·경쟁 조건 | `VERIFIED`(로컬). 승인 누락, PR 본문 승인 토큰, SHA 불일치, PR 없음(404), 인증·권한 오류(401·403), 이미 병합됨, 중복, Docs base 분기 및 검증 도중 main 변경, 제품·정책 파일을 24개 테스트에서 확인했다. [회귀 픽스처](../scripts/test_docs_sync.py) |
| 토큰 권한 | `VERIFIED`(워크플로 정의). Dispatch 토큰은 Docs 한 저장소의 `Contents: write`, Read 토큰은 해당 코드 저장소 한 곳의 `Contents: read`와 `Pull requests: read`로 요청한다. 실제 App 설치 전체와 Server 토큰 발급은 후속 확인 대상이다. [발신 설정](https://github.com/pby1360/fitlog-v2-server/blob/6d1c7ba7f227b3b6087e2033b1e74213f25fa708/.github/workflows/docs-sync.yml) · [수신 설정](../.github/workflows/docs-sync.yml) |

### 다음 승인된 Server 구현 PR 검증 계획

1. 실제 구현과 문서 근거가 생긴 Server PR을 대상으로 한다. 양쪽 PR의 필수 검사, 배포 분류·영향, Docs 파일 범위와 현재 `main`을 확인한다. 사용자 승인에는 Server PR 병합과 정확한 Docs SHA를 포함한다. 기능 변경의 자동 배포가 예상되면 그 영향도 병합 전에 명시한다.
2. 같은 코드 PR에 연결된 Docs PR에 Source·Base를 기록하고 검토가 끝난 Docs head를 고정한다. Docs PR을 Ready로 바꾼 뒤, 승인된 Server 병합 커밋의 마지막 문단에 기존 세 트레일러를 넣는다. 권한은 기존 범위로 유지한다.
3. Server 발신 잡의 토큰 발급·Dispatch, Docs 수신 잡의 Server 토큰 발급·검증·정확한 head 병합 성공, Docs main 반영을 확인한다. 실행 URL과 병합 SHA를 남긴다. 이미 병합된 동일 이벤트는 추가 병합 없이 종료해야 한다. SHA·base가 움직이거나 정책에 막히면 해당 이유를 기록하고 재승인 없이 새 head를 적용하지 않는다.

운영 복구 기준이 확보되면 `V1-05 공용 운동 종목 확충`을 Server 실전 후보로 검토한다. V1-05 승인·구현 PR 생성·마이그레이션 전후 호환 검증 뒤에만 위 절차를 연결한다. Server PR 병합이 기능 자동 배포를 유발하는지 먼저 확인하고, 연결된 신규 Docs PR head를 승인받는다. 이번 증거 갱신은 Server 코드나 신규 Docs 자동 병합을 시작하는 근거가 아니다. [V1-05 백로그](../status/BACKLOG.md#p1)

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
| 최종 검증일 | 2026-11-20 |
| 관련 설계 | [문서 규칙](../AGENTS.md), [시스템 개요](../architecture/SYSTEM_OVERVIEW.md) |
