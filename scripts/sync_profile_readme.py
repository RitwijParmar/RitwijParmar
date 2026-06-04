#!/usr/bin/env python3
"""Render the dynamic project-card section for the GitHub profile README."""

from __future__ import annotations

import html
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
GENERATED_DIR = ROOT / ".generated"
ASSETS_DIR = ROOT / "assets"
PINNED_JSON_PATH = GENERATED_DIR / "pinned_projects.json"
PINNED_MD_PATH = GENERATED_DIR / "pinned_projects.md"
GITHUB_SIGNAL_PATH = ASSETS_DIR / "github-signal.svg"

PROFILE_USER = "RitwijParmar"
START_MARKER = "<!-- START:DYNAMIC_PINNED -->"
END_MARKER = "<!-- END:DYNAMIC_PINNED -->"


@dataclass(frozen=True)
class Project:
    title: str
    repo: str
    description: str
    tags: list[str]
    live_url: str | None = None
    demo_url: str | None = None

    @property
    def repo_url(self) -> str:
        return f"https://github.com/{PROFILE_USER}/{self.repo}"


PROJECTS = [
    Project(
        title="HelixServe",
        repo="HelixServe",
        description=(
            "LLM serving runtime on GCP NVIDIA L4 with paged KV cache, continuous batching, "
            "prefix caching, CUDA Graph decode, and benchmark instrumentation."
        ),
        tags=["Paged KV Cache", "Continuous Batching", "CUDA Graph Decode"],
        demo_url="https://storage.googleapis.com/ritwij-demo-videos-2281c357/helixserve_linkedin_final.mp4",
    ),
    Project(
        title="ManoVarta",
        repo="ManoVarta",
        description=(
            "Controller-led multilingual mental-health GenAI system for English, Hindi, and "
            "Hinglish PHQ-9/GAD-7 item-level assessment with evidence extraction and safety routing."
        ),
        tags=["Evidence Extraction", "PHQ/GAD Scoring", "Safety Routing"],
        live_url="https://manovarta-runtime-ciiiagnzaq-uk.a.run.app",
        demo_url="https://storage.googleapis.com/ritwij-demo-videos-2281c357/manovarta_final_demo.mp4",
    ),
    Project(
        title="SRE-Nidaan",
        repo="SRE-Nidaan",
        description=(
            "Incident response copilot using Next.js, FastAPI, vLLM, telemetry grounding, "
            "runbook retrieval, remediation gating, and analyst feedback loops."
        ),
        tags=["Telemetry Grounding", "Remediation Gates", "RLHF Pipeline"],
        live_url="https://sre-nidaan-122722888597.us-east4.run.app",
        demo_url="https://storage.googleapis.com/ritwij-demo-videos-2281c357/sre_nidaan_demo.mp4",
    ),
    Project(
        title="Nervaflow Intelligence",
        repo="nervaflow-intelligence",
        description=(
            "Cloud-native decision engine for supply operations using Vertex AI Search, "
            "conversational APIs, BigQuery pipelines, operational traces, and cost attribution."
        ),
        tags=["Vertex AI Search", "BigQuery Cost Attribution", "Playbook Tracing"],
        demo_url=(
            "https://raw.githubusercontent.com/RitwijParmar/nervaflow-intelligence/main/"
            "artifacts/video/nervaflow_demo_linkedin_1080p.mp4"
        ),
    ),
]


def get_repo_meta(repo: str) -> dict:
    url = f"https://api.github.com/repos/{PROFILE_USER}/{repo}"
    headers = {"User-Agent": "ritwij-profile-sync"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}


def badge(label: str, value: str, color: str, logo: str | None = None) -> str:
    safe_label = quote(label.replace("-", "--"), safe="")
    safe_value = quote(value.replace("-", "--"), safe="")
    logo_part = f"&logo={quote(logo)}&logoColor=white" if logo else ""
    return (
        f'<img src="https://img.shields.io/badge/{safe_label}-{safe_value}-{color}'
        f'?style=flat-square{logo_part}" alt="{html.escape(label)}: {html.escape(value)}"/>'
    )


