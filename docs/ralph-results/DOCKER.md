# Docker Deployment

## Build

```bash
docker build -t green-agent .
```

## Run

**Default** (host: 0.0.0.0, port: 9009):

```bash
docker run -p 9009:9009 green-agent
```

**Custom configuration**:

```bash
docker run -p 8080:8080 green-agent --host 0.0.0.0 --port 8080 --card-url http://example.com:8080
```

**With LLM evaluation**:

```bash
docker run -p 9009:9009 \
  -e AGENTBEATS_LLM_API_KEY="your-api-key" \
  -e AGENTBEATS_LLM_BASE_URL="https://api.openai.com/v1" \
  -e AGENTBEATS_LLM_MODEL="gpt-4o-mini" \
  green-agent
```

## Verify

```bash
curl http://localhost:9009/.well-known/agent.json
```

## Environment Variables

**LLM Evaluation** (optional, uses rule-based fallback if not set):

- `AGENTBEATS_LLM_API_KEY` - API key for LLM provider
- `AGENTBEATS_LLM_BASE_URL` - OpenAI-compatible endpoint (default: `https://api.openai.com/v1`)
- `AGENTBEATS_LLM_MODEL` - Model name (default: `gpt-4o-mini`)

**Runtime** (set by Dockerfile):

- `PYTHONUNBUFFERED=1` - Immediate log output
- `PYTHONDONTWRITEBYTECODE=1` - No .pyc files
- `PYTHONPATH=/app/src` - Module path resolution
