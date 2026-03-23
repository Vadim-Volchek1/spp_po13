"""Анализ активности контрибьюторов GitHub."""

import os
import requests
import matplotlib.pyplot as plt


def github_get(url, params=None):
    """Выполняет GET-запрос к GitHub API с поддержкой токена."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_contributors(owner, repo_name):
    """Возвращает список контрибьюторов репозитория."""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contributors"
    return github_get(url)


def get_pull_requests(owner, repo_name, state):
    """Возвращает список PR в указанном состоянии."""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    return github_get(url, params={"state": state, "per_page": 100})


def get_issues(owner, repo_name, state):
    """Возвращает список issues в указанном состоянии."""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/issues"
    return github_get(url, params={"state": state, "per_page": 100})


def get_user_last_activity(username):
    """Возвращает дату последней активности пользователя."""
    url = f"https://api.github.com/users/{username}/events/public"
    events = github_get(url)
    if not events:
        return None
    return events[0]["created_at"]


def calculate_user_stats(username, context):
    """Вычисляет статистику активности одного пользователя."""
    commits = context["commits"]
    open_prs = context["open_prs"]
    closed_prs = context["closed_prs"]
    open_issues = context["open_issues"]
    closed_issues = context["closed_issues"]

    prs_open = len([p for p in open_prs if p["user"]["login"] == username])
    prs_closed = len([p for p in closed_prs if p["user"]["login"] == username])

    issues_open = len([i for i in open_issues if i["user"]["login"] == username])
    issues_closed = len([i for i in closed_issues if i["user"]["login"] == username])

    last_activity = get_user_last_activity(username)

    total_score = commits + prs_open + prs_closed + issues_open + issues_closed

    return {
        "user": username,
        "commits": commits,
        "prs": prs_open + prs_closed,
        "issues": issues_open + issues_closed,
        "last_activity": last_activity,
        "score": total_score,
    }



def analyze_repo(full_name):
    """Анализирует активность контрибьюторов репозитория."""
    owner, repo_name = full_name.split("/")
    print(f'Анализируем вклад контрибьюторов в "{full_name}"...')

    contributors = get_contributors(owner, repo_name)
    open_prs = get_pull_requests(owner, repo_name, "open")
    closed_prs = get_pull_requests(owner, repo_name, "closed")
    open_issues = get_issues(owner, repo_name, "open")
    closed_issues = get_issues(owner, repo_name, "closed")

    stats_list = []

    for contributor in contributors:
        username = contributor["login"]
        commits = contributor.get("contributions", 0)

        context = {
            "commits": commits,
            "open_prs": open_prs,
            "closed_prs": closed_prs,
            "open_issues": open_issues,
            "closed_issues": closed_issues,
        }

        user_stats = calculate_user_stats(username, context)
        stats_list.append(user_stats)

    return sorted(stats_list, key=lambda x: x["score"], reverse=True)


def plot_stats(stats, repo_name):
    """Строит график активности контрибьюторов."""
    top = stats[:10]

    users = [s["user"] for s in top]
    scores = [s["score"] for s in top]

    plt.figure(figsize=(12, 6))
    plt.bar(users, scores, color="skyblue")
    plt.title(f"Активность контрибьюторов в {repo_name}")
    plt.ylabel("Суммарный вклад")
    plt.xticks(rotation=45, ha="right")

    filename = repo_name.replace("/", "_") + "_contributors.png"
    plt.tight_layout()
    plt.savefig(filename)
    print(f'График сохранён в "{filename}"')


if __name__ == "__main__":
    repo_input = input("Введите репозиторий (owner/repo): ").strip()
    stats_result = analyze_repo(repo_input)

    print("\nТОП-5 самых активных разработчиков:")
    for i, s in enumerate(stats_result[:5], start=1):
        print(
            f"{i}. {s['user']} — {s['commits']} коммитов, {s['prs']} PR, {s['issues']} issues"
        )

    plot_stats(stats_result, repo_input)
