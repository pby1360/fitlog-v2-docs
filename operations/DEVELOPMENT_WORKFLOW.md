# 개발 작업 등록과 실행

[TASKS](../status/TASKS.md)의 `main`이 작업 실행 상태의 원본이다. [BACKLOG](../status/BACKLOG.md)는 요구사항·우선순위·완료 조건, [CURRENT_STATUS](../status/CURRENT_STATUS.md)는 구현과 검증 근거, [ROADMAP](../product/ROADMAP.md)은 마일스톤을 관리한다. 각 상태 변경은 Docs PR의 변경 이력과 `main`의 병합 SHA로 추적한다. 날짜·시각은 `Asia/Seoul`의 `YYYY-MM-DDTHH:mm:ss+09:00`으로 기록한다. 기존 기록에서 정확한 시각을 확인할 수 없으면 `미확인`으로 남긴다.

## 신규 기능과 실행 대기열

1. [신규 기능 아이디어](../product/FEATURE_IDEAS.md)에서 제안을 등록하고 검토 상태를 관리한다. 사용자가 요청하면 기존 PRD·Tech Spec 템플릿으로 구체화한다. 제품 정책·범위, 의존성, 수용 기준과 구현·테스트 범위를 확인한 뒤 사용자에게 승인 근거를 받는다.
2. 승인된 기능을 같은 ID로 BACKLOG의 P0~P3에 올린다. 명세를 Docs `main`에 반영하고 확정한 PRD·Tech Spec 두 파일이 포함된 전체 커밋 SHA를 기록한다. 자동 개발을 허용하는 승인 기록에는 Task ID, 그 SHA, 대상 저장소와 자동 개발 허용 범위를 명시한다.
3. [WORK_QUEUE](../status/WORK_QUEUE.yaml)에 항목이 필요하면 [스키마](../status/WORK_QUEUE.schema.json)에 맞춰 별도 Docs PR로 등록한다. 처음 `READY`에 등록하려면 같은 Task ID가 TASKS에서 `APPROVED`여야 한다. `backlog_ref`, `prd_ref`, `tech_spec_ref`는 저장소 루트 기준이다. 백로그 링크의 `#p0`~`#p3`와 각 우선순위 표의 실제 Task ID를 대조한다. `depends_on`은 선행 Task ID의 목록이며, 완료 기준은 TASKS의 코드·문서 병합 근거를 갖춘 `DONE`이다.

아래는 대기열 `tasks`에 적는 항목의 형식 예시다.

```yaml
- task_id: FEAT-0001
  backlog_ref: status/BACKLOG.md#p2
  prd_ref: features/example/PRD.md
  tech_spec_ref: features/example/TECH_SPEC.md
  repositories: [pby1360/fitlog-v2-web]
  priority: P2
  auto_development_allowed: false
  approval_ref: null
  approved_spec_sha: null
  depends_on: []
  state: WAITING
```

| 대기열 상태 | 의미 |
| --- | --- |
| `WAITING` | 백로그 등록 후 자동 개발 승인, 명세 확정 또는 선행 조건을 기다린다. |
| `READY` | 사용자 승인 근거, 확정 PRD·Tech Spec과 변경 없는 승인 SHA, 명확한 대상 저장소, 선행 작업 `DONE`, `auto_development_allowed: true`를 모두 확인했다. |
| `HOLD` | 승인 철회, 명세 변경 또는 차단 사유가 있다. 다시 편입하려면 최신 근거를 검증한다. |
| `REMOVED` | 완료·취소·제외로 대기열에서 내려 감사 기록만 남긴다. |

대기열 상태는 후보 편입 여부를 나타낸다. 실행 상태와 선점은 TASKS에서 확인한다. 승인 명세 SHA는 현재 Docs `main`의 조상이어야 하고 현재 PRD·Tech Spec의 내용이 승인 때와 일치해야 한다. 두 명세 파일 중 하나라도 바뀌면 후보에서 제외하고 사용자에게 재승인을 받는다. 그 밖의 문서만 바뀐 커밋은 기존 명세 승인을 유지할 수 있다. 승인 기록의 SHA·대상 저장소를 대기열에서 바꾸면 원래 승인과 일치하는지 다시 확인한다.

