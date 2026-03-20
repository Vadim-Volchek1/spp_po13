import requests
import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

TOKEN = ""

HEADERS = {}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"


def get_github_data(username):
    repos_url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(repos_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка соединения или доступа: {e}")
        return None

    repos = response.json()
    all_commits_info = []
    monthly_activity = []
    repo_commit_counts = {}

    print(f"Начинаю сбор данных для пользователя: {username}...")

    for repo in repos:
        repo_name = repo['name']
        # Ограничиваем количество, чтобы не упереться в лимиты API
        commits_url = (
            f"https://api.github.com/repos/{username}/{repo_name}/"
            "commits?per_page=10"
        )
        try:
            c_response = requests.get(commits_url, headers=HEADERS, timeout=10)
            if c_response.status_code == 200:
                commits = c_response.json()
                repo_commit_counts[repo_name] = len(commits)

                for c in commits:
                    if not c.get('commit'):
                        continue

                    date_str = c['commit']['author']['date']
                    msg = c['commit']['message']
                    author = c['commit']['author']['name']

                    # ISO формат: 2023-10-27T12:00:00Z
                    dt_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

                    all_commits_info.append({
                        "repository": repo_name,
                        "date": date_str,
                        "message": msg,
                        "author": author
                    })
                    monthly_activity.append(dt_obj.strftime("%Y-%m"))
        except Exception:
            print(f"Не удалось получить коммиты для {repo_name}")

    return all_commits_info, monthly_activity, repo_commit_counts


def main():
    user_input = input("Введите имя GitHub (например, octocat): ").strip()
    if not user_input:
        print("Имя пользователя не может быть пустым.")
        return

    result = get_github_data(user_input)
    if not result:
        return

    commits_list, months, repo_counts = result
    total_commits = len(commits_list)
    month_stats = Counter(months)

    top_repos = sorted(
        repo_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    print("-" * 30)
    print(f"Общее количество найденных коммитов: {total_commits}")

    if month_stats:
        active_month, count = month_stats.most_common(1)[0]
        print(f"Самый активный месяц: {active_month} ({count} коммитов)")

    print("ТОП-3 репозитория по количеству коммитов:")
    for i, (name, count) in enumerate(top_repos, 1):
        print(f"{i}. {name} ({count} коммитов)")

    if months:
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
        # plt.show() лучше закомментировать для CI, чтобы не блокировать поток
    else:
        print("\nДанные для графика отсутствуют.")

    final_json = {
        "target_user": user_input,
        "total_commits": total_commits,
        "top_repositories": top_repos,
        "detailed_commits": commits_list
    }

    try:
        with open("github_activity.json", "w", encoding="utf-8") as f:
            json.dump(final_json, f, indent=4, ensure_ascii=False)
        print("Данные успешно сохранены в: github_activity.json")
    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    main()
