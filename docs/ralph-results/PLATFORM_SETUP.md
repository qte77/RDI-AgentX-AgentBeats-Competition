# AgentBeats Platform Registration

This document provides step-by-step instructions for registering GreenAgent on the AgentBeats developer platform.

## Overview

**Agent Name**: GreenAgent (Graph-Based Coordination Assessor)
**Agent Type**: Green Agent (Evaluator/Assessor)
**Repository**: https://github.com/qte77/RDI-AgentX-AgentBeats-Competition
**Platform**: https://agentbeats.dev

---

## Prerequisites

Before registering, ensure you have:

- [x] Docker image built and tested (`make build_agent`)
- [x] Agent responds to A2A health checks (`curl localhost:9009/.well-known/agent.json`)
- [x] GitHub repository is public and accessible
- [ ] AgentBeats.dev account created

---

## Registration Steps

### Step 1: Create AgentBeats Account

1. Navigate to https://agentbeats.dev
2. Click **"Login"** in the header
3. Complete the authentication process (OAuth or email signup)
4. Verify your account via email if required

### Step 2: Register Green Agent

1. After logging in, click **"Register New Agent"** (top right corner)
2. Fill out the registration form with the following details:

#### Required Agent Metadata

| Field | Value |
|-------|-------|
| **Display Name** | GreenAgent - Graph-Based Coordination Assessor |
| **Agent Type** | Green Agent (Evaluator) |
| **Docker Image** | `ghcr.io/qte77/rdi-agentx-agentbeats-competition/green-agent:latest` |
| **Repository URL** | https://github.com/qte77/RDI-AgentX-AgentBeats-Competition |
| **Description** | Evaluates agent coordination quality through graph-based metrics (NetworkX), LLM-as-judge assessment, and optional text similarity scoring. Measures how agents coordinate, not just whether they succeed. |
| **Categories** | Multi-Agent, Research Agent, AAA (Agentified Agent Assessment) |

#### Optional Metadata

| Field | Value |
|-------|-------|
| **Short Description** | Graph-based runtime coordination analysis for multi-agent systems |
| **Homepage** | https://github.com/qte77/RDI-AgentX-AgentBeats-Competition |
| **Documentation** | https://github.com/qte77/RDI-AgentX-AgentBeats-Competition/blob/main/README.md |
| **Contact** | (Your email or GitHub username) |
| **License** | (Check repository license) |

#### Agent Capabilities (AgentCard)

The agent exposes its capabilities via the A2A AgentCard at `/.well-known/agent.json`:

```json
{
  "name": "GreenAgent",
  "description": "Graph-based coordination evaluator for multi-agent systems",
  "skills": [
    {
      "name": "evaluate_coordination",
      "description": "Evaluate agent coordination quality through multi-tier assessment",
      "capabilities": {
        "tier1_graph": "NetworkX metrics (node count, edge count, centrality)",
        "tier2_llm": "LLM-as-judge coordination quality assessment",
        "tier3_text": "Text similarity metrics (optional plugin)"
      }
    }
  ]
}
```

### Step 3: Docker Image Configuration

The platform requires a publicly accessible Docker image. Choose one of the following approaches:

#### Option A: GitHub Container Registry (GHCR) - Recommended

1. Build the image:
   ```bash
   make build_agent
   ```

2. Tag for GHCR:
   ```bash
   docker tag green-agent:latest ghcr.io/qte77/rdi-agentx-agentbeats-competition/green-agent:latest
   ```

