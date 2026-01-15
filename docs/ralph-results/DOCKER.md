# Docker Deployment Guide

This document describes how to build and run the AgentBeats GreenAgent using Docker.

## Building the Image

Build the Docker image for linux/amd64 architecture:

```bash
docker build -t green-agent .
```

## Running the Container

### Default Configuration

Run with default settings (host: 0.0.0.0, port: 9009):

```bash
docker run -p 9009:9009 green-agent
```

### Custom Configuration

Run with custom host, port, and card URL:

```bash
docker run -p 8080:8080 green-agent --host 0.0.0.0 --port 8080 --card-url http://example.com:8080
```

## Verifying the Deployment

Test the agent card endpoint:

```bash
curl http://localhost:9009/.well-known/agent-card.json
```

Expected response should contain:
- Agent name: "AgentBeats GreenAgent"
- Description of multi-tier evaluation capabilities
- List of skills: graph_evaluation, llm_judging, text_metrics, agent_assessment

## Architecture

The Dockerfile:
- Targets `linux/amd64` platform
- Uses Python 3.13 slim base image
- Installs dependencies via uv package manager
- Exposes port 9009 by default
- Runs the A2A server with configurable host, port, and card URL

## Environment Variables

- `PYTHONUNBUFFERED=1` - Ensures logs are sent to stdout immediately
- `PYTHONDONTWRITEBYTECODE=1` - Prevents Python from writing .pyc files

## Production Considerations

- The image installs only production dependencies (no dev or test packages)
- Layer caching is optimized by copying pyproject.toml before source code
- .dockerignore excludes unnecessary files to reduce image size
