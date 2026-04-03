import json
import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import requests
import seaborn as sns


class GitHubTrendAnalyzer:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Trend-Analyzer"
        }

    def get_trending_repositories(self, language, days, min_stars=0):
        # Используем текущую дату корректно
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Правильный синтаксис GitHub Search API
        # Ищем репозитории с недавними обновлениями
        query = f"language:{language} pushed:>{since_date}"

        # Добавляем фильтр звёзд если указан
        if min_stars > 0:
            query += f" stars:>={min_stars}"

        return self._search_repositories(query, per_page=30)

    def _search_repositories(self, query, per_page=30):
        # Выполнение поискового запроса к GitHub API
        search_url = f"{self.base_url}/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page
        }

        try:
            response = requests.get(search_url, headers=self.headers, params=params,  timeout=30)

            if response.status_code == 403:
                print("Превышен лимит запросов. Рекомендуется использовать GitHub Token.")
                print("Получите токен: https://github.com/settings/tokens")
                return []

            if response.status_code == 422:
                print(f"Ошибка в запросе: {response.text}")
                return []

            response.raise_for_status()
            data = response.json()

            repositories = []
            for repo in data.get("items", []):
                repo_data = self._extract_repo_data(repo)
                if repo_data:
                    repositories.append(repo_data)

            return repositories

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к GitHub API: {e}")
            return []

    def _extract_repo_data(self, repo):
        try:
            created_at = datetime.strptime(repo.get("created_at", ""), "%Y-%m-%dT%H:%M:%SZ")
            days_since_creation = (datetime.now() - created_at).days

            total_stars = repo.get("stargazers_count", 0)
            description = repo.get("description") or "Нет описания"

            # Расчет новых звёзд:
            # Если репозиторий создан недавно (< 30 дней), все звёзды - новые
            # Иначе оцениваем через активность (примерно 5-10% от общих за период)
            if days_since_creation <= 30:
                new_stars = total_stars
            else:
                # Для старых репозиториев: оценка на основе периода
                # Предполагаем, что активные репозитории получают ~0.5% звёзд в день
                new_stars = max(int(total_stars * 0.005 * min(days_since_creation, 30)), 100)

            # Ограничиваем new_stars разумными пределами
            new_stars = min(new_stars, total_stars)

            return {
                "name": repo.get("name", "N/A"),
                "full_name": repo.get("full_name", "N/A"),
                "owner": repo.get("owner", {}).get("login", "N/A"),
                "description": description,
                "html_url": repo.get("html_url", ""),
                "language": repo.get("language", "N/A"),
                "total_stars": total_stars,
                "new_stars": new_stars,
                "forks_count": repo.get("forks_count", 0),
                "open_issues": repo.get("open_issues_count", 0),
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
                "days_since_creation": days_since_creation
            }

        except (ValueError, KeyError, AttributeError) as e:
            print(f"Ошибка обработки данных репозитория: {e}")
            return None

    def visualize_trends(self, repositories, language, days, save_path="trend_chart.png"):
        # Визуализация трендов GitHub репозиториев
        if not repositories:
            print("Нет данных для визуализации")
            return None

        self._setup_plot_style()
        display_names, new_stars, total_stars = self._prepare_chart_data(repositories)

        # Убираем неиспользуемую переменную fig
        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Уменьшено количество аргументов - language и days передаются в параметрах стиля
        self._create_new_stars_chart(ax1, display_names, new_stars, language, days)
        self._create_total_stars_chart(ax2, display_names, total_stars)

        plt.suptitle(f"GitHub Trending Analysis: {language}", fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()

        return self._save_and_show_plot(save_path)

    def _setup_plot_style(self):
        # Настройка стиля графиков
        sns.set_style("whitegrid")
        plt.rcParams['font.family'] = 'DejaVu Sans'

    def _prepare_chart_data(self, repositories):
        # Подготовка данных для визуализации
        top_repos = repositories[:5]

        display_names = []
        for repo in top_repos:
            name = repo["full_name"]
            if len(name) > 25:
                name = name[:22] + "..."
            display_names.append(name)

        new_stars = [repo.get("new_stars", 0) for repo in top_repos]
        total_stars = [repo.get("total_stars", 0) for repo in top_repos]

        return display_names, new_stars, total_stars

    def _create_new_stars_chart(self, ax, display_names, stars_data, language):
        # Создание графика новых звёзд
        colors = sns.color_palette("viridis", len(display_names))

        rects = ax.barh(display_names, stars_data, color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xlabel("New Stars (estimated)", fontsize=12, fontweight='bold')
        ax.set_title(
            f"Fastest Growing {language} Repositories\n",
            fontsize=14, fontweight='bold', pad=20
        )
        ax.invert_yaxis()

        if stars_data and max(stars_data) > 0:
            max_val = max(stars_data)
            for rect, value in zip(rects, stars_data):
                if value > 0:
                    ax.text(
                        value + max_val * 0.01,
                        rect.get_y() + rect.get_height() / 2,
                        f"+{value:,}",
                        va='center',
                        fontsize=10,
                        fontweight='bold',
                        color='darkgreen'
                    )

    def _create_total_stars_chart(self, ax, display_names, stars_data):
        # Создание графика общих звёзд
        colors = sns.color_palette("viridis", len(display_names))

        xlabel = "Total Stars"
        title = "Total Popularity"
        color_label = 'navy'
        value_prefix = ""

        # Переименована переменная bar -> rect
        rects = ax.barh(display_names, stars_data, color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.invert_yaxis()

        if stars_data and max(stars_data) > 0:
            for rect, value in zip(rects, stars_data):
                if value > 0:
                    ax.text(
                        value + max(stars_data) * 0.01,
                        rect.get_y() + rect.get_height() / 2,
                        f"{value_prefix}{value:,}",
                        va='center',
                        fontsize=10,
                        fontweight='bold',
                        color=color_label
                    )

    def _save_and_show_plot(self, save_path):
        # Сохранение и отображение графика
        try:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"\nГрафик сохранён в: {os.path.abspath(save_path)}")
            plt.show()
            return save_path
        except (OSError, IOError) as e:
            print(f"Ошибка сохранения графика: {e}")
            plt.show()
            return None

    def generate_report(self, repositories, language, days, save_path="trend_report.json"):
        # Генерация отчёта в JSON формате
        report = {
            "analysis_metadata": {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "language": language,
                "period_days": days,
                "api_used": "GitHub Search API",
                "total_found": len(repositories)
            },
            "repositories": []
        }

        for i, repo in enumerate(repositories, 1):
            report["repositories"].append({
                "rank": i,
                "name": repo["full_name"],
                "description": repo["description"],
                "url": repo["html_url"],
                "stars": {
                    "total": repo["total_stars"],
                    "new_estimated": repo["new_stars"]
                },
                "forks": repo["forks_count"],
                "issues": repo["open_issues"],
                "language": repo["language"],
                "days_since_creation": repo.get("days_since_creation", 0)
            })

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"Отчёт сохранён в: {os.path.abspath(save_path)}")
            return save_path
        except (OSError, IOError) as e:
            print(f"Ошибка сохранения отчёта: {e}")
            return None

    def print_top_repositories(self, repositories, top_n=5):
        if not repositories:
            print("Репозитории не найдены")
            return

        print(f"\nТОП-{min(top_n, len(repositories))} ТРЕНДОВЫХ РЕПОЗИТОРИЕВ:\n")

        for i, repo in enumerate(repositories[:top_n], 1):
            new_stars = repo.get("new_stars", 0)
            total_stars = repo.get("total_stars", 0)
            forks = repo.get("forks_count", 0)

            print(f"{i}. {repo['full_name']}")
            print(f"   +{new_stars:,} new stars (estimated) | {total_stars:,} total stars")
            print(f"   Forks: {forks:,} | Issues: {repo.get('open_issues', 0)}")
            print(f"   Desc: {repo.get('description', 'No description')}")
            print(f"   URL: {repo.get('html_url')}")
            print()


def main():
    print("GITHUB TRENDING REPOSITORIES ANALYZER")

    analyzer = GitHubTrendAnalyzer()

    # Ввод параметров
    language = input("\nProgramming language (Python, JavaScript, Go, etc.): ").strip()
    if not language:
        language = "Python"
        print(f"Default: {language}")

    period = input("Period (7/30 days): ").strip()
    days = 30 if period == "30" else 7

    # Enter для пропуска min_stars
    min_stars_input = input("Min stars filter (optional, Enter to skip): ").strip()
    min_stars = int(min_stars_input) if min_stars_input.isdigit() else 0

    print(f"\nAnalyzing {language} repositories (last {days} days)...")
    if min_stars > 0:
        print(f"Filter: min {min_stars} stars\n")

    # Получение данных
    repositories = analyzer.get_trending_repositories(language, days, min_stars)

    if not repositories:
        print("\nERROR: No data retrieved.")
        print("Possible reasons:")
        print("1. API rate limit exceeded (provide GitHub Token)")
        print("2. No repositories match criteria")
        print("3. Network issues")
        return

    # Вывод и сохранение
    analyzer.print_top_repositories(repositories, top_n=5)
    chart_path = analyzer.visualize_trends(repositories, language, days)
    report_path = analyzer.generate_report(repositories, language, days)

    # Итоги
    print("\nANALYSIS COMPLETE\n")
    print(f"Repositories analyzed: {len(repositories)}")
    if chart_path:
        print(f"Chart saved: {chart_path}")
    if report_path:
        print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
