#!/usr/bin/env python3
"""
GitHub Contributor Activity Analyzer
Анализирует активность контрибьюторов в указанном репозитории за определенный период
"""

import sys
import time
import traceback
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor

import requests
import matplotlib.pyplot as plt
import numpy as np

# Настройка русских шрифтов для matplotlib
plt.rcParams["font.family"] = ["DejaVu Sans", "Arial", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False


class ChartData:
    """Класс для хранения данных для графиков"""

    def __init__(self, data: Dict[str, List]):
        """
        Инициализация данных для графиков

        Args:
            data: словарь с данными (logins, commits, prs, issues, comments)
        """
        self.logins = data.get("logins", [])
        self.commits = data.get("commits", [])
        self.prs = data.get("prs", [])
        self.issues = data.get("issues", [])
        self.comments = data.get("comments", [])


class GitHubContributorAnalyzer:
    """Класс для анализа активности контрибьюторов GitHub"""

    def __init__(self, repo: str, token: Optional[str] = None):
        """
        Инициализация анализатора

        Args:
            repo: репозиторий в формате owner/repo
            token: GitHub токен для увеличения лимита запросов (опционально)
        """
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Contributor-Analyzer/1.0",
        }

        if token:
            self.headers["Authorization"] = f"token {token}"
            print("✓ Используется GitHub токен для аутентификации")

        self.owner, self.repo_name = repo.split("/")

        # Периоды в днях
        self.periods = {"week": 7, "month": 30, "year": 365}

        # Результаты анализа
        self.contributors = defaultdict(
            lambda: {
                "commits": 0,
                "additions": 0,
                "deletions": 0,
                "prs_opened": 0,
                "prs_closed": 0,
                "issues_opened": 0,
                "issues_closed": 0,
                "comments": 0,
                "pr_comments": 0,
                "issue_comments": 0,
                "login": "",
                "name": "",
                "avatar": "",
                "activity_score": 0,
            }
        )

    def _check_rate_limit(self, response: requests.Response) -> None:
        """Проверка лимитов API и ожидание при необходимости"""
        remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
        if remaining < 10:
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            wait_time = max(0, reset_time - time.time())
            if wait_time > 0:
                print(
                    f"  ⚠ Предупреждение: осталось {remaining} запросов. "
                    f"Ожидание {wait_time:.0f} секунд..."
                )
                time.sleep(wait_time)

    def _make_request(self, url: str, params: Dict = None) -> List[Dict]:
        """
        Выполнение запроса к GitHub API с обработкой пагинации
        """
        results = []
        page = 1

        while True:
            if params is None:
                params = {}
            params["page"] = page
            params["per_page"] = 100

            try:
                response = requests.get(
                    url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()

                self._check_rate_limit(response)

                data = response.json()
                if not data:
                    break

                if isinstance(data, list):
                    results.extend(data)
                else:
                    results.append(data)

                # Проверка на наличие следующей страницы
                link_header = response.headers.get("Link", "")
                if 'rel="next"' not in link_header:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"  ✗ Ошибка при запросе {url}: {e}")
                break

        return results

    def _print_analysis_header(self, since_date: datetime, min_commits: int) -> None:
        """Вывод заголовка анализа"""
        print(f"\n📊 Анализ контрибьюторов репозитория {self.repo}")
        print(
            f"📅 Период анализа: с {since_date.strftime('%Y-%m-%d')} "
            f"по {datetime.now().strftime('%Y-%m-%d')}"
        )
        print(f"🔍 Минимальное количество коммитов: {min_commits}\n")

    def _fetch_contributors_list(self, min_commits: int) -> List[Dict]:
        """Получение списка контрибьюторов"""
        print("1. Получение списка контрибьюторов...")
        contributors_url = f"{self.base_url}/repos/{self.repo}/contributors"
        contributors = self._make_request(contributors_url)

        # Фильтруем контрибьюторов с достаточным количеством коммитов
        contributors = [c for c in contributors if c["contributions"] >= min_commits]
        print(f"   Найдено {len(contributors)} контрибьюторов " f"(после фильтрации)\n")
        return contributors

    def _process_contributor_data(self, login: str, since_date: datetime) -> None:
        """Обработка данных одного контрибьютора"""
        self._get_commits_stats(login, since_date)
        self._get_prs_stats(login, since_date)
        self._get_issues_stats(login, since_date)
        self._get_comments_stats(login, since_date)

    def _calculate_activity_scores(self) -> None:
        """Расчет баллов активности для всех контрибьюторов"""
        for stats in self.contributors.values():
            stats["activity_score"] = (
                stats["commits"] * 5
                + stats["prs_opened"] * 3
                + stats["issues_opened"] * 2
                + stats["comments"] * 1
                + (stats["additions"] + stats["deletions"]) / 100
            )

    def get_contributors_stats(
        self, since_date: datetime, min_commits: int = 0
    ) -> Dict:
        """
        Получение полной статистики по контрибьюторам
        """
        self._print_analysis_header(since_date, min_commits)

        # Получение списка контрибьюторов
        contributors = self._fetch_contributors_list(min_commits)

        if not contributors:
            return {}

        # Устанавливаем логины контрибьюторов
        for contributor in contributors:
            login = contributor["login"]
            self.contributors[login]["login"] = login
            self.contributors[login]["avatar"] = contributor.get("avatar_url", "")

        # Собираем данные по каждому контрибьютору
        print("2. Сбор детальной статистики...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for contributor in contributors:
                login = contributor["login"]
                futures.append(
                    executor.submit(self._process_contributor_data, login, since_date)
                )

            for i, future in enumerate(futures, 1):
                future.result()  # Ждем завершения
                if i % 20 == 0:
                    print(f"   Обработано {i}/{len(futures)} задач...")

        print("   Сбор данных завершен\n")

        # Рассчитываем баллы активности
        self._calculate_activity_scores()

        # Фильтруем по минимальному количеству коммитов
        filtered = {
            login: stats
            for login, stats in self.contributors.items()
            if stats["commits"] >= min_commits
        }

        return filtered

    def _get_commits_stats(self, contributor: str, since_date: datetime) -> None:
        """Получение статистики коммитов"""
        commits_url = f"{self.base_url}/repos/{self.repo}/commits"
        params = {
            "author": contributor,
            "since": since_date.isoformat(),
            "until": datetime.now().isoformat(),
        }

        commits = self._make_request(commits_url, params)
        self.contributors[contributor]["commits"] = len(commits)

        # Получение детальной статистики изменений для коммитов
        for commit in commits[:30]:
            try:
                commit_url = commit["url"]
                response = requests.get(commit_url, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    commit_data = response.json()
                    if "stats" in commit_data:
                        self.contributors[contributor]["additions"] += commit_data[
                            "stats"
                        ].get("additions", 0)
                        self.contributors[contributor]["deletions"] += commit_data[
                            "stats"
                        ].get("deletions", 0)
            except (requests.RequestException, KeyError, ValueError):
                continue

    def _get_prs_stats(self, contributor: str, since_date: datetime) -> None:
        """Получение статистики Pull Requests"""
        prs_url = f"{self.base_url}/repos/{self.repo}/pulls"
        params = {"state": "all", "since": since_date.isoformat()}

        all_prs = self._make_request(prs_url, params)

        for pr in all_prs:
            if pr["user"]["login"] == contributor:
                self.contributors[contributor]["prs_opened"] += 1
                if pr["state"] == "closed":
                    self.contributors[contributor]["prs_closed"] += 1

    def _get_issues_stats(self, contributor: str, since_date: datetime) -> None:
        """Получение статистики Issues"""
        issues_url = f"{self.base_url}/repos/{self.repo}/issues"
        params = {"state": "all", "since": since_date.isoformat(), "filter": "all"}

        all_issues = self._make_request(issues_url, params)

        for issue in all_issues:
            # Игнорируем PR, так как они уже учтены
            if "pull_request" in issue:
                continue

            if issue["user"]["login"] == contributor:
                self.contributors[contributor]["issues_opened"] += 1
                if issue["state"] == "closed":
                    self.contributors[contributor]["issues_closed"] += 1

    def _get_comments_stats(self, contributor: str, since_date: datetime) -> None:
        """Получение статистики комментариев"""
        comments_url = f"{self.base_url}/repos/{self.repo}/issues/comments"
        params = {"since": since_date.isoformat()}

        comments = self._make_request(comments_url, params)

        for comment in comments:
            if comment["user"]["login"] == contributor:
                self.contributors[contributor]["comments"] += 1
                # Определяем тип комментария (PR или Issue)
                issue_url = comment.get("issue_url", "")
                if "/pulls/" in issue_url:
                    self.contributors[contributor]["pr_comments"] += 1
                else:
                    self.contributors[contributor]["issue_comments"] += 1

    def get_top_contributors(self, top_n: int = 5) -> List[Tuple[str, Dict]]:
        """Получение топ N контрибьюторов по активности"""
        sorted_contributors = sorted(
            self.contributors.items(),
            key=lambda x: x[1]["activity_score"],
            reverse=True,
        )
        return sorted_contributors[:top_n]

    def _print_contributor_stats(self, rank: int, login: str, stats: Dict) -> None:
        """Вывод статистики одного контрибьютора"""
        print(f"\n{rank}. @{login}")
        print(f"   ├─ 📝 Коммиты: {stats['commits']}")
        print(
            f"   ├─ 💻 Изменения кода: +{stats['additions']} / "
            f"-{stats['deletions']} строк"
        )
        print(
            f"   ├─ 🔀 Pull Requests: открыто {stats['prs_opened']} / "
            f"закрыто {stats['prs_closed']}"
        )
        print(
            f"   ├─ 🐛 Issues: открыто {stats['issues_opened']} / "
            f"закрыто {stats['issues_closed']}"
        )
        print(
            f"   ├─ 💬 Комментарии: {stats['comments']} "
            f"(PR: {stats['pr_comments']}, Issues: {stats['issue_comments']})"
        )
        print(f"   └─ ⭐ Активность: {stats['activity_score']:.1f} баллов")

    def print_report(self, top_contributors: List[Tuple[str, Dict]]) -> None:
        """Вывод отчета в консоль"""
        print("\n" + "=" * 80)
        print(f"📈 ТОП-5 АКТИВНЫХ КОНТРИБЬЮТОРОВ В {self.repo.upper()}")
        print("=" * 80)

        for i, (login, stats) in enumerate(top_contributors, 1):
            self._print_contributor_stats(i, login, stats)

        print("\n" + "=" * 80)

    def _prepare_chart_data(
        self, top_contributors: List[Tuple[str, Dict]]
    ) -> ChartData:
        """Подготовка данных для графиков"""
        chart_dict = {
            "logins": [f"@{login}" for login, _ in top_contributors],
            "commits": [stats["commits"] for _, stats in top_contributors],
            "prs": [stats["prs_opened"] for _, stats in top_contributors],
            "issues": [stats["issues_opened"] for _, stats in top_contributors],
            "comments": [stats["comments"] for _, stats in top_contributors],
        }

        return ChartData(chart_dict)

    def _create_commits_chart(self, ax: plt.Axes, data: ChartData) -> None:
        """Создание графика коммитов"""
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(data.logins)))
        ax.bar(data.logins, data.commits, color=colors, alpha=0.8)
        ax.set_title("Количество коммитов", fontsize=12, fontweight="bold")
        ax.set_ylabel("Коммиты")
        ax.tick_params(axis="x", rotation=45)

        if data.commits:
            max_val = max(data.commits)
            for i, v in enumerate(data.commits):
                ax.text(i, v + max_val * 0.01, str(v), ha="center", fontsize=9)

    def _create_prs_issues_chart(self, ax: plt.Axes, data: ChartData) -> None:
        """Создание графика PR и Issues"""
        x = np.arange(len(data.logins))
        width = 0.35

        ax.bar(
            x - width / 2,
            data.prs,
            width,
            label="Pull Requests",
            color="#2ecc71",
            alpha=0.8,
        )
        ax.bar(
            x + width / 2,
            data.issues,
            width,
            label="Issues",
            color="#e74c3c",
            alpha=0.8,
        )
        ax.set_title("Pull Requests и Issues", fontsize=12, fontweight="bold")
        ax.set_ylabel("Количество")
        ax.set_xticks(x)
        ax.set_xticklabels(data.logins, rotation=45)
        ax.legend()

    def _create_comments_chart(self, ax: plt.Axes, data: ChartData) -> None:
        """Создание графика комментариев"""
        ax.bar(data.logins, data.comments, color="#3498db", alpha=0.8)
        ax.set_title("Количество комментариев", fontsize=12, fontweight="bold")
        ax.set_ylabel("Комментарии")
        ax.tick_params(axis="x", rotation=45)

        if data.comments:
            max_val = max(data.comments)
            for i, v in enumerate(data.comments):
                ax.text(i, v + max_val * 0.01, str(v), ha="center", fontsize=9)

    def _create_radar_chart(self, top_contributors: List[Tuple[str, Dict]]) -> None:
        """Создание радарной диаграммы для сравнения контрибьюторов"""
        if len(top_contributors) >= 3:
            metrics = ["Коммиты", "PR", "Issues", "Комментарии", "Изменения"]
            top3_data = []

            # Нормализуем данные для топ-3
            max_commits = max(s["commits"] for _, s in top_contributors[:3])
            max_prs = max(s["prs_opened"] for _, s in top_contributors[:3])
            max_issues = max(s["issues_opened"] for _, s in top_contributors[:3])
            max_comments = max(s["comments"] for _, s in top_contributors[:3])

            for _, stats in top_contributors[:3]:
                normalized = [
                    stats["commits"] / max_commits if max_commits > 0 else 0,
                    stats["prs_opened"] / max_prs if max_prs > 0 else 0,
                    stats["issues_opened"] / max_issues if max_issues > 0 else 0,
                    stats["comments"] / max_comments if max_comments > 0 else 0,
                    min((stats["additions"] + stats["deletions"]) / 1000, 1),
                ]
                top3_data.append(normalized)

            # Радарная диаграмма
            angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
            angles += angles[:1]

            fig = plt.gcf()
            ax = fig.add_subplot(2, 2, 4, projection="polar")
            colors_radar = ["#e74c3c", "#3498db", "#2ecc71"]

            for i, data in enumerate(top3_data):
                data += data[:1]
                ax.plot(
                    angles,
                    data,
                    "o-",
                    linewidth=2,
                    label=f"@{top_contributors[i][0]}",
                    color=colors_radar[i],
                )
                ax.fill(angles, data, alpha=0.1, color=colors_radar[i])

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(metrics)
            ax.set_title(
                "Сравнительная активность", fontsize=12, fontweight="bold", pad=20
            )
            ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
        else:
            fig = plt.gcf()
            ax = fig.add_subplot(2, 2, 4)
            ax.text(
                0.5,
                0.5,
                "Недостаточно данных\nдля радарной диаграммы",
                ha="center",
                va="center",
                fontsize=12,
            )
            ax.set_title("Сравнительная активность", fontsize=12, fontweight="bold")

    def visualize_activity(
        self, top_contributors: List[Tuple[str, Dict]], filename: str = None
    ) -> None:
        """Визуализация активности контрибьюторов"""
        if not top_contributors:
            print("Нет данных для визуализации")
            return

        if filename is None:
            filename = f"{self.repo_name}_contributors.png"

        # Подготовка данных
        chart_data = self._prepare_chart_data(top_contributors)

        # Создание фигуры с несколькими подграфиками
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(
            f"Активность контрибьюторов в репозитории {self.repo}",
            fontsize=16,
            fontweight="bold",
        )

        # Создание графиков
        self._create_commits_chart(axes[0, 0], chart_data)
        self._create_prs_issues_chart(axes[0, 1], chart_data)
        self._create_comments_chart(axes[1, 0], chart_data)

        plt.tight_layout()

        # Создаем радарную диаграмму отдельно, так как она добавляет подграфик
        self._create_radar_chart(top_contributors)

        plt.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"\n📊 Графики активности сохранены в '{filename}'")
        plt.show()

    def _build_html_report(self, top_contributors: List[Tuple[str, Dict]]) -> str:
        """Построение HTML содержимого отчета"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>GitHub Activity Report - {self.repo}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #24292e;
                    border-bottom: 3px solid #0366d6;
                    padding-bottom: 10px;
                }}
                .contributor {{
                    background-color: #f6f8fa;
                    border-left: 4px solid #0366d6;
                    margin: 20px 0;
                    padding: 15px;
                    border-radius: 5px;
                }}
                .contributor h3 {{
                    margin-top: 0;
                    color: #0366d6;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 10px;
                    margin-top: 10px;
                }}
                .stat {{
                    background-color: white;
                    padding: 8px;
                    border-radius: 3px;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                }}
                .stat-value {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #24292e;
                }}
                .stat-label {{
                    font-size: 12px;
                    color: #586069;
                }}
                .badge {{
                    display: inline-block;
                    padding: 2px 6px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .badge-commits {{ background-color: #28a745; color: white; }}
                .badge-prs {{ background-color: #0366d6; color: white; }}
                .badge-issues {{ background-color: #e36209; color: white; }}
                .badge-comments {{ background-color: #6f42c1; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 GitHub Contributor Activity Report</h1>
                <p><strong>Репозиторий:</strong> {self.repo}</p>
                <p><strong>Дата отчета:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

                <h2>🏆 Топ-5 активных контрибьюторов</h2>
        """

        for rank, (login, stats) in enumerate(top_contributors, 1):
            html_content += f"""
                <div class="contributor">
                    <h3>{rank}. @{login}</h3>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-value">{stats['commits']}</div>
                            <div class="stat-label">📝 Коммиты</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">+{stats['additions']}/-{stats['deletions']}</div>
                            <div class="stat-label">💻 Изменения кода</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{stats['prs_opened']}/{stats['prs_closed']}</div>
                            <div class="stat-label">🔀 PR (открыто/закрыто)</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{stats['issues_opened']}/{stats['issues_closed']}</div>
                            <div class="stat-label">🐛 Issues (открыто/закрыто)</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{stats['comments']}</div>
                            <div class="stat-label">💬 Комментарии</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{stats['activity_score']:.1f}</div>
                            <div class="stat-label">⭐ Балл активности</div>
                        </div>
                    </div>
                    <div>
                        <span class="badge badge-commits">Коммиты: {stats['commits']}</span>
                        <span class="badge badge-prs">PR: {stats['prs_opened']}</span>
                        <span class="badge badge-issues">Issues: {stats['issues_opened']}</span>
                        <span class="badge badge-comments">Комментарии: {stats['comments']}</span>
                    </div>
                </div>
            """

        html_content += """
            </div>
        </body>
        </html>
        """

        return html_content

    def generate_html_report(
        self, top_contributors: List[Tuple[str, Dict]], filename: str = None
    ) -> None:
        """Генерация HTML отчета"""
        if filename is None:
            filename = f"{self.repo_name}_report.html"

        html_content = self._build_html_report(top_contributors)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"📄 HTML отчет сохранен в '{filename}'")


