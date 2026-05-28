#!/usr/bin/env python3
"""Render the dynamic project-card section for the GitHub profile README."""

from __future__ import annotations

import html
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
GENERATED_DIR = ROOT / ".generated"
PINNED_JSON_PATH = GENERATED_DIR / "pinned_projects.json"
PINNED_MD_PATH = GENERATED_DIR / "pinned_projects.md"

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
        tags=["LLM Serving", "CUDA Graphs", "GCP L4"],
        demo_url="https://storage.googleapis.com/ritwij-demo-videos-2281c357/helixserve_linkedin_final.mp4",
    ),
    Project(
        title="ManoVarta",
        repo="ManoVarta",
        description=(
            "Controller-led multilingual mental-health GenAI system for English, Hindi, and "
            "Hinglish PHQ-9/GAD-7 item-level assessment with evidence extraction and safety routing."
        ),
        tags=["GenAI Runtime", "Cloud Run", "Safety"],
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
        tags=["SRE Copilot", "vLLM", "FastAPI"],
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
        tags=["Vertex AI", "BigQuery", "Operations"],
        demo_url=(
            "https://raw.githubusercontent.com/RitwijParmar/nervaflow-intelligence/main/"
            "artifacts/video/nervaflow_demo_linkedin_1080p.mp4"
        ),
    ),
]


def get_repo_meta(repo: str) -> dict:
    url = f"https://api.github.com/repos/{PROFILE_USER}/{repo}"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}


def badge(label: str, value: str, color: str, logo: str | None = None) -> str:
    safe_label = quote(label.replace("-", "--"))
    safe_value = quote(value.replace("-", "--"))
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
    tag_badges = " ".join(badge("Stack", tag, "0f766e") for tag in project.tags)
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


def main() -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    dynamic_section, data = render_dynamic_section(PROJECTS)
    PINNED_JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    PINNED_MD_PATH.write_text(dynamic_section, encoding="utf-8")

    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# Ritwij Aryan Parmar\n"
    README_PATH.write_text(inject_section(readme, dynamic_section), encoding="utf-8")
    print(f"Updated {README_PATH}")
    print(f"Wrote {PINNED_JSON_PATH}")
    print(f"Wrote {PINNED_MD_PATH}")


if __name__ == "__main__":
    main()
