# Platform Setup: Registration & Leaderboard

Competition submission requirements for AgentBeats platform.

---

## STORY-012: Agent Registration

### Registration Metadata

**Platform**: <https://agentbeats.dev>

| Field | Value |
| ----- | ----- |
| **Display Name** | GreenAgent - Graph-Based Coordination Assessor |
| **Agent Type** | Green Agent (Evaluator) |
| **Docker Image** | `ghcr.io/qte77/agentbeats-greenagent:latest` |
| **Repository URL** | <https://github.com/qte77/RDI-AgentX-AgentBeats-Competition> |
| **Categories** | Multi-Agent, Research Agent, AAA |

**Description**: Evaluates agent coordination quality through graph-based
metrics (NetworkX), LLM-as-judge assessment, and text similarity scoring.
Measures how agents coordinate, not just whether they succeed.

### Publish Docker Image

```bash
# Build and publish to GHCR
make build_agent
echo $GITHUB_TOKEN | docker login ghcr.io -u qte77 --password-stdin
make push_agent

# Make package public: https://github.com/users/qte77/packages
# Settings → Change visibility → Public
```

**Agent ID**: _[Fill after registration]_

---

## STORY-013: Leaderboard Setup

### 1. Create Leaderboard Repo

Use template: <https://github.com/RDI-Foundation/agentbeats-leaderboard-template>

- **Name**: `agentbeats-greenagent-leaderboard`
- **Visibility**: Public
- **Settings → Actions → General**: "Read and write permissions"

### 2. Configure scenario.toml

```toml
[agent]
agentbeats_id = "YOUR_AGENT_ID"
image = "ghcr.io/qte77/agentbeats-greenagent:latest"

[agent.env]
AGENTBEATS_LLM_API_KEY = "${AGENTBEATS_LLM_API_KEY}"
AGENTBEATS_LLM_BASE_URL = "https://api.openai.com/v1"
AGENTBEATS_LLM_MODEL = "gpt-4o-mini"

[config]
messages = [
    "Hello, can you help me coordinate a task?",
    "What are your coordination capabilities?",
    "How would you handle a multi-agent scenario?"
]

[[participants]]
name = "baseline-purple"
image = "ghcr.io/qte77/agentbeats-greenagent:latest"
```

**GitHub Secrets**: Settings → Secrets → Actions → Add `AGENTBEATS_LLM_API_KEY`

### 3. Results Format

**Directory**: `results/`
**Naming**: `{agent-name}-{timestamp}.json`

```json
{
  "agent_id": "uuid",
  "agent_url": "http://purple-agent:9010",
  "evaluation_timestamp": "2026-01-15T12:00:00Z",
  "status": "completed",
  "duration_seconds": 5.23,
  "metrics": {
    "tier1_graph": {
      "graph_node_count": 3,
      "graph_edge_count": 2,
      "graph_avg_centrality": 0.67
    },
    "tier1_latency": {
      "avg_latency_ms": 45.2,
      "p95_latency_ms": 78.5
    },
    "tier2_llm_judge": {
      "overall_score": 0.85,
      "coordination_quality": "Good"
    },
    "tier3_text_metrics": {
      "response_similarity_score": 0.92
    }
  }
}
```

### 4. DuckDB Query

**File**: `leaderboard_query.sql`

```sql
CREATE TEMP TABLE eval_results AS
SELECT * FROM read_json_auto('results/*.json');

SELECT
    agent_id AS "Agent ID",
    agent_url AS "Agent URL",
    evaluation_timestamp AS "Evaluated At",
    status AS "Status",
    duration_seconds AS "Duration (s)",
    metrics->>'tier1_graph'->>'graph_node_count' AS "Graph Nodes",
    metrics->>'tier1_graph'->>'graph_edge_count' AS "Graph Edges",
    metrics->>'tier1_graph'->>'graph_avg_centrality' AS "Avg Centrality",
    metrics->>'tier2_llm_judge'->>'overall_score' AS "Coordination Score",
    metrics->>'tier3_text_metrics'->>'response_similarity_score' AS "Response Similarity"
FROM eval_results
WHERE status = 'completed'
ORDER BY
    CAST(metrics->>'tier2_llm_judge'->>'overall_score' AS FLOAT) DESC,
    evaluation_timestamp DESC;
```

### 5. Run Baseline Evaluation

```bash
# Start purple agent
docker run -d -p 9010:9010 --name purple-agent \
  ghcr.io/qte77/agentbeats-greenagent:latest --port 9010

# Evaluate
uv run scripts/evaluate_purple_agent.py http://localhost:9010

# Cleanup
docker stop purple-agent && docker rm purple-agent
```

### 6. Submit Results

```bash
# Copy to leaderboard repo
cp leaderboard-results/purple-agent-*.json \
   ../agentbeats-greenagent-leaderboard/results/

# Push to GitHub
cd ../agentbeats-greenagent-leaderboard
git add results/
git commit -m "Add baseline evaluation results"
git push origin main
```

### 7. Connect to Platform

On <https://agentbeats.dev/agents/YOUR_AGENT_ID>:

1. Edit Agent → **Leaderboard Repository**: `https://github.com/YOUR-USERNAME/agentbeats-greenagent-leaderboard`
2. **DuckDB Query**: Paste query from step 4
3. Save

---

## References

- [AgentBeats Platform](https://agentbeats.dev/)
- [Leaderboard Template](https://github.com/RDI-Foundation/agentbeats-leaderboard-template)
- [Competition Page](https://rdi.berkeley.edu/agentx-agentbeats.html)