def link_badge(label: str, url: str, color: str, logo: str | None = None) -> str:
    return f'<a href="{html.escape(url)}">{badge(label, "Open", color, logo)}</a>'


def render_card(project: Project, meta: dict) -> str:
    language = meta.get("language") or "Code"
    stars = str(meta.get("stargazers_count") or 0)
    tag_badges = " ".join(badge("Signal", tag, "0f766e") for tag in project.tags)
    links = [
        link_badge("GitHub", project.repo_url, "1e3a8a", "github"),
    ]
    if project.live_url:
        links.append(link_badge("Live", project.live_url, "047857"))
    if project.demo_url:
        links.append(link_badge("Demo", project.demo_url, "f97316"))

    return "\n".join(
        [
            '<td width="50%" valign="top">',
            f'<h3><a href="{project.repo_url}">{html.escape(project.title)}</a></h3>',
            f"<sub>{html.escape(project.description)}</sub><br/><br/>",
            f'{badge("Language", language, "334155")} {badge("Stars", stars, "334155", "github")}<br/><br/>',
            f"{tag_badges}<br/><br/>",
            " ".join(links),
            "</td>",
        ]
    )


def render_dynamic_section(projects: list[Project]) -> tuple[str, dict]:
    metadata = {project.repo: get_repo_meta(project.repo) for project in projects}
    rows: list[str] = []
    for offset in range(0, len(projects), 2):
        chunk = projects[offset : offset + 2]
        rows.extend(["<table>", "<tr>"])
        for project in chunk:
            rows.append(render_card(project, metadata.get(project.repo, {})))
        if len(chunk) == 1:
            rows.append('<td width="50%" valign="top"></td>')
        rows.extend(["</tr>", "</table>"])
        if offset + 2 < len(projects):
            rows.append("")

    data = {
        "profile": f"https://github.com/{PROFILE_USER}",
        "projects": [
            {
                **asdict(project),
                "repo_url": project.repo_url,
                "language": metadata.get(project.repo, {}).get("language") or "Code",
                "stars": metadata.get(project.repo, {}).get("stargazers_count") or 0,
            }
            for project in projects
        ],
    }
    return "\n".join(rows).rstrip() + "\n", data


def inject_section(readme_text: str, section: str) -> str:
    start = readme_text.find(START_MARKER)
    end = readme_text.find(END_MARKER)
    replacement = f"{START_MARKER}\n{section}{END_MARKER}"
    if start != -1 and end != -1 and end > start:
        return readme_text[:start] + replacement + readme_text[end + len(END_MARKER) :]
    return readme_text.rstrip() + "\n\n" + replacement + "\n"


def years_since(value: str, now: datetime) -> int:
    created = datetime.fromisoformat(value.replace("Z", "+00:00"))
    years = now.year - created.year
    if (now.month, now.day) < (created.month, created.day):
        years -= 1
    return max(years, 0)


def github_graphql(query: str, variables: dict) -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required to render github-signal.svg")
    response = requests.post(
        "https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {token}"},
        json={"query": query, "variables": variables},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload["data"]


