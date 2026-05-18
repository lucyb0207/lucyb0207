import os
import requests
import re

USERNAME = "lucyb0207"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"
}

if __name__ == "__main__":

    # -----------------------------
    # GET TOTAL MERGED PR COUNT
    # -----------------------------
    url = f"https://api.github.com/search/issues?q=type:pr+is:merged+author:{USERNAME}"

    r = requests.get(url, headers=HEADERS)
    data = r.json()

    total_merged_prs = data.get("total_count", 0)

    # -----------------------------
    # BUILD BADGE
    # -----------------------------
    badge = (
        f'<span><img src="https://img.shields.io/badge/'
        f'Total_Merged_PRs-{total_merged_prs}-1877F2?style=for-the-badge"></span>'
    )

    # -----------------------------
    # READ README
    # -----------------------------
    with open("README.md", "r") as f:
        readme = f.read()

    # -----------------------------
    # REPLACE COUNT ONLY
    # -----------------------------
    new_readme = re.sub(
        r"(<!--Start Count Merged PRs-->)(.*?)(<!--Finish Count Merged PRs-->)",
        f"\\1\n{badge}\n\\3",
        readme,
        flags=re.DOTALL
    )

    # -----------------------------
    # WRITE BACK
    # -----------------------------
    with open("README.md", "w") as f:
        f.write(new_readme)

    print(f"Total merged PRs: {total_merged_prs}")