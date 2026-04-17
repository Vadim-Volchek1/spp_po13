from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


GITHUB_API_BASE = "https://api.github.com"
DEFAULT_STATE_FILE = "github_release_state.json"


@dataclass
class ReleaseInfo:
    owner: str
    repo: str
    latest_version: str
    published_at: str | None
    html_url: str | None
    body: str | None

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.repo}"


def _read_input_repos(raw: str) -> list[str]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    repos: list[str] = []
    for p in parts:
        if "/" not in p:
            raise ValueError(f"Invalid repo format '{p}'. Expected owner/repo.")
        repos.append(p)
    return repos


def _request_json(url: str, headers: dict[str, str], timeout_s: int = 20) -> dict[str, Any] | list[Any] | None:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                pass
            body = resp.read().decode("utf-8", errors="replace")
            if not body.strip():
                return None
            return json.loads(body)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def _github_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-release-tracker-lr4",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_latest_release(owner: str, repo: str) -> ReleaseInfo | None:
    """
    Fetches the latest published release for {owner}/{repo}.
    If the repository has no releases, returns None.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/releases/latest"
    headers = _github_headers()
    data = _request_json(url, headers=headers)
    if not data:
        return None

    return ReleaseInfo(
        owner=owner,
        repo=repo,
        latest_version=str(data.get("tag_name") or "").strip(),
        published_at=data.get("published_at"),
        html_url=data.get("html_url"),
        body=data.get("body"),
    )


def fetch_latest_tag(owner: str, repo: str) -> ReleaseInfo | None:
    """
    Fallback: if there are no GitHub releases, we consider the latest tag as "latest update".
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/tags?per_page=1"
    headers = _github_headers()
    data = _request_json(url, headers=headers)
    if not data or not isinstance(data, list) or not data:
        return None
    tag = data[0]
    return ReleaseInfo(
        owner=owner,
        repo=repo,
        latest_version=str(tag.get("name") or "").strip(),
        published_at=None,
        html_url=None,
        body=None,
    )


def load_state(state_path: str) -> dict[str, Any]:
    if not os.path.exists(state_path):
        return {"checked_at": None, "items": {}}
    with open(state_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state_path: str, state: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(state_path) or ".", exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _print_update_details(key: str, info: ReleaseInfo, source: str) -> None:
    print(f"Найдено обновление: {key} -> {info.latest_version}" + (f" ({source})" if source else ""))
    if info.published_at:
        print(f"Дата: {info.published_at}")
    if info.html_url:
        print(info.html_url)
    if not info.body:
        print()
        return

    short = info.body.strip()
    if len(short) > 600:
        short = short[:600] + "..."
    if short:
        print("Основные изменения (changelog):")
        print(short)
    print()


def _build_update_payload(key: str, source: str, prev_version: str, info: ReleaseInfo) -> dict[str, Any]:
    return {
        "repo": key,
        "type": source,
        "old_version": prev_version,
        "new_version": info.latest_version,
        "published_at": info.published_at,
        "url": info.html_url,
        "changelog": (info.body or "").strip(),
    }


def _fetch_latest_info(owner: str, repo: str) -> tuple[ReleaseInfo | None, str]:
    info = fetch_latest_release(owner, repo)
    source = "release"
    if info is None:
        info = fetch_latest_tag(owner, repo)
        source = "tag"
    return info, source


def check_repositories(repos: list[str], state_path: str) -> list[dict[str, Any]]:
    """
    Returns a list of updates detected in the current run.
    """
    state = load_state(state_path)
    items: dict[str, Any] = state.get("items", {})

    now_iso = _iso_now()
    updates: list[dict[str, Any]] = []

    for full in repos:
        owner, repo = full.split("/", 1)
        key = f"{owner}/{repo}"

        info, source = _fetch_latest_info(owner, repo)
        if info is None:
            print(f"Skip {key}: cannot fetch latest release/tag.")
            continue

        last_seen = items.get(key, {})
        prev_version = last_seen.get("version")

        is_new = (prev_version is None) or (info.latest_version and info.latest_version != prev_version)
        if is_new and prev_version is not None:
            updates.append(_build_update_payload(key, source, prev_version, info))
            _print_update_details(key, info, source)

        # Update state (also on first run).
        items[key] = {
            "version": info.latest_version,
            "checked_at": now_iso,
            "type": source,
        }

    state["checked_at"] = now_iso
    state["items"] = items
    save_state(state_path, state)

    return updates


def visualize_updates(updates: list[dict[str, Any]], output_png: str) -> None:
    """
    Simple visualization:
    - x axis: repos
    - y axis: ordinal of published_at (if known), otherwise 0
    """
    if not updates:
        print("No new updates found in this run. No graph will be generated.")
        return

    if plt is None:
        print("matplotlib is not available. Skipping visualization graph.")
        return

    x_labels: list[str] = []
    y_values: list[float] = []

    for u in updates:
        x_labels.append(u["repo"])
        published_at = u.get("published_at")
        if published_at:
            try:
                dt = datetime.fromisoformat(str(published_at).replace("Z", "+00:00"))
                y_values.append(dt.timestamp())
            except (TypeError, ValueError):
                y_values.append(0.0)
        else:
            y_values.append(0.0)

    min_y = min(y_values) if y_values else 0.0
    norm = [v - min_y for v in y_values]

    plt.figure(figsize=(12, 5))
    plt.bar(range(len(updates)), norm)
    plt.xticks(range(len(updates)), x_labels, rotation=35, ha="right")
    plt.ylabel("New update date (relative, seconds)")
    plt.title("GitHub releases/tag updates detected (this run)")
    plt.tight_layout()
    plt.savefig(output_png, dpi=150)
    plt.close()

    print(f'График сохранён: "{output_png}"')


def build_report_markdown(updates: list[dict[str, Any]], output_md: str) -> None:
    lines = _build_report_lines(updates)
    os.makedirs(os.path.dirname(output_md) or ".", exist_ok=True)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f'Отчёт сохранён: "{output_md}"')


