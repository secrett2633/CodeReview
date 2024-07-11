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