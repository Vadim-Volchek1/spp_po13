"""
Анализ активности разработчиков GitHub-репозитория.
Получение статистики по коммитам, PR и issues.
"""

import requests
import matplotlib.pyplot as plt

BASE_URL = "https://api.github.com"
TIMEOUT = 10


def get_json(url):
    """Отправляет GET-запрос и возвращает JSON."""
    return requests.get(url, timeout=TIMEOUT).json()


# pylint: disable=too-many-locals
def main():
    """Основная функция программы."""
    while True:
        repo = input("Введите репозиторий (owner/repo): ")
        if "/" in repo:
            owner, repo_name = repo.split("/")
            break
        print("❌ Неверный формат. Пример: fastapi/fastapi")

    contributors_url = f"{BASE_URL}/repos/{owner}/{repo_name}/contributors"
    contributors = get_json(contributors_url)

    results = []

    print(f'Анализируем вклад контрибьюторов в "{repo}"...\n')

    for contributor in contributors[:10]:
        username = contributor["login"]
        commits = contributor.get("contributions", 0)

        pr_url = f"{BASE_URL}/search/issues?q=repo:{owner}/{repo_name}+author:{username}+type:pr"
        pr_data = get_json(pr_url)
        total_pr = pr_data.get("total_count", 0)

        issues_url = f"{BASE_URL}/search/issues?q=repo:{owner}/{repo_name}+author:{username}+type:issue"
        issues_data = get_json(issues_url)
        total_issues = issues_data.get("total_count", 0)

        events_url = f"{BASE_URL}/users/{username}/events/public"
        events = get_json(events_url)

        last_activity = "N/A"
        if events:
            last_activity = events[0].get("created_at", "N/A")

        total_score = commits + total_pr + total_issues

        results.append(
            {
                "user": username,
                "commits": commits,
                "pr": total_pr,
                "issues": total_issues,
                "score": total_score,
                "last_activity": last_activity,
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)

print("ТОП-5 самых активных разработчиков:\n")
for i, user in enumerate(results[:5], start=1):
    print(f"{i}. {user['user']} - {user['commits']} коммитов, {user['pr']} PR, {user['issues']} issues")

names = [u["user"] for u in results[:5]]
scores = [u["score"] for u in results[:5]]

plt.figure()
plt.bar(names, scores)
plt.xlabel("Разработчики")
plt.ylabel("Суммарный вклад")
plt.title(f"Активность разработчиков ({repo})")

file_name = f"{repo_name}_contributors.png"
plt.savefig(file_name)

print(f'\nГрафик сохранен в "{file_name}"')



if __name__ == "__main__":
    main()
