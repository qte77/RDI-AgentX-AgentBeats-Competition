---
title: User Story - AgentBeats GreenAgent (Assessor)
version: 2.0
applies-to: Agents and humans
purpose: Product vision, value proposition, and success metrics
---

## PRD References

- **Original Implementation**: [archive/PRD-v1.md](archive/PRD-v1.md) -
  Initial green agent evaluation system
- **Benchmarking Enhancements**: [PRD.md](PRD.md) - A2A protocol fix, real
  LLM integration, latency metrics, extensibility

## As a benchmark creator

**I want to** evaluate multi-agent coordination quality through runtime graph analysis

**So that** I can measure **how** agents collaborate, not just whether they succeed

## Value Proposition

No existing AgentBeats benchmark analyzes coordination patterns through graph structure.

## Acceptance

### Core Functionality (Original)

- Purple agents submit to evaluation via A2A protocol →
  *[archive/PRD-v1.md](archive/PRD-v1.md)* (STORY-005, STORY-006) +
  *[PRD.md](PRD.md)* (STORY-001 to 003 - protocol fix)
- GreenAgent captures interaction traces →
  *[archive/PRD-v1.md](archive/PRD-v1.md)* (STORY-002-IMPL)
- Graph metrics reveal coordination quality (centrality, efficiency,
  bottlenecks) → *[archive/PRD-v1.md](archive/PRD-v1.md)* (STORY-003-IMPL)
- LLM-as-judge provides qualitative assessment →
  *[archive/PRD-v1.md](archive/PRD-v1.md)* (STORY-004-IMPL) +
  *[PRD.md](PRD.md)* (STORY-004 to 008 - real LLM)
- Results returned as structured A2A artifacts →
  *[archive/PRD-v1.md](archive/PRD-v1.md)* (STORY-007-IMPL)

### Benchmarking Enhancements (v2.0)

- **Real A2A Communication**: Messenger uses A2A SDK ClientFactory (not
  custom REST mock) → *[PRD.md](PRD.md)* (STORY-001 to 003)
- **Real LLM Evaluation**: LLM Judge calls actual LLM API with fallback to
  rule-based → *[PRD.md](PRD.md)* (STORY-004 to 008)
- **Performance Metrics**: Latency evaluator tracks response times (avg,
  p50, p95, p99) → *[PRD.md](PRD.md)* (STORY-009)
- **Extensibility**: Documentation enables adding custom evaluators without
  modifying core code → *[PRD.md](PRD.md)* (STORY-010)

## Success Metrics

1. A2A protocol compliance (agent card accessible)
2. Trace capture working (graph buildable from interactions)
3. Dual evaluation (graph metrics + LLM judge)
4. Local testability (uv run + curl verification)
5. Docker deployment ready
