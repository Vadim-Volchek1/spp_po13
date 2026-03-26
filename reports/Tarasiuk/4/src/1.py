import requests
from datetime import datetime, timedelta, timezone
from dateutil import parser
import matplotlib.pyplot as plt
import re

GITHUB_TOKEN = "API_KEY"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

BASE_URL = "https://api.github.com"


def get(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


# Фильтрация коммитов по дате
def filter_commits_by_time(commits, since_time):
    result = []
    for c in commits:
        try:
            date_str = c["commit"]["author"]["date"]
            if parser.parse(date_str) >= since_time:
                result.append(c)
        except KeyError:
            continue
    return result


def get_commits(owner, repo, since_time):
    url = f"{BASE_URL}/repos/{owner}/{repo}/commits"
    commits = get(url)
    return filter_commits_by_time(commits, since_time)


def filter_by_time(items, key, since_time):
    result = []
    for i in items:
        try:
            if parser.parse(i[key]) >= since_time:
                result.append(i)
        except (KeyError, TypeError):
            continue
    return result


def get_issues(owner, repo, since_time):
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues"
    issues = get(url, {"state": "all"})

    new_issues = filter_by_time(issues, "created_at", since_time)
    closed_issues = filter_by_time(
        [i for i in issues if i.get("closed_at")],
        "closed_at",
        since_time
    )
    return new_issues, closed_issues


def get_pulls(owner, repo, since_time):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    pulls = get(url, {"state": "all"})

    new_pulls = filter_by_time(pulls, "created_at", since_time)
    closed_pulls = filter_by_time(
        [p for p in pulls if p.get("closed_at")],
        "closed_at",
        since_time
    )
    return new_pulls, closed_pulls


def get_contributors(commits):
    authors = set()
    for c in commits:
        if c.get("author"):
            authors.add(c["author"]["login"])
    return authors


def get_mentions(owner, repo, since_time):
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues/comments"
    comments = get(url)
    comments = filter_by_time(comments, "created_at", since_time)

    mentions = set()
    for c in comments:
        body = c.get("body", "")
        found = re.findall(r'@\w+', body)
        mentions.update(found)
    return mentions


def get_repo_stats(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    repo_data = get(url)
    return repo_data.get("stargazers_count", 0), repo_data.get("forks_count", 0)


def visualize(data):
    labels = list(data.keys())
    values = list(data.values())

    plt.figure()
    plt.bar(labels, values)
    plt.title("GitHub Activity Overview")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def main():
    repo_input = input("Введите репозиторий (owner/repo): ").strip()
    if "/" not in repo_input:
        print("Ошибка: нужно вводить в формате owner/repo, например: django/django")
        return

    owner, repo = repo_input.split("/")
    hours = int(input("Введите временной диапазон (часы): "))
    since_time = datetime.now(timezone.utc) - timedelta(hours=hours)

    commits = get_commits(owner, repo, since_time)
    new_issues, closed_issues = get_issues(owner, repo, since_time)
    new_pulls, closed_pulls = get_pulls(owner, repo, since_time)
    mentions = get_mentions(owner, repo, since_time)
    stars, forks = get_repo_stats(owner, repo)
    contributors = get_contributors(commits)

    print(f"\nМониторинг активности в '{repo_input}' за последние {hours} часов:\n")
    print(f"{len(commits)} новых коммитов")
    print(f"{len(new_pulls)} новых PR ({len(closed_pulls)} закрыто)")
    print(f"{len(new_issues)} новых issues ({len(closed_issues)} закрыто)")
    print(f"{len(contributors)} новых контрибьюторов: {', '.join(contributors) if contributors else 'нет'}")
    print(f"{stars} звёзд, {forks} форков")
    print(f"{len(mentions)} упоминаний: {', '.join(mentions) if mentions else 'нет'}")

    # Визуализация
    visualize({
        "Commits": len(commits),
        "PR Opened": len(new_pulls),
        "PR Closed": len(closed_pulls),
        "Issues Opened": len(new_issues),
        "Issues Closed": len(closed_issues),
        "Mentions": len(mentions)
    })


if __name__ == "__main__":
    main()