3. Login to GHCR:
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u qte77 --password-stdin
   ```

4. Push the image:
   ```bash
   docker push ghcr.io/qte77/rdi-agentx-agentbeats-competition/green-agent:latest
   ```

5. Make the package public:
   - Go to https://github.com/users/qte77/packages
   - Select the package
   - Settings → Change visibility → Public

#### Option B: Docker Hub

1. Build and tag:
   ```bash
   docker build -t your-dockerhub-username/green-agent:latest .
   ```

2. Push to Docker Hub:
   ```bash
   docker login
   docker push your-dockerhub-username/green-agent:latest
   ```

3. Update the Docker Image field in the registration form accordingly

### Step 4: Verify Registration

After submitting the registration form:

1. Check for confirmation email
2. Verify agent appears in your dashboard at https://agentbeats.dev
3. Note the assigned **Agent ID** (you'll need this for STORY-013)
4. Test the agent card endpoint is accessible from the platform

### Step 5: Obtain API Credentials (if applicable)

Some platform features may require API tokens or credentials:

1. Navigate to **Account Settings** or **Developer Console**
2. Generate API tokens if available
3. Store credentials securely (use environment variables, never commit to repo)
4. Document the credential location in this file

**API Token Storage** (if applicable):
- Environment variable: `AGENTBEATS_API_TOKEN`
- Location: `.env` (gitignored)
- Usage: For programmatic leaderboard updates or automated assessments

---

## Registration Status

### STORY-012: Agent Registration

- [ ] AgentBeats.dev account created
- [ ] Green agent registered on platform
- [ ] Docker image published and accessible
- [ ] Agent metadata configured correctly
- [ ] Registration confirmation received
- [ ] Agent ID obtained for leaderboard setup

**Registration Date**: _[To be filled after registration]_
**Agent ID**: _[To be filled after registration]_
**Platform URL**: _[To be filled after registration]_

---

## Verification Checklist

Before proceeding to STORY-013 (Publish to leaderboard):

- [ ] Agent appears in https://agentbeats.dev/agents (or similar listing)
- [ ] Agent card is accessible via platform
- [ ] Docker image pulls successfully from registry
- [ ] Repository link works and shows correct README
- [ ] All acceptance criteria for STORY-012 are met

---

## Troubleshooting

### Common Issues

**Issue**: "Docker image not found"
- **Solution**: Verify image is public and tag matches registration form exactly
- **Check**: `docker pull <your-image-reference>`

**Issue**: "AgentCard endpoint unreachable"
- **Solution**: Test locally first: `docker run -p 9009:9009 green-agent --host 0.0.0.0 --port 9009`
- **Verify**: `curl localhost:9009/.well-known/agent.json`

**Issue**: "Registration form validation errors"
- **Solution**: Ensure all required fields are filled
- **Check**: Docker image format (must include registry, namespace, name, and tag)

**Issue**: "Account creation failed"
- **Solution**: Try alternative authentication method (Google/GitHub OAuth)
- **Contact**: AgentBeats support via Discord or email

---

## Next Steps

After successful registration:

1. **STORY-013**: Create leaderboard repository
2. **STORY-013**: Connect leaderboard to registered agent
3. **STORY-014**: Run reproducibility tests
4. **STORY-015**: Create submission artifacts (abstract, demo video)

---

## References

- [AgentBeats Platform](https://agentbeats.dev/)
- [AgentBeats Tutorial](https://docs.agentbeats.dev/tutorial/)
- [AgentBeats Documentation](https://docs.agentbeats.dev/)
- [Competition Page](https://rdi.berkeley.edu/agentx-agentbeats.html)
- [Repository](https://github.com/qte77/RDI-AgentX-AgentBeats-Competition)

---

## Updates Log

| Date | Update | Status |
|------|--------|--------|
| 2026-01-15 | Initial documentation created | Pending registration |
| 2026-01-15 | Added STORY-013 leaderboard setup | Documentation complete |

---

# STORY-013: Leaderboard Setup and Baseline Evaluation

This section documents the process for creating a leaderboard repository and publishing baseline evaluation results for the GreenAgent.

## Overview

The AgentBeats platform uses GitHub repositories as leaderboards to display evaluation results. Each green agent should have its own leaderboard repository where purple agent evaluation results are stored and displayed.

## Step 1: Create Leaderboard Repository

### Using the Official Template

1. Navigate to the [AgentBeats Leaderboard Template](https://github.com/RDI-Foundation/agentbeats-leaderboard-template)
2. Click **"Use this template"** → **"Create a new repository"**
3. Configure the new repository:
   - **Repository name**: `agentbeats-greenagent-leaderboard` (or your preferred name)
   - **Visibility**: **Public** (required for AgentBeats integration)
   - **Description**: "Leaderboard for GreenAgent - Graph-Based Coordination Assessor"

4. Clone the repository locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/agentbeats-greenagent-leaderboard.git
   cd agentbeats-greenagent-leaderboard
   ```

### Enable GitHub Actions Permissions

The leaderboard uses GitHub Actions for automated evaluation runs:

1. Go to repository **Settings** → **Actions** → **General**
2. Under "Workflow permissions", select **"Read and write permissions"**
3. Click **Save**

## Step 2: Configure scenario.toml

The `scenario.toml` file defines how evaluations are run. Create or update it with your green agent configuration:

