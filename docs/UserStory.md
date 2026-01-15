---
title: User Story - AgentBeats GreenAgent (Assessor)
version: 1.0
applies-to: all-agents
purpose: Product vision, value proposition, and success metrics
---

## As a benchmark creator

**I want to** evaluate multi-agent coordination quality through runtime graph analysis

**So that** I can measure **how** agents collaborate, not just whether they succeed

## Value Proposition

No existing AgentBeats benchmark analyzes coordination patterns through graph structure.

## Acceptance

- Purple agents submit to evaluation via A2A protocol
- GreenAgent captures interaction traces
- Graph metrics reveal coordination quality (centrality, efficiency, bottlenecks)
- LLM-as-judge provides qualitative assessment
- Results returned as structured A2A artifacts

## Success Metrics

1. A2A protocol compliance (agent card accessible)
2. Trace capture working (graph buildable from interactions)
3. Dual evaluation (graph metrics + LLM judge)
4. Local testability (uv run + curl verification)
5. Docker deployment ready
