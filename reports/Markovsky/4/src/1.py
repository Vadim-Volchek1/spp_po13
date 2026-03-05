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


class CollaborationCollector:
    INTERACTION_TYPES = {
        'commit_authors': 'Авторы коммитов',
        'pr_reviewers': 'Ревьюеры PR',
        'pr_authors': 'Авторы PR (в чужих репозиториях)',
        'issue_authors': 'Авторы issues',
        'issue_commenters': 'Комментаторы issues',
        'starred_owners': 'Владельцы репозиториев со звездами'
    }

    def __init__(self, username):
        self.username = username.lower()
        self.collaborators = {
            'commit_authors': set(),
            'pr_reviewers': set(),
            'pr_authors': set(),
            'issue_authors': set(),
            'issue_commenters': set(),
            'starred_owners': set()
        }

    def _add_collaborator(self, collaborator_type, username):
        if username and username.lower() != self.username:
            self.collaborators[collaborator_type].add(username.lower())

    def add_pr_author(self, author):
        self._add_collaborator('pr_authors', author)

    def add_issue_author(self, author):
        self._add_collaborator('issue_authors', author)

    def add_starred_owner(self, owner):
        self._add_collaborator('starred_owners', owner)

    def add_multiple_collaborators(self, collaborator_type, usernames):
        for username in usernames:
            self._add_collaborator(collaborator_type, username)

    def get_all_collaborators(self):
        all_collaborators = set()
        for collab_set in self.collaborators.values():
            all_collaborators.update(collab_set)
        return all_collaborators

    def print_summary(self):
        print("ВЗАИМОДЕЙСТВИЯ С ДРУГИМИ РАЗРАБОТЧИКАМИ:")
        has_any_interactions = False
        for collab_type, collab_set in self.collaborators.items():
            if collab_set:
                has_any_interactions = True
                display_name = self.INTERACTION_TYPES.get(collab_type, collab_type.replace('_', ' ').title())
                print(f"\n{display_name}: {len(collab_set)}")
                for collab in sorted(collab_set)[:10]:
                    print(f"  - {collab}")
                if len(collab_set) > 10:
                    print(f"... и еще {len(collab_set) - 10}")
        if not has_any_interactions:
            print("\nНе найдено взаимодействий с другими разработчиками")

        all_collabs = self.get_all_collaborators()
        print(f"\nВСЕГО УНИКАЛЬНЫХ РАЗРАБОТЧИКОВ: {len(all_collabs)}")
        if all_collabs:
            print("Полный список (первые 20):")
            for i, collab in enumerate(sorted(all_collabs)[:20], 1):
                print(f"{i}. {collab}")
            if len(all_collabs) > 20:
                print(f"... и еще {len(all_collabs) - 20}")


class InteractionCollector:
    def __init__(self, username, api_client, collaboration_collector):
        self.username = username
        self.api = api_client
        self.collaboration = collaboration_collector
        self.commit_repos = set()
        self.pr_repos = set()
        self.issue_repos = set()
        self.starred_repos = set()

    @staticmethod
    def _extract_usernames_from_items(items, key='user'):
        usernames = set()
        for item in items:
            if key in item and item[key] and 'login' in item[key]:
                usernames.add(item[key]['login'])
        return usernames

    def get_user_repos(self):
        print("\nПолучаем репозитории пользователя...")
        url = f"{self.api.base_url}/users/{self.username}/repos"
        repos = self.api.get_all_pages(url)
        print(f"Найдено {len(repos)} репозиториев")
        return repos

    def check_commits_in_repo(self, owner, repo):
        url = f"{self.api.base_url}/repos/{owner}/{repo}/commits"

        params = {'author': self.username, 'per_page': 100}
        user_commits = self.api.get_all_pages(url, params)
        has_user_commits = bool(user_commits and len(user_commits) > 0)

        params = {'per_page': 100}
        all_commits = self.api.get_all_pages(url, params)
        if all_commits:
            authors = self._extract_usernames_from_items(all_commits, 'author')
            self.collaboration.add_multiple_collaborators('commit_authors', authors)

        return has_user_commits

    def check_prs_in_repo(self, owner, repo):
        url = f"{self.api.base_url}/repos/{owner}/{repo}/pulls"
        params = {'state': 'all', 'per_page': 100}
        pulls = self.api.get_all_pages(url, params)
        found_user_prs = False
        if pulls:
            for pr in pulls:
                pr_author = pr['user']['login']
                if pr_author.lower() == self.username.lower():
                    found_user_prs = True
                    reviews_url = pr['url'] + '/reviews'
                    reviews = self.api.get_all_pages(reviews_url)
                    if reviews:
                        reviewers = self._extract_usernames_from_items(reviews, 'user')
                        self.collaboration.add_multiple_collaborators('pr_reviewers', reviewers)
                elif owner == self.username:
                    self.collaboration.add_pr_author(pr_author)
                comments_url = pr['comments_url']
                comments = self.api.get_all_pages(comments_url)
                if comments:
                    commenters = self._extract_usernames_from_items(comments, 'user')
                    self.collaboration.add_multiple_collaborators('issue_commenters', commenters)

        return found_user_prs

    def check_issues_in_repo(self, owner, repo):
        url = f"{self.api.base_url}/repos/{owner}/{repo}/issues"
        params = {'state': 'all', 'per_page': 100}
        issues = self.api.get_all_pages(url, params)
        found_user_issues = False
        if issues:
            for issue in issues:
                issue_author = issue['user']['login']
                if issue_author.lower() == self.username.lower():
                    found_user_issues = True
                    comments_url = issue['comments_url']
                    comments = self.api.get_all_pages(comments_url)
                    if comments:
                        commenters = self._extract_usernames_from_items(comments, 'user')
                        self.collaboration.add_multiple_collaborators('issue_commenters', commenters)
                elif owner == self.username:
                    self.collaboration.add_issue_author(issue_author)
                    comments_url = issue['comments_url']
                    comments = self.api.get_all_pages(comments_url)
                    if comments:
                        commenters = self._extract_usernames_from_items(comments, 'user')
                        self.collaboration.add_multiple_collaborators('issue_commenters', commenters)

        return found_user_issues

    def get_starred_repositories(self):
        print("\nПолучаем звезды...")
        url = f"{self.api.base_url}/users/{self.username}/starred"
        starred_data = self.api.get_all_pages(url)

        if starred_data:
            for repo in starred_data:
                repo_full_name = repo['full_name']
                self.starred_repos.add(repo_full_name)
                owner = repo_full_name.split('/')[0]
                self.collaboration.add_starred_owner(owner)

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
            owner, repo_name_only = repo_name.split('/')
            print("---")
            print(repo_name_only)
            if self.check_commits_in_repo(owner, repo_name_only):
                self.commit_repos.add(repo_name)
                print(f" - Коммиты: {repo_name}")
            if self.check_prs_in_repo(owner, repo_name_only):
                self.pr_repos.add(repo_name)
                print(f" - PR: {repo_name}")
            if self.check_issues_in_repo(owner, repo_name_only):
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
        self.collaboration.print_summary()


def main():
    username = input("Введите имя пользователя GitHub: ").strip()
    if not username:
        print("Имя пользователя не может быть пустым!")
        return

    api_client = GitHubAPIClient()
    collaboration_collector = CollaborationCollector(username)
    collector = InteractionCollector(
        username=username,
        api_client=api_client,
        collaboration_collector=collaboration_collector
    )
    collector.collect_interaction_repos()


if __name__ == "__main__":
    main()
