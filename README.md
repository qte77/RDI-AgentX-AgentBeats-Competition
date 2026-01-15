---
title: Graph-Based Assessor - AgentBeats GreenAgent
version: 1.0
applies-to: humans
purpose: Project overview and quick start guide
---

> Measure how, not just whether

A GreenAgent for [AgentBeats competition](https://rdi.berkeley.edu/agentx-agentbeats.html)
that evaluates **how agents coordinate**, not just whether they succeed.

## Novel Value

Graph-based runtime coordination analysis - measuring collaboration quality
through NetworkX metrics and LLM-as-judge evaluation.

## Architecture

```text
Purple Agents → A2A Request → GreenAgent
                                ├─ Trace Capture
                                ├─ Graph Metrics (Tier 1)
                                ├─ LLM Judge (Tier 2)
                                └─ Text Metrics (Tier 3, plugin, optional)
                                     ↓
                              A2A Artifact {scores}
```

## Quick Start

```bash
# Install dependencies
uv sync

# Start GreenAgent server
uv run src/agentbeats/server.py

# Test (new terminal)
curl localhost:9009/.well-known/agent.json
```

## Development with Ralph Loop

```bash
# Generate task tracking from PRD
make ralph_init

# Run autonomous development
make ralph

# Check progress
make ralph_status
```

## Files

- `docs/UserStory.md` - User story and value proposition
- `docs/PRD.md` - Product requirements (17 stories)
- `docs/RalphUsage.md` - Ralph loop commands
- `src/agentbeats/` - A2A implementation

## Evaluation Tiers

| Tier | Type      | Description                                   |
| ---- | --------- | --------------------------------------------- |
| 1    | Graph     | NetworkX metrics (centrality, efficiency)     |
| 2    | LLM-Judge | Coordination quality assessment               |
| 3    | Text      | Similarity metrics (plugin for PeerRead)      |

## Roadmap

- ✅ Phase 1: A2A + Graph + Basic eval (current)
- 🔜 Phase 2: ART training on traces (outlook)
- 🔮 Phase 3: Self-evolving GreenAgent (outlook, e.g., [DGM](https://arxiv.org/abs/2410.04444))

## Competition Tracks

- Research Agent
- Multi-Agent
- AAA (Agentified Agent Assessment)

## Submission

### Abstract

GreenAgent is a novel evaluation framework that measures **how agents coordinate**, not just whether they succeed. The system combines graph-based structural analysis (NetworkX metrics), LLM-as-judge assessment, and text similarity scoring to provide comprehensive multi-tier evaluation of agent coordination quality. Through A2A-compliant trace capture and directed graph analysis, GreenAgent reveals coordination patterns, bottlenecks, and collaboration effectiveness. We demonstrate perfect reproducibility (0% variance) across metrics in independent evaluation runs, enabling fair and consistent assessment of multi-agent systems.

Full abstract: [docs/ABSTRACT.md](docs/ABSTRACT.md)

### Demo Video

**Video URL**: [To be added - demo video showing agent startup, evaluation flow, and results interpretation]

The demo video (max 3 minutes) demonstrates:
- GreenAgent server startup and A2A endpoint verification
- Purple agent evaluation flow with trace capture
- Multi-tier evaluation results (graph metrics, LLM judge, text similarity)
- Result interpretation and leaderboard integration
