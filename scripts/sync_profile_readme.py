#!/usr/bin/env python3
"""Generate dynamic sections for the GitHub profile README.

Features:
- Scrape pinned repos from public profile page.
- Pull each pinned repo README.
- Extract demo media links (mp4/webm/gif or README demo links).
- Render markdown section and inject into README markers.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List

import requests


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
GENERATED_DIR = ROOT / ".generated"
PINNED_JSON_PATH = GENERATED_DIR / "pinned_projects.json"
PINNED_MD_PATH = GENERATED_DIR / "pinned_projects.md"

PROFILE_USER = "RitwijParmar"
PROFILE_URL = f"https://github.com/{PROFILE_USER}"

START_MARKER = "<!-- START:DYNAMIC_PINNED -->"
END_MARKER = "<!-- END:DYNAMIC_PINNED -->"
DESCRIPTION_MAX_CHARS = 135


@dataclass
class ProjectMedia:
    kind: str
    url: str
    source: str


@dataclass
class PinnedProject:
    repo: str
    url: str
    description: str
    language: str
    stars: int
    readme_branch: str
    media: List[ProjectMedia]


def _get(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def get_pinned_repos(username: str) -> List[str]:
    html = _get(f"https://github.com/{username}")
    # The profile HTML includes PINNED_REPO marker near each pinned href.
    repos = re.findall(r"PINNED_REPO.*?href=\"/%s/([^\"]+)\"" % re.escape(username), html)
    ordered_unique = []
    seen = set()
    for repo in repos:
        if repo not in seen:
            ordered_unique.append(repo)
            seen.add(repo)
    return ordered_unique


def get_repo_metadata(username: str, repo: str) -> dict:
    api_url = f"https://api.github.com/repos/{username}/{repo}"
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    return response.json()


def _normalize_link(link: str, username: str, repo: str, branch: str) -> str:
    if link.startswith("http://") or link.startswith("https://"):
        return link
    # Treat as repository-relative path.
    clean = link.lstrip("./")
    return f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/{clean}"


def _compact_description(text: str, max_chars: int = 220) -> str:
    clean = " ".join((text or "").split()).strip()
    if not clean:
        return ""

    # Prefer a natural short clause over hard truncation.
    for sep in (". ", "; ", ", and ", ", "):
        if sep in clean:
            candidate = clean.split(sep, 1)[0].strip().rstrip(" .,;")
            if 30 <= len(candidate) <= max_chars:
                return candidate

    sentences = re.split(r"(?<=[.!?])\s+", clean)
    if sentences:
        first_sentence = sentences[0].strip()
        if 30 <= len(first_sentence) <= max_chars:
            return first_sentence.rstrip(" .,;")

    if len(clean) <= max_chars:
        return clean.rstrip(" .,;")

    trimmed = clean[:max_chars].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return trimmed + "..."


def _extract_media_links(readme_text: str, username: str, repo: str, branch: str) -> List[ProjectMedia]:
    media: List[ProjectMedia] = []
    seen = set()

    def add(kind: str, url: str, source: str) -> None:
        if url in seen:
            return
        seen.add(url)
        media.append(ProjectMedia(kind=kind, url=url, source=source))

    # 1) Markdown links with video extensions.
    for match in re.findall(r"\[[^\]]*\]\(([^)]+)\)", readme_text):
        normalized = _normalize_link(match, username, repo, branch)
        lower = normalized.lower()
        if lower.endswith((".mp4", ".webm", ".mov")):
            add("video", normalized, "markdown_link")

    # 2) HTML video tags.
    for match in re.findall(r"<video[^>]*src=[\"']([^\"']+)", readme_text, flags=re.IGNORECASE):
        normalized = _normalize_link(match, username, repo, branch)
        add("video", normalized, "html_video")

    # 3) GitHub user-attachment assets often host demo videos.
    for match in re.findall(r"https://github.com/user-attachments/assets/[A-Za-z0-9\-]+", readme_text):
        add("video", match, "user_attachment")

    return media


def fetch_readme(username: str, repo: str) -> tuple[str, str]:
    for branch in ("main", "master"):
        # Resolve branch -> commit SHA first to avoid stale CDN reads on branch aliases.
        commit_api = f"https://api.github.com/repos/{username}/{repo}/commits/{branch}"
        commit_res = requests.get(commit_api, timeout=30)
        if commit_res.status_code != 200:
            continue
        sha = commit_res.json().get("sha")
        if not sha:
            continue

        raw_url = f"https://raw.githubusercontent.com/{username}/{repo}/{sha}/README.md"
        readme_res = requests.get(raw_url, timeout=30)
        if readme_res.status_code == 200:
            return branch, readme_res.text
    return "main", ""


def build_project_records(username: str, repos: Iterable[str]) -> List[PinnedProject]:
    records: List[PinnedProject] = []
    for repo in repos:
        meta = get_repo_metadata(username, repo)
        branch, readme = fetch_readme(username, repo)
        media = _extract_media_links(readme, username, repo, branch)
        records.append(
            PinnedProject(
                repo=repo,
                url=f"https://github.com/{username}/{repo}",
                description=_compact_description((meta.get("description") or "").strip(), DESCRIPTION_MAX_CHARS),
                language=meta.get("language") or "N/A",
                stars=int(meta.get("stargazers_count") or 0),
                readme_branch=branch,
                media=media[:1],  # keep profile concise
            )
        )
    return records


def _render_media_block(project: PinnedProject) -> str:
    if not project.media:
        return "_Demo video not linked in project README yet._"

    lines = []
    priority = {"video": 0}
    sorted_media = sorted(project.media, key=lambda item: priority.get(item.kind, 9))
    for item in sorted_media[:1]:
        if item.kind == "video":
            lines.append(
                f'<video src="{item.url}" controls muted playsinline width="100%"></video>'
            )
    return "\n".join(lines)


def render_pinned_markdown(projects: List[PinnedProject]) -> str:
    parts: List[str] = []
    for project in projects:
        media_block = _render_media_block(project)
        parts.extend(
            [
                f"### [{project.repo}]({project.url})",
                f"{project.description or 'No repository description yet.'}",
                f"`{project.language}` | ⭐ `{project.stars}` | [Repository]({project.url})",
                "",
                media_block,
                "",
            ]
        )
    return "\n".join(parts).rstrip() + "\n"


def inject_section(readme_text: str, section: str) -> str:
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        flags=re.DOTALL,
    )
    replacement = f"{START_MARKER}\n{section}{END_MARKER}"
    if pattern.search(readme_text):
        return pattern.sub(replacement, readme_text)
    return readme_text.rstrip() + "\n\n" + replacement + "\n"


def main() -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    pinned = get_pinned_repos(PROFILE_USER)[:3]
    projects = build_project_records(PROFILE_USER, pinned)

    data = {
        "profile": PROFILE_URL,
        "pinned_repos": pinned,
        "projects": [
            {
                **asdict(p),
                "media": [asdict(m) for m in p.media],
            }
            for p in projects
        ],
    }
    PINNED_JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    dynamic_section = render_pinned_markdown(projects)
    PINNED_MD_PATH.write_text(dynamic_section, encoding="utf-8")

    if README_PATH.exists():
        readme_text = README_PATH.read_text(encoding="utf-8")
    else:
        readme_text = "# Ritwij Aryan Parmar\n\n"

    updated = inject_section(readme_text, dynamic_section)
    README_PATH.write_text(updated, encoding="utf-8")
    print(f"Updated {README_PATH}")
    print(f"Wrote {PINNED_JSON_PATH}")
    print(f"Wrote {PINNED_MD_PATH}")


if __name__ == "__main__":
    main()