### 후보 선택과 검증

1. 한 번의 선택은 최신 Docs `main` SHA로 모두 고정한다. TASKS의 `STARTING`, `IN_PROGRESS`, `PR_OPEN`과 실행 여부가 불확실한 `BLOCKED`를 먼저 확인한다. 대상 저장소의 Task ID가 연결된 기존 PR·CI, 접근 가능한 실행 목록과 대조한다. 활동 중인 작업이 있거나 상태 조회 결과를 신뢰할 수 없으면 새 작업 선택을 보류한다.
2. `READY` 중 TASKS가 `APPROVED`인 작업만 고려한다. 신뢰할 수 있는 승인 원본에서 승인자, 적용 범위, Task ID, 승인 SHA, 대상 저장소와 자동 개발 허용을 교차 확인한다. YAML의 링크와 상태는 교차 확인할 입력이다. 의존과 명세의 내용도 확인한다. 실행 인터페이스가 연결돼 있는지 확인할 수 없으면 실행 후보를 정하지 않는다.
3. 검증을 통과한 작업 중 `P0`부터 `P3` 순서로 한 건을 선정한다. 같은 우선순위에서는 Task ID 오름차순을 사용한다. 예약 점검은 보고만 남긴다. 이후 별도로 승인·연결된 실행 워커가 있다면 최신 근거를 재검증하고 [승인과 선점](#승인과-선점) 절차를 거친다. 자기 선점으로 `STARTING`이 반영되기 전에는 실행 요청을 보내지 않는다.

초기 대기열은 비어 있다. [로컬 검사기](../scripts/validate_work_queue.py)는 특정 Git 스냅샷의 스키마, 중복 ID, 백로그·명세 참조, 의존 상태 및 승인 SHA를 검사한다. 관련 Docs PR에도 동일한 검사를 실행한다. 후보 함수에는 승인 원본 및 활동 조회를 별도 검증한 입력이 필요하다. 검사 CLI는 GitHub나 Cloud에 요청을 보내지 않는다.

```sh
python -m pip install -r scripts/work-queue-requirements.txt
python scripts/validate_work_queue.py HEAD
PYTHONPATH=scripts python -m unittest discover -s tests
```

## 상태와 전이

| 상태 | 진입 조건 | 허용되는 다음 상태 |
| --- | --- | --- |
| `TODO` | Task ID가 배정됐으며 아직 착수 후보로 제출되지 않았다. | `PROPOSED`, `CANCELLED` |
| `PROPOSED` | 범위, 대상 저장소, 완료 조건을 연결했고 사용자 승인을 기다린다. | `APPROVED`, `TODO`, `CANCELLED` |
| `APPROVED` | 해당 범위의 사용자 승인 근거와 시각, 대상 저장소를 기록했다. 아직 실행 요청을 보내지 않았다. | `STARTING`, `BLOCKED`, `CANCELLED` |
| `STARTING` | 해당 Task ID의 선점 ID, 담당자, 대상, 기준 SHA를 담은 PR이 Docs `main`에 반영됐다. Cloud 실행을 준비한다. | `IN_PROGRESS`, `BLOCKED`, `CANCELLED` |
| `IN_PROGRESS` | 실제 Cloud 실행 ID 또는 해당 선점과 연결된 실행 시작 근거가 있다. 시작 시각과 작업 브랜치를 기록한다. | `PR_OPEN`, `BLOCKED`, `CANCELLED` |
| `PR_OPEN` | 코드 Draft PR을 생성하고 GitHub에서 확인했다. 문서 작업만 하는 경우 대상 Docs Draft PR로 같은 상태를 기록한다. 검토에 필요한 PR과 검증 근거를 연결한다. | `DONE`, `BLOCKED`, `CANCELLED` |
| `BLOCKED` | 실패·환경 오류·추가 승인 또는 실행/병합을 확인할 수 없는 이유와 마지막으로 확인한 상태를 기록했다. | `APPROVED`, `IN_PROGRESS`, `PR_OPEN`, `DONE`, `CANCELLED` |
| `DONE` | 코드 PR의 실제 병합 SHA와 필요한 Docs 동기화까지 `main`에서 확인했다. Docs 전용 작업은 대상 문서 병합을 확인했다. | 후속 작업은 새 Task ID로 등록한다. |
| `CANCELLED` | 사용자의 취소 근거를 확인했다. 이미 시작한 실행은 중단 여부와 남은 PR 처리를 확인했다. | 다시 요청되면 새 Task ID로 등록한다. |

신규 Task는 대기 또는 승인 요청 여부에 따라 `TODO`나 `PROPOSED`로 등록한다. 등록 전 이미 사용자 승인을 확인한 경우 승인 근거와 함께 `APPROVED`로 등록할 수 있다. 범위 변경으로 승인이 무효가 되면 `BLOCKED`에 이유를 남긴다. 새 실행이 필요하면 사용자 승인 후 `APPROVED`로 돌아가 새 선점 ID를 발급한다. `BLOCKED`에서 `IN_PROGRESS`로 복귀하는 경우는 기존 실행이 같은 선점에서 실제로 진행 중임을 확인했을 때다. 기존 PR이 검토 가능해졌으면 `PR_OPEN`으로 돌아간다. 코드와 필요한 Docs 병합이 모두 확인된 경우에는 `DONE`을 기록할 수 있다. 사용자가 취소했고 실행 중단을 확인할 수 없으면 `BLOCKED`로 두고 확인을 요청한다.

## 승인과 선점

1. 원격 Docs `main`의 최신 SHA와 `TASKS.md`를 읽는다. Task ID가 파일에서 한 번만 등장하는지와 대상 코드의 브랜치·열린 PR을 확인한다. 관련 PRD·Tech Spec과 사용자 승인 범위도 대조한다.
2. `APPROVED` 작업에 선점 ID를 하나 발급한다. 해당 Task가 `STARTING`, `IN_PROGRESS`, `PR_OPEN`이면 선점하지 않는다. Cloud 생성 요청의 응답이 불확실한 `BLOCKED`도 기존 실행 여부를 해결할 때까지 신규 선점을 차단한다.
3. 확인한 Docs `main`을 기준으로 독립 브랜치 `docs/task/<task-id>/<claim-id>`를 만든다. `APPROVED → STARTING`만 포함하는 커밋을 작성하고 Docs 상태 PR에 Task ID, 기대 이전 상태, 기준 `main` SHA, 사용자가 승인한 범위와 선점 ID를 연결한다.
4. 승인된 상태 전이 검증기가 있다면 최신 `main`의 기대 상태, Task ID 유일성, 선점 ID, 변경 파일과 PR head SHA를 검증한 뒤 병합한다. 검증과 반영 사이의 경쟁은 GitHub에서 최신 base를 강제하는 병합 규칙 또는 같은 보장을 제공하는 단일 직렬 병합 경로로 제어한다. PR 병합 API의 head SHA 검사는 변경된 base까지 검사하지 못한다. 자동 승인 경로가 미구성이라면 지정된 병합 담당자 한 명이 상태 PR을 한 건씩 처리한다. 담당자를 정하거나 병합을 직렬화할 수 없으면 선점을 보류한다.
5. PR이 병합된 후 병합 SHA가 원격 Docs `main`에 포함됐는지 조회한다. 다시 최신 `TASKS.md`를 읽어 그 Task ID의 상태가 `STARTING`이고 자신이 제출한 선점 ID·담당자가 맞는지 확인한다. 별도 체크아웃의 파일, 로컬 커밋, 열린 PR은 선점 근거로 사용할 수 없다. `main`에서 확인할 수 없으면 Cloud 실행을 요청하지 않는다.
6. Cloud 실행에는 Task ID와 선점 ID를 연계한다. 생성 요청 타임아웃이나 응답 유실 시, 같은 선점의 실행을 조회해 확인한다. 제공자가 중복 생성 방지를 지원하면 동일 선점 ID를 요청 키로 쓴다. 실행의 존재 여부가 미확인인 동안 재호출과 새 선점을 중지하고 `BLOCKED`에 사유를 남긴다.
7. 실행 ID 또는 해당 선점의 시작 근거를 확인한 뒤 상태 PR로 `IN_PROGRESS`를 기록한다. 근거는 Cloud 실행 링크나 시간과 실행 식별 정보를 확인할 수 있는 이벤트를 사용한다. 기록 갱신이 실패하면 이미 시작한 실행의 근거를 보존하고 같은 선점의 상태만 복구한다.

기준 `main`이 바뀌거나 상태 PR이 충돌하면 최신 `main`의 Task ID·상태·선점 ID부터 재조회한다. 다른 실행이 먼저 선점했으면 자신의 PR을 정리하고 중단한다. 작업이 여전히 `APPROVED`이고 선점이 없다면 새 base에서 검증을 다시 받는다. 서로 다른 Task ID라도 같은 Docs `main`을 갱신하므로 오래된 검사를 재사용하지 않는다.

## 진행 및 종료

- 코드는 대상 저장소의 `AGENTS.md`와 `fitlog-loop`를 적용한다. `IN_PROGRESS`는 실행 ID 또는 실행 시작 증거, 작업 브랜치, 담당자를 연결한다. 코드 Draft PR이 열리면 `PR_OPEN` 상태 PR에서 해당 PR과 Docs PR을 기록한다. 검증이나 추가 승인이 막히면 `BLOCKED`에 사유와 마지막 증거를 남긴다.
- 코드 PR은 사용자 승인 후 수동 병합한다. 병합 SHA를 GitHub에서 확인하고 영향받는 Tech Spec·API·아키텍처와 BACKLOG, CURRENT_STATUS, 날짜별 이력을 갱신한다. 코드 PR과 구현 Docs PR을 상호 연결하고, 갱신이 필요 없는 경우 코드 PR에 그 이유를 기록한다. [코드·문서 동기화](DOCS_SYNC.md)
- 필요한 문서가 `main`에 반영된 다음 `DONE` 상태 PR에 코드·문서 병합 근거와 완료 시각을 기록한다. `DONE`은 등록한 작업의 완료이며, 운영 배포 및 실제 데이터·기기 검증은 확인한 경우에만 [현재 상태](../status/CURRENT_STATUS.md)의 운영 근거로 기록한다. 배포 권한은 [배포 절차](DEPLOYMENT.md)를 따른다.

## 자동화와 수동 개입

병합된 구현을 검증하는 Docs 동기화는 기존 [워크플로](DOCS_SYNC.md)의 허용 파일에 `TASKS.md`를 포함하지 않는다. 따라서 선점과 작업 상태 전이는 별도 상태 PR로 처리한다. 현재 등록 양식과 절차를 정의했으며, 상태 전이 자동 병합과 예약 점검 설정은 확인되지 않았다. GitHub App 설치가 필요한 기존 구현 동기화도 실제 교차 저장소 실행 확인이 필요하다.

자동화 승인 범위는 최신 base를 기준으로 이미 승인된 Task의 `TASKS.md` 필드와 허용 전이만 적용하는 작업이다. 새 요구사항·우선순위·보안 정책·제품 범위·아키텍처 결정과 새로운 개발 승인은 기존 사용자 승인 경로를 따른다. 자동화가 없거나 실패하면 사용자 또는 승인된 담당자가 상태 PR에서 기대 상태·base SHA를 다시 확인해 병합한다. 병합 또는 선점 확인이 끝날 때까지 신규 실행을 차단한다. 운영 접근은 상태 기록으로 승인되지 않는다.

후속 구현에는 상태 PR 전용 검증 및 병합 경로, 동일 Task의 동시 병합 테스트, 실행 생성의 중복 요청 방지와 조회, 3시간 예약 점검 및 연속 관측 기록을 포함한다. 승인된 코드 병합으로 발생하는 문서 검사와 작업 선점은 별도 워크플로로 관리한다.

## 3시간 예약 점검

예약 점검은 설정 후 3시간 간격으로 읽기 전용 실행한다. 우선 Docs `main`의 TASKS를 기준으로 `STARTING`, `IN_PROGRESS`, `PR_OPEN`, `BLOCKED`의 마지막 갱신과 근거를 읽고 GitHub PR·CI 상태를 대조한다. 접근 가능한 경우 Cloud 실행 ID 및 실행 상태를 확인한다. 권한 또는 근거가 없으면 `미확인`으로 보고한다.

Task별 직전 관측의 상태·마지막 갱신 시각·선점 ID를 별도의 관측 기록과 비교한다. 기준 스냅샷 이후 두 번 연속 갱신이 관찰되지 않거나 실제 실행 상태와 기록이 충돌하면 사용자 확인이 필요하다고 보고한다. 보고에는 Task ID, 관련 PR·CI, 마지막 증거, 점검 시각과 충돌 내용을 포함한다. 관측 결과만으로 `DONE` 또는 `CANCELLED`로 전이하거나 실행을 재시작하지 않는다. 점검은 TASKS와 Git 브랜치를 직접 수정하지 않는다.

## Codex Cloud 연동 계획

- 저장된 `fitlog-v2` 환경을 환경 목록에서 확인했다. 공식 CLI는 실험 기능인 `codex cloud exec`로 작업 생성, `codex cloud list --json`으로 목록 조회를 지원한다. 설치된 CLI 도움말은 작업 ID를 받는 `codex cloud status`도 제공한다. 현재 실행 환경에서 읽기 전용 `list` 요청은 연결 실패로 응답을 확인하지 못했다. 환경 목록 노출만으로 CLI 인증, 조회 권한이나 생성 성공을 보장할 수 없다. 이 환경의 작업 생성·조회에 사용할 안정적인 공개 REST 계약이나 제공자 차원의 중복 요청 키는 확인되지 않았다. [OpenAI CLI 명령 참고](https://developers.openai.com/codex/cli/reference#codex-cloud)
- 연동 전 운영 담당자는 실행 워커의 승인된 CLI 로그인과 대상 환경 접근 범위를 확인한다. 워커에는 Docs·대상 코드의 조회, 승인된 브랜치와 Draft PR에 필요한 GitHub 권한만 제공한다. main 직접 푸시, 코드 PR 병합, 운영 배포 자격증명은 부여하지 않는다. 자격증명은 승인된 시크릿 저장소에 보관한다.
- 실행 워커는 `(Task ID, 선점 ID)`를 유일 키로 둔 내구성 있는 기록에 요청 상태와 제공자 작업 ID를 보존한다. 작업 브랜치, 확정 명세와 선점 ID를 실행 입력에 포함한다. 요청 성공 후 작업 ID로 상태를 조회해 시작 근거를 확인한다. 응답 유실 시 같은 키의 기존 작업을 확인하기 전 재요청하지 않는다. 작업 존재나 결과가 불확실하면 승인된 담당자가 `BLOCKED`로 기록하고 복구한다.
- CLI 로그인이 가능한 실행 환경에서도 연결·조회·취소 복구를 비운영 테스트로 먼저 확인한다. 해당 인터페이스를 신뢰할 수 없다면 승인된 별도 워커에서 비대화형 `codex exec`를 사용하고 워커가 실행 ID·상태를 관리하는 방안을 검토한다. 이 경로는 별도 실행 인프라를 사용하므로 Codex Cloud 작업 ID로 기록하지 않는다. 실행 연동 도입 전까지는 읽기 전용 예약 점검과 승인된 담당자의 수동 선점 절차를 사용한다. [OpenAI 비대화형 실행 문서](https://developers.openai.com/codex/noninteractive)

| 추적 정보 | 내용 |
| --- | --- |
| 문서 상태 | 검토 중 |
| 원본 출처 | Docs 중심 작업 상태 관리 요청, 개발 규칙 및 코드·문서 동기화 절차 |
| 관련 기능 또는 Issue | [작업 실행 현황](../status/TASKS.md), [백로그](../status/BACKLOG.md) |
| 최종 검증일 | 2026-11-19 |
| 관련 설계 | [문서 관리 규칙](../AGENTS.md), [코드·문서 동기화](DOCS_SYNC.md), [배포](DEPLOYMENT.md) |
