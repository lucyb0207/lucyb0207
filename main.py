import os
import requests
import re

USERNAME = "lucyb0207"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"
}

if __name__ == "__main__":

    # ----------------------------
    # GET REPOS
    # ----------------------------
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos = requests.get(repos_url, headers=HEADERS).json()

    total_merged_prs = 0
    pr_list = []

    emoji = ["🥳", "🎉", "🎊", "🥂", "🙌🏼"]
    count = 0

    # ----------------------------
    # LOOP REPOS + COUNT PRS
    # ----------------------------
    for repo in repos:

        repo_name = repo["full_name"]

        search_url = (
            f"https://api.github.com/search/issues"
            f"?q=repo:{repo_name}+type:pr+is:merged+author:{USERNAME}"
        )

        r = requests.get(search_url, headers=HEADERS)

        if r.status_code != 200:
            continue

        data = r.json()

        total_merged_prs += data.get("total_count", 0)

        for item in data.get("items", []):

            emoticon = emoji[count % len(emoji)]
            pull_request_url = item["html_url"]

            repo_url = pull_request_url.split("/pull/")[0]

            pr_list.append(
                f"{count + 1}. {emoticon} Merged PR "
                f"[#{item['number']}]({pull_request_url}) - "
                f"[{repo_name}]({repo_url})"
            )

            count += 1

            if count == 5:
                break

    # ----------------------------
    # BADGE
    # ----------------------------
    badge = (
        f'<span><img src="https://img.shields.io/badge/'
        f'Total_Merged_PRs-{total_merged_prs}-1877F2?style=for-the-badge"></span>'
    )

    pr_content = "\n".join(pr_list) if pr_list else "No merged PRs found yet."

    # ----------------------------
    # READ README
    # ----------------------------
    with open("README.md", "r") as f:
        readme = f.read()

    # ----------------------------
    # UPDATE COUNT
    # ----------------------------
    readme = re.sub(
        r"(<!--Start Count Merged PRs-->)(.*?)(<!--Finish Count Merged PRs-->)",
        f"\\1\n{badge}\n\\3",
        readme,
        flags=re.DOTALL
    )

    # ----------------------------
    # UPDATE PR LIST
    # ----------------------------
    readme = re.sub(
        r"(<!--Start Merged PRs-->)(.*?)(<!--Finish Merged PRs-->)",
        f"\\1\n{pr_content}\n\\3",
        readme,
        flags=re.DOTALL
    )

    # ----------------------------
    # WRITE BACK
    # ----------------------------
    with open("README.md", "w") as f:
        f.write(readme)

    print(f"Total merged PRs: {total_merged_prs}")