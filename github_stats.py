from datetime import date, datetime

from github import Github
from github.GithubException import GithubException
from tqdm import tqdm

api = Github("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")

# Get organization repos count
org = api.get_organization("CardoAI")
print("Total GitHub repositories:", org.get_repos().totalCount)

# Get number of repositories created this year
repos = org.get_repos()
current_year = date.today().year
beginning_of_year = datetime(current_year, 1, 1, 0, 0, 0)

repos_created_this_year = 0
total_commits_this_year = 0
contributors = set()
coding_languages = set()

pbar = tqdm(repos)
for repo in pbar:
    pbar.set_description(f"Processing {repo.name}")
    if repo.created_at.year == current_year:
        repos_created_this_year += 1

    try:
        commits_this_year = repo.get_commits(since=beginning_of_year)
        total_commits_this_year += commits_this_year.totalCount

        # Get contributors from commits
        for commit in commits_this_year:
            if commit.author:
                contributors.add(commit.author.login)
    except GithubException as e:
        if "Git Repository is empty" in str(e):
            continue

    # Get languages used in repo
    repo_languages = repo.get_languages()
    coding_languages.update(repo_languages.keys())


print("Repositories created this year:", repos_created_this_year)
print("Total Number of Commits in our repositories this year (until today):", total_commits_this_year)
print("Total Number of Contributors in our repositories this year:", len(contributors))
print("Coding Languages used in our repositories:", len(coding_languages))
print("Full list:", ", ".join(coding_languages))
