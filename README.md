# Ritwij Aryan Parmar

**MS in Computer Science @ University at Buffalo**  
Building reliable AI systems where model quality and systems quality are treated as one problem.

<p>
  <a href="https://github.com/RitwijParmar"><img alt="Profile views" src="https://komarev.com/ghpvc/?username=RitwijParmar&label=Profile%20views&color=0e75b6&style=flat" /></a>
  <a href="https://github.com/RitwijParmar?tab=followers"><img alt="Followers" src="https://img.shields.io/github/followers/RitwijParmar?label=Followers&style=flat" /></a>
</p>

## Contents

- [Abstract](#abstract)
- [Current Focus](#current-focus)
- [Experience Snapshot](#experience-snapshot)
- [Method](#method)
- [Systems In Public](#systems-in-public)
- [Notes](#notes)
- [Connect](#connect)

## Abstract

Most LLM prototypes fail not because the model is weak, but because the system around it is unstable: poor latency discipline, weak observability, and unclear failure boundaries.  
Current work is focused on turning promising AI ideas into measurable, production-ready systems with explicit tradeoffs.

## Current Focus

- LLM runtime engineering: scheduling, memory strategy, and inference-path optimization.
- SRE-aware AI workflows: reliability instrumentation, runbook quality, and safe automation loops.
- Cloud-native deployment paths: reproducible environments, CI/CD, and benchmark-driven iteration.

## Looking For

- Applied AI infra / ML systems engineering roles.
- High-ownership environments where reliability and product impact both matter.

## Experience Snapshot

Based on recent professional work:

- **Distributed Robotics and Networked Embedded Sensing Lab**  
  Architected 3D mapping and navigation pipelines for edge devices in GPS-denied conditions; maintained low drift and improved trajectory reliability in low-visibility runs.
- **Tata Elxsi (Autonomous Driving)**  
  Migrated monolithic components toward distributed, fault-tolerant services using C++/CUDA; reduced latency and improved positioning accuracy in state-estimation modules.
- **LLMate.ai**  
  Built asynchronous backend services and CI/CD workflows; improved response latency and deployment reliability for LLM-enabled product surfaces.

## Method

Work is driven by a simple loop:

1. Define a clear bottleneck and failure mode.
2. Instrument before optimizing.
3. Ship minimal, testable changes.
4. Re-measure and publish tradeoffs.

## Evidence Style

- Claim -> metric -> artifact link.
- Architectural choices are presented with failure modes, not just benefits.
- Demo-first communication: videos and reproducible runs over static claims.

## Systems In Public

Only pinned repositories are highlighted below, with media pulled dynamically from each project README.

<!-- START:DYNAMIC_PINNED -->
## Pinned Systems (Auto-synced)

_This section is generated from live pinned repos and each project README media._
_Last sync: 2026-04-06 22:26 UTC_

### [nervaflow-intelligence](https://github.com/RitwijParmar/nervaflow-intelligence)
- **Language:** `Python`  |  **Stars:** `2`
- **Summary:** Google Cloud-native decision engine for supply operations. Uses Vertex AI Search + conversational APIs for grounded GenAI responses, BigQuery pipelines for scenario and signal aggregation, and Cloud Run services for scalable API execution. Produces evidence-linked recommendations with quantified impact across locations, routes, and SKUs.

![nervaflow-intelligence preview](https://raw.githubusercontent.com/RitwijParmar/nervaflow-intelligence/main/docs/images/nervaflow-banner.svg)

### [SRE-Nidaan](https://github.com/RitwijParmar/SRE-Nidaan)
- **Language:** `Python`  |  **Stars:** `0`
- **Summary:** Production-style causal incident response copilot that helps teams identify what broke first, choose safer next actions, and avoid risky interventions using grounded LLM reasoning, MCP-style tool routing, and human safety gating. Built as a Face-Body-Brain architecture with QLoRA SFT, reward modeling, and RLHF for operations-ready decisions.

<video src="https://raw.githubusercontent.com/RitwijParmar/SRE-Nidaan/main/presentations/SRE_Nidaan_Demo_Recording_Voiceover_Indian.mp4" controls muted playsinline width="100%"></video>
![SRE-Nidaan preview](https://raw.githubusercontent.com/RitwijParmar/SRE-Nidaan/main/assets/readme/architecture_split_compute.png)

### [HelixServe](https://github.com/RitwijParmar/HelixServe)
- **Language:** `Python`  |  **Stars:** `0`
- **Summary:** A runtime-first LLM serving engine built to show how modern inference systems actually scale. It combines paged KV-cache allocation, continuous batching, chunked prefill, prefix caching, CUDA Graph replay, and custom Triton/CUDA kernels on a single GCP L4 GPU. Fully benchmarked and demonstrated gains in throughput, TTFT, and inter-token latency.

<video src="https://raw.githubusercontent.com/RitwijParmar/HelixServe/main/docs/assets/demo/final/helixserve_linkedin_final.mp4" controls muted playsinline width="100%"></video>
<video src="https://raw.githubusercontent.com/RitwijParmar/HelixServe/main/docs/assets/demo/helixserve_demo.mp4" controls muted playsinline width="100%"></video>
<!-- END:DYNAMIC_PINNED -->

## Notes

- Preference is for practical depth over hype.
- Strong interest in roles that combine systems engineering, AI infra, and reliability.

## Connect

- Email: **ritwij.aryan.parmar@gmail.com**
- LinkedIn: [ritwij-parmar](https://www.linkedin.com/in/ritwij-parmar/)
- GitHub: [RitwijParmar](https://github.com/RitwijParmar)
