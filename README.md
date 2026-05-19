# Hiring Tracker CLI

간단한 Python CLI 프로그램으로 채용 후보자 정보를 기록하고 단계별로 추적할 수 있습니다. 모든 데이터는 JSON 파일(기본 `hiring_data.json`)에 저장되어 자동으로 로그가 남습니다.

## 주요 기능
- **DB 초기화:** 새 JSON DB 파일을 생성합니다.
- **후보자 등록:** 이름, 지원 포지션, 이메일, 소스를 기록하고 기본 단계(`applied`)로 저장합니다.
- **단계 이동:** `screen`, `onsite`, `offer` 등 원하는 단계로 옮기면서 변경 이력을 남깁니다.
- **노트 추가:** 면접 피드백 같은 메모를 후보자별로 추가합니다.
- **목록/이력 조회:** 후보자 목록과 개별 이벤트 히스토리를 확인합니다.

## 사용 방법
별도 빌드 과정은 없으며 Python 3.11+만 있으면 바로 실행할 수 있습니다. (빌드 명령어가 없다는 뜻이며, 바로 아래 실행 예시처럼 곧바로 실행하면 됩니다.)

### 빠른 시작
가장 빠르게 "프로그램을 만들고(=준비하고) 실행"하려면 아래 순서만 따르면 됩니다.

1) **코드 내려받기**: 저장소를 클론하고 폴더로 이동합니다.
2) **(선택) 가상환경**: `python -m venv .venv && source .venv/bin/activate` 로 격리된 환경을 만듭니다.
3) **즉시 실행**: 추가 의존성이 없으므로 바로 `python hiring_tracker.py --help` 또는 `python hiring_tracker.py init` 을 실행하면 준비가 끝납니다.

```bash
# 저장소 클론
git clone <repo-url>
cd 0G-zu

# (선택) 가상환경 생성 후 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 의존성: 표준 라이브러리만 사용하므로 추가 설치가 필요 없습니다.

# 사용법 확인
python hiring_tracker.py --help
```

### "빌드"에 해당하는 실행 명령 요약
이 프로젝트는 별도 빌드 단계를 두지 않으므로, 아래 실행 명령이 곧 빌드/실행 절차입니다.

```bash
# 데이터베이스 초기화 후 즉시 실행 예시
python hiring_tracker.py init
python hiring_tracker.py list
```

### Visual Studio Code에서 실행하기
빌드 단계 없이 VS Code 통합 터미널이나 Run/Debug 버튼으로 바로 실행할 수 있습니다.

1. VS Code로 폴더를 열고 Python 확장을 설치합니다.
2. 통합 터미널에서 `python hiring_tracker.py --help` 또는 아래 예시 명령을 그대로 실행합니다.
3. **Run and Debug** 뷰에서 제공되는 `Python: hiring_tracker.py (help)` 또는 `Python: hiring_tracker.py (init + list)` 구성을 선택하면 디버깅 모드로 즉시 실행할 수 있습니다. (`.vscode/launch.json`에 포함)

```bash
# VS Code 통합 터미널 예시
python hiring_tracker.py init
python hiring_tracker.py add --name "홍길동" --role "Backend Engineer" --email "hong@example.com" --source "LinkedIn"
python hiring_tracker.py list
```

### 기본 명령어 예시
```bash
# 데이터베이스 초기화
python hiring_tracker.py init

# 후보자 추가
python hiring_tracker.py add --name "홍길동" --role "Backend Engineer" --email "hong@example.com" --source "LinkedIn"

# 단계 이동
python hiring_tracker.py advance <candidate-id> --stage "onsite" --note "과제 제출 완료"

# 노트만 추가
python hiring_tracker.py note <candidate-id> --note "급여 협의 필요"

# 전체 목록 확인
python hiring_tracker.py list

# 특정 후보 히스토리 확인
python hiring_tracker.py history <candidate-id>
```

`--db` 옵션으로 다른 JSON 경로를 지정해 여러 채용 공고나 팀별로 별도 데이터 파일을 관리할 수 있습니다.

## 테스트 실행
표준 라이브러리의 `unittest`로 동작 확인이 가능합니다.

```bash
python -m unittest tests/test_hiring_tracker.py
```

## 데이터 구조 예시
`hiring_data.json` 예시 구조는 다음과 같습니다.

```json
{
  "candidates": {
    "<uuid>": {
      "id": "<uuid>",
      "name": "홍길동",
      "role": "Backend Engineer",
      "email": "hong@example.com",
      "source": "LinkedIn",
      "stage": "onsite",
      "created_at": "2024-07-01T12:00:00Z",
      "updated_at": "2024-07-02T09:30:00Z"
    }
  },
  "events": [
    {
      "candidate_id": "<uuid>",
      "type": "candidate_added",
      "summary": "Added candidate from LinkedIn",
      "note": null,
      "timestamp": "2024-07-01T12:00:00Z"
    },
    {
      "candidate_id": "<uuid>",
      "type": "stage_changed",
      "summary": "applied -> onsite",
      "note": "과제 제출 완료",
      "timestamp": "2024-07-02T09:30:00Z"
    }
  ]
}
```

## 개발 메모
- 데이터베이스 파일을 누락하면 자동으로 새 파일을 생성합니다.
- 프로그램 종료 시 JSON을 저장하므로 스크립트 실행 후 별도 서버가 필요 없습니다.
- 필요 시 서브커맨드를 추가해 팀원 할당, 일정 관리 등 기능을 확장할 수 있습니다.
