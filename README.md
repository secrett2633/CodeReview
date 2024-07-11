# 자동 코드 리뷰 도구

이 프로젝트는 GitHub Actions와 Claude API를 사용하여 자동으로 Pull Request의 코드를 리뷰하는 도구입니다.

## 기능

- Pull Request가 열릴 때 자동으로 코드 리뷰 실행
- Claude AI를 사용한 지능적인 코드 분석
- 다음 항목들을 중점적으로 검사:
  - Pre-condition 체크
  - Runtime 에러 가능성 검사
  - 코드 최적화 포인트 식별
  - 보안 이슈 점검

## 설치 방법

1. 이 리포지토리를 클론합니다.
2. `.github/workflows/code-review.yml` 파일을 당신의 리포지토리의 같은 위치에 복사합니다.
3. `action` 폴더 전체를 당신의 리포지토리의 루트 디렉토리에 복사합니다.

## 설정 방법

1. Claude API 키 설정:
   - GitHub 리포지토리의 Settings > Secrets and variables > Actions로 이동합니다.
   - 'New repository secret'을 클릭합니다.
   - 이름을 `CLAUDE_API_KEY`로 설정하고, 값에 실제 Claude API 키를 입력합니다.

2. GitHub Actions 권한 설정:
   - 리포지토리의 Settings > Actions > General로 이동합니다.
   - 'Workflow permissions'에서 'Read and write permissions'를 선택합니다.

## 사용 방법

설정이 완료되면, 리포지토리에 새로운 Pull Request가 생성될 때마다 자동으로 코드 리뷰가 실행됩니다. 
리뷰 결과는 Pull Request의 코멘트로 추가됩니다.

## 프로젝트 구조

~~~
your-repository/
├── .github/
│   └── workflows/
│       └── code-review.yml
├── action/
│   ├── client.py
│   ├── requirements.txt
│   └── action.yml
└── README.md
~~~

- `.github/workflows/code-review.yml`: GitHub Actions 워크플로우 정의
- `action/client.py`: Claude API 호출 및 GitHub PR 코멘트 로직
- `action/requirements.txt`: 필요한 Python 라이브러리 목록
- `action/Dockerfile`: 액션 실행을 위한 Docker 이미지 정의
- `action/action.yml`: GitHub Action 정의

## 주의사항

- 이 도구는 자동화된 코드 리뷰를 제공하지만, 인간의 코드 리뷰를 완전히 대체할 수 없습니다.
- Claude API의 사용량과 비용을 모니터링하세요.
- 코드 리뷰 결과를 항상 검토하고, 필요한 경우 수동으로 보완하세요.

## 기여 방법

프로젝트 개선을 위한 제안이나 버그 리포트는 언제나 환영합니다. Issues 섹션을 통해 의견을 제시해 주세요.
