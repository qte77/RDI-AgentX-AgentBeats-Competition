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

