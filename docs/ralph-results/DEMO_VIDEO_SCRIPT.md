# Demo Video Script

**Duration**: 3 minutes maximum
**Purpose**: Demonstrate graph-based coordination assessment

## Script (3 sections)

### 1. Introduction & Startup (45 seconds)

**Narration**:
> "GraphJudge evaluates HOW agents coordinate, not just whether they succeed.
> We use graph-based structural analysis as the primary metric, complemented by
> LLM-as-judge assessment."

**Commands**:

```bash
# Start GraphJudge server
make run_agent

# Verify A2A endpoint
curl http://localhost:9009/.well-known/agent.json
```

**Show**: Agent card JSON with evaluation capabilities

### 2. Evaluation Flow (90 seconds)

**Narration**:
> "Evaluation captures interaction traces and transforms them into directed
> graphs. We extract structural metrics—centrality, density, efficiency—that
> quantify coordination quality. Three evaluation tiers: Tier 1 includes graph
> metrics and latency; Tier 2 provides LLM-based qualitative assessment; Tier
> 3 measures consistency."

**Commands**:

```bash
# Evaluate purple agent
uv run scripts/evaluate_purple_agent.py http://localhost:9010
```

**Show**:

1. Trace capture in progress
2. Graph construction from traces
3. Metrics calculation:
   - **Tier 1 Graph**: node count, edge count, centrality (primary focus)
   - **Tier 1 Latency**: avg, p50, p95, p99
   - **Tier 2 LLM Judge**: coordination quality score
   - **Tier 3 Text**: response similarity

**Visual**: Communication graph diagram being built

### 3. Results & Integration (45 seconds)

**Narration**:
> "Graph metrics reveal coordination patterns. The baseline purple agent shows
> minimal interaction: 2 nodes, 1 edge. We validated reproducibility across
> multiple runs. Results are published to the AgentBeats leaderboard for
> transparent comparison."

**Commands**:

```bash
# Show results
cat results.json | jq '.tier1_graph'

# Show reproducibility validation
ls docs/ralph-results/reproducibility-results/

# Agent registry and leaderboard
# https://agentbeats.dev/qte77/graphjudge
# https://github.com/qte77/RDI-AgentX-AgentBeats-Competition-Leaderboard
```

**Show**:

- Graph metrics interpretation
- Reproducibility results directory with multiple run files
- Agent registry page at agentbeats.dev/qte77/graphjudge
- Leaderboard repository displaying GraphJudge results

## Recording Setup

**Terminal**: Clear font (14-16pt), high contrast, 1920x1080

**Commands to test**:

```bash
make run_agent
curl http://localhost:9009/.well-known/agent.json
uv run scripts/evaluate_purple_agent.py http://localhost:9010
ls docs/ralph-results/reproducibility-results/
```

**Emphasis**: "graph-based", "structural metrics", "coordination quality"

## Checklist

- [ ] All commands tested
- [ ] Graph visualization ready
- [ ] Reproducibility results shown
- [ ] Leaderboard URL displayed
- [ ] Video < 3 minutes
- [ ] Graph metrics emphasized
- [ ] Uploaded and link public
