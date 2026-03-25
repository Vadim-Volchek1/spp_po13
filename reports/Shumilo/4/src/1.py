import json
import os
from datetime import datetime

import requests
import matplotlib.pyplot as plt
from requests.exceptions import RequestException


STATE_FILE = "repo_state.json"
GITHUB_API = "https://api.github.com/repos/{repo}/releases/latest"


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)


def get_latest_release(repo):
    url = GITHUB_API.format(repo=repo)
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "GitHub-Release-Monitor"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except RequestException as e:
        print(f"⚠ Ошибка сети при запросе {repo}: {e}")
        return None
    if response.status_code == 404:
        print(f"⚠ У репозитория {repo} нет релизов (404).")
        return None
    if response.status_code == 403:
        print(f"⚠ Доступ запрещён или превышен лимит запросов для {repo}.")
        print("Ответ GitHub:", response.text[:200], "...")
        return None
    if response.status_code != 200:
        print(f"⚠ Ошибка {response.status_code} при запросе {repo}")
        print("Ответ:", response.text[:200], "...")
        return None
    data = response.json()
    if not data.get("tag_name"):
        print(f"⚠ У {repo} нет корректных данных о релизе.")
        return None
    return {
        "tag": data.get("tag_name"),
        "date": data.get("published_at"),
        "url": data.get("html_url"),
        "body": data.get("body", "Нет описания изменений"),
    }


def visualize_release_dates(state):
    repos = []
    dates = []
    for repo, releases in state.items():
        for rel in releases:
            if rel.get("date"):
                repos.append(f"{repo} ({rel['tag']})")
                dates.append(datetime.fromisoformat(rel["date"].replace("Z", "")))
    if not dates:
        print("Нет данных для визуализации")
        return
    plt.figure(figsize=(14, 6))
    plt.bar(repos, dates)
    plt.ylabel("Дата релиза")
    plt.title("История релизов отслеживаемых репозиториев")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def main():
    user_input = input("Введите репозитории для отслеживания (через запятую): ")
    repos = [r.strip() for r in user_input.split(",")]
    previous_state = load_state()
    new_state = previous_state.copy()
    for repo in repos:
        print(f"\nПроверяем обновления для {repo}...")
        latest = get_latest_release(repo)
        if not latest:
            continue
        if repo not in new_state:
            new_state[repo] = []
        existing_tags = [r["tag"] for r in new_state[repo]]
        if latest["tag"] not in existing_tags:
            print(f"Найден новый релиз: {latest['tag']} ({latest['date']})")
            print(latest["url"])
            print("Основные изменения:")
            print(latest["body"][:300], "...\n")
            new_state[repo].append(latest)
        else:
            print("Обновлений нет.")
    save_state(new_state)
    visualize_release_dates(new_state)
    print("\nГотово!")


if __name__ == "__main__":
    main()
