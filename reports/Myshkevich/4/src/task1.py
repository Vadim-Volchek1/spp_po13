"""GitHub пользователя."""

import os
import sys
from datetime import datetime
import json
import pandas as pd
from github import Github, GithubException
from dotenv import load_dotenv


def check_token():
    """Проверка наличия токена."""
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Ошибка: Не найден GITHUB_TOKEN в файле .env")
        print("Создайте файл .env с содержимым: GITHUB_TOKEN=ваш_токен")
        sys.exit(1)
    return token


def get_user_repositories(user, github_client):
    """Получение уникальных репозиториев пользователя."""
    repos_dict = {}

    # 1. Получаем репозитории, созданные пользователем
    print("Получаем репозитории пользователя...")
    for repo in user.get_repos():
        repos_dict[repo.full_name] = {
            "full_name": repo.full_name,
            "owner": repo.owner.login,
            "name": repo.name
        }

    # 2. Получаем репозитории, которые пользователь форкнул
    print("Получаем форкнутые репозитории...")
    for repo in user.get_repos():
        if repo.fork:
            repos_dict[repo.full_name] = {
                "full_name": repo.full_name,
                "owner": repo.owner.login,
                "name": repo.name
            }

    # 3. Получаем репозитории через pull requests
    print("Получаем pull requests пользователя...")
    query = f"is:pr author:{user.login} is:merged"
    for pr in github_client.search_issues(query):
        repo_name = pr.repository.full_name
        if repo_name not in repos_dict:
            repos_dict[repo_name] = {
                "full_name": repo_name,
                "owner": pr.repository.owner.login,
                "name": pr.repository.name,
            }

    # 4. Получаем репозитории через issues
    print("Получаем issues пользователя...")
    query = f"is:issue author:{user.login}"
    for issue in github_client.search_issues(query):
        repo_name = issue.repository.full_name
        if repo_name not in repos_dict:
            repos_dict[repo_name] = {
                "full_name": repo_name,
                "owner": issue.repository.owner.login,
                "name": issue.repository.name,
            }

    return repos_dict


def count_commits(repo, user):
    """Подсчет коммитов пользователя в репозитории."""
    try:
        commits = repo.get_commits(author=user)
        return sum(1 for _ in commits)
    except GithubException as e:
        print(f"  Не удалось получить коммиты: {e}")
        return 0


def count_pull_requests(repo, username):
    """Подсчет PR пользователя."""
    open_prs_count = 0
    closed_prs_count = 0

    # Открытые PR
    try:
        open_prs = repo.get_pulls(state="open", sort="created")
        for pr in open_prs:
            if pr.user.login == username:
                open_prs_count += 1
    except GithubException as e:
        print(f"  Не удалось получить открытые PR: {e}")

    # Закрытые PR
    try:
        closed_prs = repo.get_pulls(state="closed", sort="created")
        for pr in closed_prs:
            if pr.user.login == username:
                closed_prs_count += 1
    except GithubException as e:
        print(f"  Не удалось получить закрытые PR: {e}")

    return open_prs_count, closed_prs_count


def count_issues(repo, user):
    """Подсчет issues пользователя."""
    try:
        issues = repo.get_issues(state="all", creator=user)
        return sum(1 for _ in issues)
    except GithubException as e:
        print(f"  Не удалось получить issues: {e}")
        return 0


def analyze_repository(repo_name, user, username, github_client):
    """Анализ одного репозитория."""
    try:
        repo = github_client.get_repo(repo_name)

        commits_count = count_commits(repo, user)
        open_prs_count, closed_prs_count = count_pull_requests(repo, username)
        issues_count = count_issues(repo, user)

        # Вычисляем активность по формуле
        activity_score = (
            commits_count * 1 +
            open_prs_count * 2 +
            closed_prs_count * 3 +
            issues_count * 1.5
        )

        has_activity = (
            commits_count > 0 or
            open_prs_count > 0 or
            closed_prs_count > 0 or
            issues_count > 0
        )

        if has_activity:
            return {
                "repository": repo_name,
                "commits": commits_count,
                "open_pull_requests": open_prs_count,
                "closed_pull_requests": closed_prs_count,
                "created_issues": issues_count,
                "activity_score": activity_score,
            }
    except GithubException as e:
        print(f"  Ошибка при анализе {repo_name}: {e}")

    return None