def _build_report_lines(updates: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = [
        "# GitHub Releases Updates Report (LR4 variant 3)",
        "",
        f"Generated at: {_iso_now()}",
        "",
    ]
    if not updates:
        lines.append("No updates were found in this run.")
        return lines

    for idx, update in enumerate(updates, start=1):
        lines.extend(_render_update_section(idx, update))
    return lines


def _render_update_section(idx: int, update: dict[str, Any]) -> list[str]:
    lines = [
        f"## {idx}) {update['repo']}",
        "",
        f"- Type: `{update['type']}`",
        f"- Old: `{update['old_version']}`",
        f"- New: `{update['new_version']}`",
    ]
    if update.get("published_at"):
        lines.append(f"- Published at: `{update['published_at']}`")
    if update.get("url"):
        lines.append(f"- URL: {update['url']}")
    lines.append("")

    changelog = str(update.get("changelog") or "")
    if changelog:
        if len(changelog) > 4000:
            changelog = changelog[:4000] + "\n...\n"
        lines.extend(["### Changelog", "", changelog, ""])
    else:
        lines.extend(["_No changelog body returned by API._", ""])
    return lines


def main() -> None:
    print("=== LR4: GitHub API (auto-track releases) ===")
    print('Enter repositories to monitor in format "owner/repo", separated by commas.')
    raw = input("Repositories (e.g., django/django, fastapi/fastapi): ").strip()

    repos = _read_input_repos(raw)

    state_path = os.path.join(os.path.dirname(__file__), DEFAULT_STATE_FILE)
    report_md = os.path.join(os.path.dirname(__file__), "..", "rep", "github_updates_report.md")
    graph_png = os.path.join(os.path.dirname(__file__), "..", "rep", "github_updates_graph.png")

    print("\nChecking updates...")
    updates = check_repositories(repos=repos, state_path=state_path)

    build_report_markdown(updates=updates, output_md=report_md)
    visualize_updates(updates=updates, output_png=graph_png)

    print("\nDone.")


if __name__ == "__main__":
    main()