def render_axis_ticks(max_value: int, x: int, y: int, height: int) -> str:
    if max_value <= 0:
        labels = [0]
    else:
        step = max(1, ((max_value + 4) // 5))
        labels = list(range(0, max_value + step, step))
    parts = [
        f'<path d="M6,{height + 0.5}H0.5V0.5H6" stroke="#586069" fill="none"/>'
    ]
    for label in labels:
        tick_y = height - (label / max(labels or [1]) * height)
        parts.append(
            f'<g transform="translate(0,{tick_y:.1f})">'
            '<line stroke="#586069" x2="6"/>'
            f'<text fill="#586069" x="9" dy="0.32em" font-size="10">{label}</text>'
            "</g>"
        )
    return f'<g transform="translate({x},{y})">' + "".join(parts) + "</g>"


def render_github_signal() -> None:
    now = datetime.now(timezone.utc)
    year_start = datetime(now.year, 1, 1, tzinfo=timezone.utc)
    year_ago = now - timedelta(days=365)
    query = """
    query($login: String!, $from: DateTime!, $yearFrom: DateTime!, $to: DateTime!) {
      user(login: $login) {
        login
        name
        location
        createdAt
        repositories(privacy: PUBLIC) {
          totalCount
        }
        year: contributionsCollection(from: $yearFrom, to: $to) {
          contributionCalendar {
            totalContributions
          }
        }
        chart: contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    data = github_graphql(
        query,
        {
            "login": PROFILE_USER,
            "from": year_ago.isoformat(),
            "yearFrom": year_start.isoformat(),
            "to": now.isoformat(),
        },
    )
    user = data["user"]
    days = [
        day
        for week in user["chart"]["contributionCalendar"]["weeks"]
        for day in week["contributionDays"]
    ]
    weekly_totals: list[int] = []
    for offset in range(0, len(days), 7):
        weekly_totals.append(sum(day["contributionCount"] for day in days[offset : offset + 7]))
    if not weekly_totals:
        weekly_totals = [0]

    chart_x = 265
    chart_y = 50
    chart_w = 380
    chart_h = 110
    max_total = max(max(weekly_totals), 1)
    points = []
    for index, total in enumerate(weekly_totals):
        x = chart_x + (index / max(len(weekly_totals) - 1, 1) * chart_w)
        y = chart_y + chart_h - (total / max_total * chart_h)
        points.append((x, y))
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area = (
        f"M{points[0][0]:.1f},{chart_y + chart_h} "
        + " ".join(f"L{x:.1f},{y:.1f}" for x, y in points)
        + f" L{points[-1][0]:.1f},{chart_y + chart_h} Z"
    )
    year_total = user["year"]["contributionCalendar"]["totalContributions"]
    joined_years = years_since(user["createdAt"], now)
    location = user.get("location") or "Location not listed"
    title = f"{user['login']} ({user.get('name') or user['login']})"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="700" height="200" viewBox="0 0 700 200">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  </style>
  <rect x="1" y="1" rx="5" ry="5" width="698" height="198" fill="#ffffff" stroke="#e4e2e2"/>
  <text x="30" y="40" fill="#0366d6" font-size="22">{html.escape(title)}</text>
  <g fill="#586069" font-size="14">
    <text x="30" y="84">{year_total} Contributions in {now.year}</text>
    <text x="30" y="112">{user["repositories"]["totalCount"]} Public Repos</text>
    <text x="30" y="140">Joined GitHub {joined_years} years ago</text>
    <text x="30" y="168">{html.escape(location)}</text>
  </g>
  <path d="{area}" fill="#40c463" opacity="0.95"/>
  <polyline points="{line}" fill="none" stroke="#40c463" stroke-width="2"/>
  <path d="M{chart_x},{chart_y + chart_h + 0.5}H{chart_x + chart_w}" stroke="#586069"/>
  {render_axis_ticks(max_total, chart_x + chart_w, chart_y, chart_h)}
  <text x="{chart_x + 250}" y="190" fill="#586069" font-size="10">contributions in the last year</text>
  <text x="{chart_x}" y="178" fill="#586069" font-size="10">{year_ago.strftime("%y/%m")}</text>
  <text x="{chart_x + chart_w - 25}" y="178" fill="#586069" font-size="10">{now.strftime("%y/%m")}</text>
</svg>
"""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    GITHUB_SIGNAL_PATH.write_text(svg, encoding="utf-8")


def main() -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    render_github_signal()
    dynamic_section, data = render_dynamic_section(PROJECTS)
    PINNED_JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    PINNED_MD_PATH.write_text(dynamic_section, encoding="utf-8")

    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# Ritwij Aryan Parmar\n"
    README_PATH.write_text(inject_section(readme, dynamic_section), encoding="utf-8")
    print(f"Updated {README_PATH}")
    print(f"Wrote {GITHUB_SIGNAL_PATH}")
    print(f"Wrote {PINNED_JSON_PATH}")
    print(f"Wrote {PINNED_MD_PATH}")


if __name__ == "__main__":
    main()