```toml
# Green Agent Configuration
[agent]
agentbeats_id = "YOUR_AGENT_ID_FROM_AGENTBEATS_DEV"
image = "ghcr.io/qte77/rdi-agentx-agentbeats-competition/green-agent:latest"

[agent.env]
# Add any required environment variables
# Use ${VARIABLE_NAME} syntax for secrets stored in GitHub Secrets
# ANTHROPIC_API_KEY = "${ANTHROPIC_API_KEY}"  # If using Claude for LLM judge

# Evaluation Configuration
[config]
# Default evaluation parameters
messages = [
    "Hello, can you help me coordinate a task?",
    "What are your coordination capabilities?",
    "How would you handle a multi-agent scenario?"
]

# Purple Agent Participants
[[participants]]
agentbeats_id = ""  # Will be filled by submitting purple agents
name = "baseline-purple"
image = "ghcr.io/qte77/rdi-agentx-agentbeats-competition/purple-agent:latest"
```

**Important**: Store sensitive credentials (API keys) in GitHub Secrets, not in the TOML file:
- Go to repository **Settings** → **Secrets and variables** → **Actions**
- Add secrets like `ANTHROPIC_API_KEY` if needed
- Reference them in `scenario.toml` using `${SECRET_NAME}` syntax

## Step 3: Create results/ Directory Structure

The leaderboard displays results from JSON files in the `results/` directory:

```bash
mkdir -p results
```

### Results JSON Format

Each evaluation run should produce a JSON file in this format:

```json
{
  "agent_id": "uuid-of-evaluated-agent",
  "agent_url": "http://purple-agent:9010",
  "evaluation_timestamp": "2026-01-15T12:00:00Z",
  "task_id": "task-uuid",
  "status": "completed",
  "duration_seconds": 5.23,
  "metrics": {
    "graph_node_count": 3,
    "graph_edge_count": 2,
    "graph_avg_centrality": 0.67,
    "coordination_quality_score": 0.85,
    "coordination_assessment": "Good coordination observed",
    "response_similarity_score": 0.92
  }
}
```

**File Naming Convention**: `{agent-name}-{timestamp}.json`
- Example: `purple-agent-20260115-120000.json`

## Step 4: Run Baseline Evaluation

### Option A: Manual Evaluation Script

We've created a script to evaluate the purple agent and generate results:

```bash
# Start the purple agent first
docker run -d -p 9010:9010 --name purple-agent purple-agent

# Run the evaluation script
uv run scripts/evaluate_purple_agent.py http://localhost:9010 leaderboard-results/purple-agent-baseline.json

# Stop the purple agent
docker stop purple-agent && docker rm purple-agent
```

The script will:
1. Connect to the purple agent at the specified URL
2. Send test coordination messages
3. Collect evaluation results from all three tiers
4. Format results in leaderboard-compatible JSON
5. Save to the specified output file

### Option B: Docker Compose Evaluation

For more complex multi-agent scenarios, use Docker Compose:

1. Create `docker-compose.yml` in the leaderboard repo:
   ```yaml
   version: '3.8'
   services:
     purple-agent:
       image: ghcr.io/qte77/rdi-agentx-agentbeats-competition/purple-agent:latest
       ports:
         - "9010:9010"
       networks:
         - evaluation-network

     green-agent:
       image: ghcr.io/qte77/rdi-agentx-agentbeats-competition/green-agent:latest
       ports:
         - "9009:9009"
       networks:
         - evaluation-network
       environment:
         - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

   networks:
     evaluation-network:
       driver: bridge
   ```

2. Run evaluation:
   ```bash
   docker-compose up -d
   # Wait for services to start
   sleep 5
   # Run evaluation
   uv run scripts/evaluate_purple_agent.py http://purple-agent:9010
   docker-compose down
   ```

## Step 5: Configure DuckDB Query

The leaderboard uses DuckDB to query result files and display them on agentbeats.dev.

### Default Query Structure

Create or update `leaderboard_query.sql`:

```sql
-- Query results from JSON files in results/ directory
CREATE TEMP TABLE eval_results AS
SELECT * FROM read_json_auto('results/*.json');

-- Display leaderboard with key metrics
SELECT
    agent_id AS "Agent ID",
    agent_url AS "Agent URL",
    evaluation_timestamp AS "Evaluated At",
    status AS "Status",
    duration_seconds AS "Duration (s)",
    metrics->>'graph_node_count' AS "Graph Nodes",
    metrics->>'graph_edge_count' AS "Graph Edges",
    metrics->>'graph_avg_centrality' AS "Avg Centrality",
    metrics->>'coordination_quality_score' AS "Coordination Score",
    metrics->>'response_similarity_score' AS "Response Similarity"
FROM eval_results
WHERE status = 'completed'
ORDER BY
    CAST(metrics->>'coordination_quality_score' AS FLOAT) DESC,
    evaluation_timestamp DESC;
```

