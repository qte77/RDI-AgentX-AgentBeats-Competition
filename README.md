# AgentBeats GreenAgent - Graph-Based Coordination Evaluator

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
