import json
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt
import requests

TOKEN = ""

HEADERS = {}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"


def get_github_data(username):
    """Получает данные о репозиториях и коммитах пользователя."""
    repos_url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(repos_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к GitHub API: {e}")
        return None

    repos = response.json()
    all_commits_info = []
    monthly_activity = []
    repo_commit_counts = {}

    print(f"Начинаю сбор данных для пользователя: {username}...")

    for repo in repos:
        repo_name = repo['name']
        commits_url = (
            f"https://api.github.com/repos/{username}/{repo_name}/"
            "commits?per_page=10"
        )
        try:
            c_res = requests.get(commits_url, headers=HEADERS, timeout=10)
            if c_res.status_code == 200:
                commits = c_res.json()
                repo_commit_counts[repo_name] = len(commits)
                process_commits(commits, repo_name, all_commits_info,
                                monthly_activity)
        except requests.exceptions.RequestException:
            print(f"Не удалось получить коммиты для {repo_name}")

    return all_commits_info, monthly_activity, repo_commit_counts


def process_commits(commits, repo_name, all_commits, monthly_act):
    """Парсит данные отдельных коммитов."""
    for commit_data in commits:
        if not commit_data.get('commit'):
            continue
        date_str = commit_data['commit']['author']['date']
        msg = commit_data['commit']['message']
        author = commit_data['commit']['author']['name']

        dt_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        all_commits.append({
            "repository": repo_name,
            "date": date_str,
            "message": msg,
            "author": author
        })
        monthly_act.append(dt_obj.strftime("%Y-%m"))


def save_visuals(user_input, month_stats):
    """Создает и сохраняет график активности."""
    sorted_months = sorted(month_stats.items())
    x_labels, y_values = zip(*sorted_months)

    plt.figure(figsize=(10, 6))
    plt.bar(x_labels, y_values, color='teal')
    plt.title(f"Активность пользователя {user_input} по месяцам")
    plt.xlabel("Месяц (Год-Месяц)")
    plt.ylabel("Количество коммитов")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig("activity_chart.png")
    print("\nГрафик сохранен в файл: activity_chart.png")


def main():
    """Основная логика скрипта."""
    user_input = input("Введите имя пользователя GitHub: ").strip()
    if not user_input:
        return

    data = get_github_data(user_input)
    if not data:
        return

    commits_list, months, repo_counts = data
    month_stats = Counter(months)
    top_repos = sorted(repo_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    print("-" * 30)
    print(f"Общее количество найденных коммитов: {len(commits_list)}")

    if month_stats:
        active_month, count = month_stats.most_common(1)[0]
        print(f"Самый активный месяц: {active_month} ({count} коммитов)")
        save_visuals(user_input, month_stats)

    print("ТОП-3 репозитория по количеству коммитов:")
    for i, (name, count) in enumerate(top_repos, 1):
        print(f"{i}. {name} ({count} коммитов)")

    final_json = {
        "target_user": user_input,
        "total_commits": len(commits_list),
        "top_repositories": top_repos,
        "detailed_commits": commits_list
    }

    with open("github_activity.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
    print("Данные успешно сохранены в: github_activity.json")


if __name__ == "__main__":
    main()
