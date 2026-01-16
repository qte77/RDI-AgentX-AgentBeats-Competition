# End-to-End Workflow

Complete system execution: GreenAgent evaluates Purple Agent and produces results.

## Prerequisites

- Docker OR uv + Python 3.13+
- Ports 9009 (GreenAgent) and 9010 (Purple Agent) available

---

## Option 1: Local Development (Fastest)

```bash
# Terminal 1: Start GreenAgent
make run_agent

# Terminal 2: Start Purple Agent
cd examples/purple-agent
uv sync
uv run python -m purpleagent.server --port 9010

# Terminal 3: Run Evaluation
uv run scripts/evaluate_purple_agent.py http://localhost:9010
```

**Results**: `leaderboard-results/purple-agent-*.json`

---

## Option 2: Docker (Production-Like)

```bash
# Terminal 1: Start GreenAgent
docker run -p 9009:9009 ghcr.io/qte77/agentbeats-greenagent:latest

# Terminal 2: Start Purple Agent
docker run -p 9010:9010 \
  ghcr.io/qte77/agentbeats-greenagent:latest \
  --port 9010

# Terminal 3: Run Evaluation
uv run scripts/evaluate_purple_agent.py http://localhost:9010
```

---

## Verification

```bash
# Check GreenAgent is running
curl http://localhost:9009/.well-known/agent.json

# Check Purple Agent is running
curl http://localhost:9010/.well-known/agent-card.json

# View evaluation results
cat leaderboard-results/purple-agent-*.json | jq
```

---

## Expected Results

Evaluation produces JSON with three tiers:

```json
{
  "metrics": {
    "graph_node_count": 3,
    "graph_edge_count": 2,
    "graph_avg_centrality": 0.67,
    "coordination_quality_score": 0.85,
    "response_similarity_score": 0.92
  }
}
```

---

## Cleanup

```bash
# Stop local processes: Ctrl+C in each terminal

# Stop Docker containers
docker stop $(docker ps -q --filter ancestor=ghcr.io/qte77/agentbeats-greenagent:latest)
```

---

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| Port already in use | Change port: `--port 9011` |
| Connection refused | Ensure agent is running: `curl` verification |
| Evaluation fails | Check agent logs for errors |

---

## Next Steps

- **Reproducibility**: Run evaluation 3+ times, compare results
- **Leaderboard**: Push results to GitHub leaderboard repo
- **Documentation**: See `docs/ralph-results/PLATFORM_SETUP.md` for submission
