import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()


class GitHubAPIClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}'
        }

    def make_request(self, url, params=None):
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 403:
                if 'rate limit' in response.text.lower():
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(reset_time - time.time(), 0)
                    print(f"Превышен лимит запросов. Ожидание {wait_time:.0f} секунд...")
                    time.sleep(wait_time + 1)
                    return self.make_request(url, params)
                else:
                    print(f"Доступ запрещен (403)")
                    return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None

    def get_all_pages(self, url, params=None):
        results = []
        page = 1

        if params is None:
            params = {}

        while True:
            params['page'] = page
            params['per_page'] = 100
            data = self.make_request(url, params.copy())
            if data is None:
                break
            if isinstance(data, list):
                if len(data) == 0:
                    break
                results.extend(data)
                if len(data) < 100:
                    break
            else:
                break
            page += 1
        return results


class InteractionCollector:
    def __init__(self, username, api_client):
        self.username = username
        self.api = api_client
        self.commit_repos = set()
        self.pr_repos = set()
        self.issue_repos = set()
        self.starred_repos = set()

    def get_user_repos(self):
        print("\nПолучаем репозитории пользователя...")
        url = f"{self.api.base_url}/users/{self.username}/repos"
        repos = self.api.get_all_pages(url)
        print(f"Найдено {len(repos)} репозиториев")
        return repos

    def check_commits_in_repo(self, owner, repo):
        url = f"{self.api.base_url}/repos/{owner}/{repo}/commits"
        params = {'author': self.username, 'per_page': 1}
        commits = self.api.make_request(url, params)
        return bool(commits and len(commits) > 0)

    def check_prs_in_repo(self, owner, repo):
        url = f"{self.api.base_url}/repos/{owner}/{repo}/pulls"
        params = {'state': 'all', 'per_page': 100}
        pulls = self.api.get_all_pages(url, params)
        if pulls:
            for pr in pulls:
                if pr['user']['login'].lower() == self.username.lower():
                    return True
        return False

    def check_issues_in_repo(self, owner, repo):
        url = f"{self.api.base_url}/repos/{owner}/{repo}/issues"
        params = {'state': 'all', 'creator': self.username, 'per_page': 1}
        issues = self.api.make_request(url, params)
        return bool(issues and len(issues) > 0)

    def get_starred_repositories(self):
        print("\nПолучаем звезды...")
        url = f"{self.api.base_url}/users/{self.username}/starred"
        starred_data = self.api.get_all_pages(url)

        if starred_data:
            for repo in starred_data:
                self.starred_repos.add(repo['full_name'])

        print(f"Найдено {len(self.starred_repos)} репозиториев со звездами")
        return self.starred_repos

    def collect_interaction_repos(self):
        repos = self.get_user_repos()
        if not repos:
            print("Не удалось получить репозитории пользователя")
            return
        print(f"\nВсего репозиториев для анализа: {len(repos)}")

        for repo in repos:
            repo_name = repo['full_name']
            owner, repo = repo_name.split('/')
            print("---")
            print(repo)
            if self.check_commits_in_repo(owner, repo):
                self.commit_repos.add(repo_name)
                print(f" - Коммиты: {repo_name}")
            if self.check_prs_in_repo(owner, repo):
                self.pr_repos.add(repo_name)
                print(f" - PR: {repo_name}")
            if self.check_issues_in_repo(owner, repo):
                self.issue_repos.add(repo_name)
                print(f" - Issues: {repo_name}")

        self.get_starred_repositories()
        print("---")
        print("РЕЗУЛЬТАТЫ АНАЛИЗА:")
        print(f"Пользователь: {self.username}")
        print(f"Коммиты: {len(self.commit_repos)} репозиториев")
        print(f"Pull Requests: {len(self.pr_repos)} репозиториев")
        print(f"Issues: {len(self.issue_repos)} репозиториев")
        print(f"Звезды: {len(self.starred_repos)} репозиториев")


def main():
    username = input("Введите имя пользователя GitHub: ").strip()
    if not username:
        print("Имя пользователя не может быть пустым!")
        return

    api_client = GitHubAPIClient()
    collector = InteractionCollector(username, api_client)
    collector.collect_interaction_repos()


if __name__ == "__main__":
    main()