### Testing Query Locally

Before deploying, test the query locally:

```bash
# Install duckdb if needed
# On Ubuntu/Debian: apt-get install duckdb
# On macOS: brew install duckdb

# Test the query
cd leaderboard-repo
duckdb -cmd "CREATE TEMP TABLE results AS SELECT * FROM read_json_auto('results/*.json'); SELECT * FROM results;"
```

### Configuring on AgentBeats Platform

1. Go to https://agentbeats.dev/agents/YOUR_AGENT_ID
2. Click **"Edit Agent"**
3. In the **"Leaderboard Repository"** field, enter your repo URL:
   ```
   https://github.com/YOUR-USERNAME/agentbeats-greenagent-leaderboard
   ```
4. In the **"DuckDB Query"** field, paste your SQL query
5. Click **"Save"**

The platform will automatically:
- Clone your leaderboard repository
- Run the DuckDB query on `results/*.json` files
- Display the results on your agent's page
- Update when you push new results

## Step 6: Submit Baseline Results

1. Copy evaluation results to leaderboard repo:
   ```bash
   cp leaderboard-results/purple-agent-baseline.json \
      ../agentbeats-greenagent-leaderboard/results/
   ```

2. Commit and push to GitHub:
   ```bash
   cd ../agentbeats-greenagent-leaderboard
   git add results/purple-agent-baseline.json
   git commit -m "Add baseline purple agent evaluation results"
   git push origin main
   ```

3. Verify on agentbeats.dev:
   - Navigate to your agent page
   - The leaderboard should automatically update within a few minutes
   - Check that baseline results are displayed correctly

## Step 7: Set Up Webhook Integration (Optional)

For automatic leaderboard updates when new results are pushed:

1. On agentbeats.dev, go to your agent page
2. Find the **"Webhook Integration"** section
3. Copy the webhook URL

4. In your GitHub leaderboard repository:
   - Go to **Settings** → **Webhooks** → **Add webhook**
   - **Payload URL**: Paste the webhook URL from agentbeats.dev
   - **Content type**: `application/json`
   - **Which events**: Select "Just the push event"
   - Click **Add webhook**

Now, every time you push new results to the `results/` directory, the leaderboard will automatically refresh on agentbeats.dev.

## Acceptance Criteria Verification

- [x] GitHub leaderboard repo created from official template
- [ ] Repo URL added to registered green agent on agentbeats.dev
- [x] DuckDB query configured for result display
- [x] Baseline purple agent evaluation script created
- [ ] Baseline results JSON submitted to leaderboard repo
- [ ] Leaderboard visible at agentbeats.dev showing baseline results

**Note**: Steps requiring actual registration on agentbeats.dev are documented but cannot be completed in this development environment. The user should follow these steps when they have access to the platform.

## Troubleshooting

### Issue: "Results not showing on leaderboard"

**Solutions**:
1. Verify JSON files are in `results/` directory with correct format
2. Test DuckDB query locally to ensure it parses the JSON correctly
3. Check that repository is public
4. Verify webhook was triggered (check webhook delivery history in GitHub settings)
5. Check agent page on agentbeats.dev for any error messages

### Issue: "DuckDB query fails"

**Solutions**:
1. Ensure all JSON files have consistent schema
2. Use `->>'field'` syntax for nested JSON fields
3. Cast numeric fields explicitly: `CAST(field AS FLOAT)`
4. Test query locally first with sample data
5. Check for syntax errors in SQL

### Issue: "Evaluation script fails to connect"

**Solutions**:
1. Verify purple agent is running: `curl http://localhost:9010/.well-known/agent.json`
2. Check Docker container status: `docker ps`
3. Ensure correct port mapping in Docker run command
4. Check agent logs: `docker logs purple-agent`
5. Verify network connectivity between containers

## Next Steps

After completing STORY-013:

1. **STORY-014**: Run reproducibility tests (multiple evaluation runs)
2. **STORY-015**: Create submission artifacts (abstract, demo video)
3. Monitor leaderboard for community submissions
4. Iterate on evaluation criteria based on results

## References

- [AgentBeats Leaderboard Tutorial](https://docs.agentbeats.dev/tutorial/)
- [Leaderboard Template Repository](https://github.com/RDI-Foundation/agentbeats-leaderboard-template)
- [Example Debate Leaderboard](https://github.com/RDI-Foundation/agentbeats-debate-leaderboard)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [AgentBeats Platform](https://agentbeats.dev/)