def print_statistics(df, username):
    """Вывод статистики в консоль."""
    total_commits = df["commits"].sum()
    total_open_prs = df["open_pull_requests"].sum()
    total_closed_prs = df["closed_pull_requests"].sum()
    total_issues = df["created_issues"].sum()
    total_activity = df["activity_score"].sum()

    most_active = df.loc[df["activity_score"].idxmax()]

    print("\n" + "=" * 50)
    print("Результаты анализа пользователя: " + username)
    print("=" * 50)
    print(f"Всего репозиториев с активностью: {len(df)}")
    print("\nОбщая статистика:")
    print(f"  - Общее количество коммитов: {total_commits}")
    print(f"  - Открытых pull requests: {total_open_prs}")
    print(f"  - Закрытых pull requests: {total_closed_prs}")
    print(f"  - Созданных issues: {total_issues}")
    print(f"  - Общая активность: {total_activity:.1f} баллов")

    print("\nСамый активный проект:")
    print(f"  - {most_active['repository']}")
    print(f"  - Коммитов: {most_active['commits']}")
    print(f"  - Открытых PR: {most_active['open_pull_requests']}")
    print(f"  - Закрытых PR: {most_active['closed_pull_requests']}")
    print(f"  - Issues: {most_active['created_issues']}")
    print(f"  - Активность: {most_active['activity_score']:.1f} баллов")

    # Топ-5 проектов по активности
    print("\nТоп-5 проектов по активности:")
    top5 = df.nlargest(5, "activity_score")[
        ["repository", "commits", "activity_score"]
    ]
    for _, row in top5.iterrows():
        print(
            f"  - {row['repository']}: {row['activity_score']:.1f} баллов "
            f"({row['commits']} коммитов)"
        )


def save_to_json(contributions, df, username):
    """Сохранение результатов в JSON файл."""
    if df.empty:
        return

    total_commits = df["commits"].sum()
    total_open_prs = df["open_pull_requests"].sum()
    total_closed_prs = df["closed_pull_requests"].sum()
    total_issues = df["created_issues"].sum()
    total_activity = df["activity_score"].sum()
    most_active = df.loc[df["activity_score"].idxmax()]

    output_data = {
        "username": username,
        "analysis_date": datetime.now().isoformat(),
        "total_repositories": len(df),
        "total_commits": int(total_commits),
        "total_open_pull_requests": int(total_open_prs),
        "total_closed_pull_requests": int(total_closed_prs),
        "total_created_issues": int(total_issues),
        "total_activity_score": float(total_activity),
        "most_active_project": {
            "repository": most_active["repository"],
            "commits": int(most_active["commits"]),
            "open_pull_requests": int(most_active["open_pull_requests"]),
            "closed_pull_requests": int(most_active["closed_pull_requests"]),
            "created_issues": int(most_active["created_issues"]),
            "activity_score": float(most_active["activity_score"]),
        },
        "all_contributions": contributions,
    }

    with open("github_contribution.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("\nРезультаты сохранены в 'github_contribution.json'")


def main():
    """Главная функция."""
    token = check_token()
    github_client = Github(token)

    username = input("Введите имя пользователя GitHub: ")
    print(f"\nАнализируем вклад пользователя '{username}'...")

    try:
        user = github_client.get_user(username)
        repos_dict = get_user_repositories(user, github_client)

        print(f"\nНайдено репозиториев: {len(repos_dict)}")

        # Собираем данные по каждому репозиторию
        contributions = []

        for repo_name in repos_dict:
            print(f"Анализируем: {repo_name}")
            result = analyze_repository(repo_name, user, username, github_client)
            if result:
                contributions.append(result)

        # Создаем DataFrame для удобного анализа
        df = pd.DataFrame(contributions)

        if df.empty:
            print(
                f"\nПользователь {username} не имеет видимой активности "
                "в публичных репозиториях."
            )
        else:
            print_statistics(df, username)
            save_to_json(contributions, df, username)

    except GithubException as e:
        print(f"Произошла ошибка: {e}")
        print(
            "Проверьте имя пользователя и наличие доступа к API GitHub"
        )


if __name__ == "__main__":
    main()
