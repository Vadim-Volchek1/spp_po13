import os
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv

# Авторизация через Personal Access Token (PAT)
# Загружаем переменные из .env
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
g = Github(token)

topic = input("Введите тему для анализа (например, machine learning): ")
print(f"Анализируем 100 популярных репозиториев по теме '{topic}'...")

# Поиск репозиториев
query = f"{topic} stars:>1"
repositories = g.search_repositories(query=query, sort="stars", order="desc")

data = []
limit = 100
count = 0

for repo in repositories:
    if count >= limit:
        break

    data.append(
        {
            "name": repo.full_name,
            "language": repo.language if repo.language else "Unknown",
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "issues": repo.open_issues_count,
            "updated_at": repo.updated_at,
        }
    )
    count += 1

# Превращаем в таблицу Pandas
df = pd.DataFrame(data)

# АНАЛИЗ

# Рейтинг языков
lang_counts = df["language"].value_counts(normalize=True) * 100

# Самый звездный
top_repo = df.loc[df["stars"].idxmax()]

# Среднее количество форков
avg_forks = df["forks"].mean()

# Процент старения (не обновлялись больше года)
year_ago = datetime.now(timezone.utc) - timedelta(days=365)
stale_repos = df[df["updated_at"] < year_ago]
stale_percent = (len(stale_repos) / len(df)) * 100

# Рассчитываем "возраст" последнего обновления в днях
now = datetime.now(timezone.utc)
df["age_days"] = (now - df["updated_at"]).dt.days

# ВЫВОД В КОНСОЛЬ
print("\nСамые популярные языки:")
for lang, percent in lang_counts.head(5).items():
    print(f" - {lang} ({percent:.1f}%)")

print(
    f"\nСамый звездный репозиторий: \"{top_repo['name']}\" ({top_repo['stars']/1000:.1f}k звёзд)"
)
print(f"Среднее количество форков: {avg_forks:.1f}")
print(f"{stale_percent:.0f}% репозиториев не обновлялись больше года!")

# ВИЗУАЛИЗАЦИЯ

# График 1: Языки (Круговая диаграмма)
plt.figure(1, figsize=(10, 6))
lang_counts.head(7).plot(kind="pie", autopct="%1.1f%%", startangle=140)
plt.title(f"Популярные языки в теме {topic}")
plt.ylabel("")  # Убираем лишнюю подпись
plt.savefig(f"{topic.replace(' ', '_')}_languages.png")

# График 2: Распределение звезд (Гистограмма)
plt.figure(2, figsize=(10, 6))
plt.hist(df["stars"], bins=20, color="skyblue", edgecolor="black")
plt.title("Распределение звёзд среди ТОП-100")
plt.xlabel("Количество звёзд")
plt.ylabel("Количество репозиториев")


# График 3: Старение репозиториев (Гистограмма)
plt.figure(3, figsize=(10, 6))
plt.hist(df["age_days"], bins=15, color="salmon", edgecolor="black", alpha=0.7)

# Добавляем вертикальную линию "1 год"
plt.axvline(
    365, color="red", linestyle="dashed", linewidth=2, label="1 год без обновлений"
)

plt.title(f"График 'старения' репозиториев по теме: {topic}")
plt.xlabel("Дней с последнего обновления")
plt.ylabel("Количество репозиториев")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

print("Вывожу графики на экран...")
plt.show()
