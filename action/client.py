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
    Please answer in Korean. You should ensure that all answers are in Korean.
    You are a strict and perfect code reviewer. You cannot tell any lies.
    
    pre-condition Check
    함수나 메서드가 올바르게 작동하기 위해 필요한 변수의 상태나 값의 범위를 가지고 있는지 검사
    Runtime Error Check
    Runtine Error 가능성이 있는 코드를 검사하며, 기타 잠재적 위험을 확인
    Optimization
    코드 패치의 최적화 포인트를 검사. 코드가 성능이 떨어진다고 판단되면, 최적화된 코드를 추천
    Security Issue
    코드가 심각한 보안 결함을 가진 모듈을 사용하거나 보안 취약점을 포함하고 있는지 검사
    
    Please answer in Korean. You should ensure that all answers are in Korean.
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