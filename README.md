# Ritwij Aryan Parmar

AI Systems Engineer specializing in LLM serving runtimes, robotics perception, and high-throughput backend infrastructure.

MS in Computer Science and Engineering, University at Buffalo. Available full-time immediately.

[LinkedIn](https://www.linkedin.com/in/ritwij-aryan-parmar-716024211/) | [Email](mailto:ritwij.aryan.parmar@gmail.com) | [GitHub](https://github.com/RitwijParmar)

## Focus

I build systems that make AI products usable under real constraints: latency, throughput, observability, deployment reliability, and evaluation quality. My strongest work sits at the intersection of LLM infrastructure, cloud-native backend services, and robotics/autonomy pipelines.

## Projects

| Project | Links | Signal |
| --- | --- | --- |
| **HelixServe** | [GitHub](https://github.com/RitwijParmar/HelixServe) · [Demo](https://storage.googleapis.com/ritwij-demo-videos-2281c357/helixserve_linkedin_final.mp4) | LLM serving runtime on GCP NVIDIA L4 with paged KV cache, continuous batching, prefix caching, CUDA Graph decode, and benchmark instrumentation. Increased throughput from 175.8 to 1,007.8 tokens/sec and reduced p95 latency from 3.28s to 0.80s. |
| **ManoVarta** | [Live](https://manovarta-runtime-ciiiagnzaq-uk.a.run.app) · [GitHub](https://github.com/RitwijParmar/ManoVarta) · [Demo](https://storage.googleapis.com/ritwij-demo-videos-2281c357/manovarta_final_demo.mp4) | Controller-led multilingual mental-health GenAI system that turns English, Hindi, and Hinglish dialogue into PHQ-9/GAD-7 item assessments with evidence extraction, structured scoring, and safety routing. |
| **SRE-Nidaan** | [Live](https://sre-nidaan-122722888597.us-east4.run.app) · [GitHub](https://github.com/RitwijParmar/SRE-Nidaan) · [Demo](https://storage.googleapis.com/ritwij-demo-videos-2281c357/sre_nidaan_demo.mp4) | SRE incident response copilot built with Next.js, FastAPI, vLLM, telemetry grounding, runbook retrieval, remediation gating, and analyst feedback loops. |

## Technical Experience

**Distributed Robotics and Networked Embedded Sensing Lab** — Research Aide, Robotics Systems Engineering

- Reduced mapping drift to under 1.2% across 500m of GPS-denied environments by building a ROS2 visual SLAM pipeline for Boston Dynamics Spot with Gaussian Splatting integration.
- Improved LiDAR and VIO fusion for low-texture subterranean navigation, reducing trajectory estimation error by 30% while sustaining 20 Hz real-time state estimation.

**Tata Elxsi** — Software Engineer Intern

- Migrated autonomous vehicle software from ROS1 to ROS2 and tuned DDS QoS behavior in CARLA, reducing inter-module latency by 40% and achieving sub-100 ms communication latency.
- Built an Extended Kalman Filter-based vehicle state estimator and safety-constrained route planner with deterministic state transitions, bounded-latency path generation, and validation hooks.

**LLMate.ai** — Backend Engineer Intern

- Built asynchronous backend services with Spring Boot and RabbitMQ for production data workflows, reducing p95 response latency by 40%.
- Deployed a GPT-3.5-based text-to-SQL workflow over 50,000 structured records and set up Docker/GitHub Actions CI/CD.

## Stack

- **Languages:** Python, C++, Java, SQL
- **AI systems:** LLM inference, model serving, vLLM, Vertex AI, QLoRA, RLHF, CUDA Graphs, prompt evaluation
- **Backend and cloud:** FastAPI, Spring Boot, Docker, GCP, Cloud Run, BigQuery, RabbitMQ, distributed systems, observability, CI/CD
- **Robotics and autonomy:** ROS2, SLAM, LiDAR/VIO sensor fusion, CARLA, state estimation

## Current Direction

I am looking for AI infrastructure, backend/product engineering, ML systems, or robotics/autonomy roles where I can own systems end to end: from low-level performance and reliability work to shipped user-facing demos.
