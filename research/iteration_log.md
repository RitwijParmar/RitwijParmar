# Profile README Iteration Log

Objective: produce a profile README that reads like an operator brief, remains dynamic, and highlights only pinned projects.

## Iteration 1 (Baseline Build)

What was built:

- Wrote a research-voice profile README scaffold.
- Added resume-backed experience summary (without resume project section).
- Added dynamic markers for pinned projects.
- Implemented first version of `scripts/sync_profile_readme.py`.

Observed gaps:

1. Scan path was weak (no contents/navigation).
2. No explicit role/availability intent.
3. Dynamic section lacked timestamp (freshness was not obvious).
4. Demo media fallback was weak for non-video projects.
5. No automation to keep content current.
6. Evidence model existed but was not explicitly stated.
7. Low social proof/credibility affordances at top.

## Iteration 2 (Structure + Credibility)

Changes:

- Added table of contents.
- Added "Looking For" section.
- Added top-level lightweight badges (views/followers).
- Added "Evidence Style" section.

Result:

- Improved recruiter skim quality and narrative clarity.

## Iteration 3 (Dynamic Media Quality)

Changes:

- Extended sync parser to detect demo image fallbacks and README media links.
- Added dynamic "Last sync" timestamp.
- Kept project mentions pinned-only (`nervaflow-intelligence`, `SRE-Nidaan`, `HelixServe`).

Result:

- Media section became robust even when some pinned repos do not expose video files.

## Iteration 4 (Automation + Maintainability)

Changes:

- Added GitHub Action: `.github/workflows/sync-profile-readme.yml`.
- Scheduled daily sync + manual dispatch.
- Auto-commit of generated assets (`.generated/*`) only when content changes.
- Removed `push` trigger to prevent timestamp-driven commit loops.

Result:

- README remains fresh without manual editing.

## Remaining Loopholes / Scope for Improvement

- Add lightweight A/B variants for first 3 lines and compare profile visits.
- Add optional "selected writing/talks" once stable public links are available.
- Add project-level uptime/latency mini-badges when APIs expose public health metrics.
- Add a one-click "download resume" artifact if a public canonical resume URL is set.
- Add short GIF previews for projects that currently only expose static images.
