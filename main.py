import requests
import re

USERNAME = "lucyb0207"

if __name__ == "__main__":

    # Get all repos for user
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos = requests.get(repos_url).json()

    total_merged_prs = 0
    pr_list = []
    emoji = ["🥳", "🎉", "🎊", "🥂", "🙌🏼"]
    count = 0

    headers = {
        "Accept": "application/vnd.github+json"
    }

    # Loop through repos and count merged PRs per repo
    for repo in repos:
        repo_name = repo["full_name"]

        search_url = f"https://api.github.com/search/issues?q=repo:{repo_name}+type:pr+is:merged+author:{USERNAME}"
        r = requests.get(search_url, headers=headers)

        if r.status_code != 200:
            continue

        data = r.json()
        total_merged_prs += data.get("total_count", 0)

        # show latest PRs (from search results)
        for item in data.get("items", []):
            emoticon = emoji[count % len(emoji)]
            pull_request_url = item["html_url"]

            new_repo_url = re.sub(r"/pull/\d+", "", pull_request_url)

            pr_list.append(
                f"{count + 1}. {emoticon} Merged PR [{item['number']}]({pull_request_url}) - "
                f"[{repo_name}]({new_repo_url})"
            )

            count += 1
            if count == 5:
                break

    # Badge
    total_merged_prs_content = (
        f'<span><img src="https://img.shields.io/badge/Total_Merged_PRs-'
        f'{total_merged_prs}-1877F2?style=for-the-badge"></span>'
    )

    pr_content = "\n".join(pr_list)

    # Read README
    with open("README.md", "r") as f:
        readme_content = f.read()

    # Replace ONLY count section
    new_readme_content = re.sub(
        r'(<!--Start Count Merged PRs-->\n)(.*?)(<!--Finish Count Merged PRs-->)',
        f'\\1{total_merged_prs_content}\n\\3',
        readme_content,
        flags=re.DOTALL
    )

    # Replace PR list section
    new_readme_content = re.sub(
        r'(<!--Start Merged PRs-->\n)(.*?)(<!--Finish Merged PRs-->)',
        f'\\1{pr_content}\n\\3',
        new_readme_content,
        flags=re.DOTALL
    )

    # Write back
    with open("README.md", "w") as f:
        f.write(new_readme_content)