def get_user_input() -> Tuple[str, int, int, Optional[str]]:
    """Получение входных данных от пользователя"""
    print("=" * 80)
    print("🐙 GitHub Contributor Activity Analyzer")
    print("Анализ активности контрибьюторов в GitHub репозитории")
    print("=" * 80)

    repo = input("\nВведите репозиторий (owner/repo): ").strip()
    if not repo or "/" not in repo:
        print("Ошибка: неверный формат репозитория. Используйте формат owner/repo")
        sys.exit(1)

    print("\nВыберите период анализа:")
    print("1. Неделя (7 дней)")
    print("2. Месяц (30 дней)")
    print("3. Год (365 дней)")
    period_choice = input("Ваш выбор (1-3): ").strip()

    period_map = {"1": "week", "2": "month", "3": "year"}

    period_key = period_map.get(period_choice, "month")
    days = {"week": 7, "month": 30, "year": 365}[period_key]

    min_commits_input = input(
        "\nМинимальное количество коммитов для попадания в рейтинг "
        "(по умолчанию 0): "
    ).strip()
    min_commits = int(min_commits_input) if min_commits_input else 0

    token = input(
        "\nGitHub токен (опционально, для увеличения лимита запросов): "
    ).strip()
    if not token:
        token = None

    return repo, days, min_commits, token


def main() -> None:
    """Основная функция"""
    try:
        repo, days, min_commits, token = get_user_input()
        since_date = datetime.now() - timedelta(days=days)

        print("\n" + "=" * 80)
        print("🚀 Начинаем анализ...")

        # Создаем анализатор
        analyzer = GitHubContributorAnalyzer(repo, token)

        # Получаем статистику
        contributors = analyzer.get_contributors_stats(since_date, min_commits)

        if not contributors:
            print("\n❌ Не найдено контрибьюторов, удовлетворяющих критериям")
            return

        # Получаем топ-5
        top_contributors = analyzer.get_top_contributors(5)

        # Выводим отчет
        analyzer.print_report(top_contributors)

        # Визуализируем результаты
        analyzer.visualize_activity(top_contributors)

        # Генерируем HTML отчет
        analyzer.generate_html_report(top_contributors)

        print("\n✨ Анализ успешно завершен!")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Ошибка сети: {e}")
        sys.exit(1)
    except (ValueError, KeyError, AttributeError) as e:
        print(f"\n❌ Ошибка обработки данных: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
