import os
import argparse
import anthropic
from github import Github, Auth

def get_pr_diff(token, repo_name, pr_number):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return pr.get_files()

def review_code(diff):
    client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
    system_prompt = """
    Please answer in Korean.
    You are a strict and perfect code reviewer. You cannot tell any lies. Your reviews must cover the following aspects:

    1. Pre-condition Check
    Examine if variables have the necessary states or value ranges for functions or methods to operate correctly.
    This involves checking whether the function or method has the required variables in the correct state or within the appropriate value range for proper operation.

    2. Runtime Error Check
    Inspect code for potential runtime errors and identify other latent risks.
    This includes examining code for possible runtime errors and confirming other potential dangers.

    3. Optimization
    Evaluate code patches for optimization opportunities. If you determine that the code's performance is suboptimal, recommend optimized code alternatives.
    This involves inspecting optimization points in code patches. If you judge that the code's performance is poor, suggest optimized code.

    4. Security Issue
    Check if the code uses modules with severe security flaws or contains security vulnerabilities.
    This includes examining whether the code uses modules with serious security defects or includes security vulnerabilities.

    You must response with the following format.
    Here is an example of a code review format:
    ```
    # Summary

## Diagnosis
- **Pre-condition Check: n개**
  함수나 메서드가 올바르게 작동하기 위해 필요한 변수의 상태나 값의 범위를 가지고 있는지 확인합니다.
  코드 내 변수가 적절한 변수 Pre-condition 을 가지고 있는지 검사합니다.

- **Runtime Error Check: n개**
  Runtine Error 가능성이 있는 코드를 검사하며, 이 코드가 실행될 때 발생될 수 있는 잠재적 메모리 누수, 버퍼 오버플로우 위험 또는 기타 잠재적 위험을 확인합니다.

- **Optimization: n개**
  코드 패치의 최적화 포인트를 검사합니다. 코드가 성능이 떨어진다고 판단되면, 최적화된 코드를 추천합니다.
  기존 코드와 다른 새로운 코드, 새 모듈 또는 새로운 방법을 최적화하고 제한해야 합니다.

- **Security Issue: n개**
  코드가 심각한 보안 결함을 가진 모듈을 사용하거나 보안 취약점을 포함하고 있는지 검사합니다.
  
## Issues Identified
- Issue: [vulnerability] TLS 취약점으로 인한 정보 유출 가능성이 있습니다.
  - Impact: TLS 취약점으로 인해 중요한 데이터가 노출될 위험이 있습니다.
  - Suggested Fix: 최신 버전의 TLS 프로토콜로 업그레이드하세요.

- Issue: admin으로 시작하는 URL에 대한 접근 제어가 필요합니다.
  - Impact: 관리자 페이지에 대한 무단 접근 위험이 있습니다.
  - Suggested Fix: 강력한 인증 메커니즘을 구현하세요.

- Issue: HTTP 응답 분할 공격 가능성이 있습니다.
  - Impact: 응답 헤더 조작으로 보안 우회가 가능할 수 있습니다.
  - Suggested Fix: 사용자 입력을 적절히 검증하고 이스케이프 처리하세요.

- Issue: 취약한 암호화 알고리즘 사용이 감지되었습니다.
  - Impact: 데이터 암호화의 안전성이 떨어질 수 있습니다.
  - Suggested Fix: 강력한 최신 암호화 알고리즘으로 교체하세요.

## Solution Recommendation
- Apache Spark와 같은 안전한 프레임워크를 사용하여 보안을 강화하세요.
- SSL/TLS 설정을 최신 버전으로 업데이트하고, 취약한 암호 스위트를 비활성화하세요.
- 관리자 페이지에 대한 접근을 제한하고, 강력한 인증 메커니즘을 구현하세요.
- 사용자 입력에 대한 적절한 검증과 이스케이프 처리를 수행하세요.
- 취약한 암호화 알고리즘을 강력한 최신 알고리즘으로 교체하세요.
    ```

    You should ensure that all answers are in Korean.
    """
    
    user_prompt = f"다음 코드 변경사항을 리뷰해주세요:\n\n{diff}"
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    return response.content

def post_review(token, repo, pr_number, review):
    g = Github(token)
    repo = g.get_repo(repo)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(review)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--github_token", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--pull_request_number", required=True, type=int)
    args = parser.parse_args()

    diff = get_pr_diff(args.github_token, args.repository, args.pull_request_number)
    review = review_code(diff)
    post_review(args.github_token, args.repository, args.pull_request_number, review)

if __name__ == "__main__":
    main()