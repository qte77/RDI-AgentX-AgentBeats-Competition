---
title: AgentBeats Competition - Requirements Analysis
version: 1.0
applies-to: all-agents
purpose: Official competition requirements, compliance status, and execution strategy
created: 2026-01-15
---

## Official Green Agent (Assessor) Requirements

### Mandatory Technical Requirements [[2](https://github.com/RDI-Foundation/green-agent-template)]

| Requirement | Details |
| ----------- | ------- |
| **A2A Protocol** | Universal interface - agents must expose A2A endpoints |
| **Docker** | Containerized (GHCR publication not required) |
| **Architecture** [[1](https://github.com/RDI-Foundation/agentbeats-tutorial)] | Build for `linux/amd64` (best practice) |
| **ENTRYPOINT** [[1](https://github.com/RDI-Foundation/agentbeats-tutorial)] | Accept CLI args: `--host`, `--port`, `--card-url` (best practice) |
| **AgentCard** | Expose at `/.well-known/agent.json` |
| **Reproducibility** | Fresh state each run, no cross-assessment state |
| **Task ID Namespacing** [[1](https://github.com/RDI-Foundation/agentbeats-tutorial)] | Use `task_id` to namespace temporary resources (best practice) |

### Official Scaffold Structure

From
[green-agent-template](https://github.com/RDI-Foundation/green-agent-template):

```text
src/
├── server.py      # A2A server setup + AgentCard metadata
├── executor.py    # AgentExecutor - request handling
├── agent.py       # Evaluation logic
└── messenger.py   # A2A messaging utilities

tests/
└── test_agent.py  # A2A conformance tests

Dockerfile         # Containerization
.github/workflows/test-and-publish.yml  # CI/CD (optional)
pyproject.toml     # Dependencies
```

### Required Dependencies [[2](https://github.com/RDI-Foundation/green-agent-template)]

```toml
dependencies = [
    "a2a-sdk[http-server]>=0.3.20",  # A2A protocol + HTTP server
    "pydantic>=2.12.5",               # Data validation
    "uvicorn>=0.38.0",                # ASGI server
    "httpx>=0.28.0",                  # HTTP client for messaging
]
requires-python = ">=3.13"
```

---

## Official Best Practices

### From AgentBeats Tutorial [[1](https://github.com/RDI-Foundation/agentbeats-tutorial)]

**Green Agent Design Patterns:**

1. **Artifact Submission** - Purple agents produce outputs for evaluation
2. **Traced Environments** - Observe agent actions (MCP, SSH, hosted
   services)
3. **Message-Based Assessment** - Evaluate via dialogue, Q&A, reasoning
4. **Multi-Agent Games** - Orchestrate competitive/collaborative interactions

**Performance & Reliability:**

- Lightweight role: verification and orchestration only
- Avoid heavy computation; delegate to purple agents
- Set appropriate timeouts for network communication
- Emit A2A task updates for progress tracking in web UI

**Reproducibility Standards:**

- Start each assessment with clean state
- Use `task_id` to namespace resources
- Prevent state carryover between concurrent assessments
- Support complete reset mechanisms

**Security & Cost:**

- BYOK (Bring-Your-Own-Key) model for LLM APIs
- Use environment variables for API keys (never hardcode)
- Implement spending limits ($10 limit, $5 alert recommended)

---

## This Repository Scaffold Analysis

### Current Structure (from PRD.md)

```text
src/agentbeats/                    # ✅ Cleaner package structure
├── server.py                      # ✅ Planned (STORY-008)
├── executor.py                    # ✅ Planned (STORY-006)
├── agent.py                       # ✅ Planned (STORY-007)
├── messenger.py                   # ✅ Planned (STORY-002)
└── evals/                         # ✅ UNIQUE VALUE-ADD
    ├── graph.py                   # ✅ NetworkX coordination metrics
    ├── llm_judge.py               # ✅ Qualitative assessment
    └── text_metrics.py            # ✅ Text similarity

tests/                             # ✅ TDD approach
├── test_messenger.py
├── test_graph.py
├── test_llm_judge.py
├── test_text_metrics.py
├── test_executor.py
├── test_agent.py
└── test_server.py

Dockerfile                         # ✅ Planned (STORY-009)
Makefile                           # ✅ Planned (STORY-010)
```

### Dependencies Status

| Dependency | Required | This Repo | Status |
| ---------- | -------- | --------- | ------ |
| `a2a-sdk[http-server]>=0.3.20` | ✅ Yes | ✅ Fixed | **ALIGNED** |
| `uvicorn>=0.38.0` | ✅ Yes | ✅ Fixed | **ALIGNED** |
| `httpx>=0.28.0` | ✅ Yes | ✅ Fixed | **ALIGNED** |
| `pydantic>=2.12.5` | ✅ Yes | ✅ Already had | **ALIGNED** |
| `networkx>=3.6.1` | N/A | ✅ Has (for evals) | **BONUS** |
| Python `>=3.13` | ✅ Yes | ✅ Fixed (was ==3.14) | **ALIGNED** |

---

## Compliance Status

### ✅ All Official Requirements Met

PRD.md is **fully compliant** with AgentBeats competition requirements:

| Requirement | PRD Coverage | Story |
| ----------- | ------------ | ----- |
| A2A protocol | ✅ Complete | STORY-006, 007, 008 |
| CLI args (`--host`, `--port`, `--card-url`) | ✅ Specified | STORY-008:220 |
| Docker + `linux/amd64` | ✅ Specified | STORY-009:236 |
| Fresh state per assessment | ✅ Specified | STORY-007:189 |
| Task ID namespacing | ✅ Specified | STORY-007:190 |
| Baseline purple agent | ✅ Complete story | STORY-011 |
| Required dependencies | ✅ All present | pyproject.toml |
| Package structure | ✅ Clean design | `src/agentbeats/` |
| TDD approach | ✅ Comprehensive | 17 TEST/IMPL pairs |
| Type checking | ✅ Strict | pyright configured |

### ✨ Unique Competitive Advantages

| Strength | Description |
| -------- | ----------- |
| **Evaluation plugins** | `evals/` module is unique - no template has this |
| **Graph metrics** | NetworkX-based coordination analysis (novel) |
| **Tiered evaluation** | 3 tiers: graph → LLM → text metrics |
| **Package organization** | `src/agentbeats/` cleaner than flat `src/` |
| **Comprehensive testing** | 17 stories with TEST/IMPL pairs |
| **Core principles** | Explicit KISS/DRY/YAGNI enforcement |

---

## Execution Strategy

### ✅ Requirements Complete - Focus on Implementation

All competition requirements are addressed in PRD.md. Execute stories in order:

**Phase 1 (MVP - Critical Path):**

1. STORY-001: Dependencies (`pyproject.toml`)
2. STORY-002: Messenger (A2A communication)
3. STORY-003: Graph evaluator (Tier 1 - core value)
4. STORY-006: Executor (A2A task handling)
5. STORY-007: Agent orchestrator (evaluation logic)
6. STORY-008: Server (A2A endpoints + AgentCard)
7. STORY-009: Dockerfile (containerization)
8. STORY-011: Baseline purple agent (demo)

**Phase 2 (Enhancement - Post-MVP):**

- STORY-004: LLM judge (Tier 2)
- STORY-005: Text metrics (Tier 3)
- STORY-010: Makefile targets

**Competitive Advantages to Preserve:**

- Graph metrics focus (innovation differentiator)
- `src/agentbeats/evals/` plugin architecture
- TDD workflow (quality assurance)
- Core principles alignment (judging criteria)

---

## Official Assessment Patterns (Reference)

From
[agentbeats-tutorial](https://github.com/RDI-Foundation/agentbeats-tutorial):

### Assessment Flow

```json
// Green agent receives:
{
  "participants": {
    "<role>": "<endpoint_url>"
  },
  "config": {}
}

// Green agent produces:
{
  "task_updates": ["logs", "progress"],
  "artifacts": [
    {
      "name": "results.json",
      "data": { "score": 0.85, "metrics": {...} }
    }
  ]
}
```

---

## Submission Checklist

Based on [competition requirements](https://rdi.berkeley.edu/agentx-agentbeats):

- [x] **GitHub Repository** - Complete source code + README
- [ ] **Abstract** - Brief description of evaluation tasks
- [ ] **Docker Image** - Runs end-to-end without manual intervention
- [ ] **AgentBeats Registration** - Registered on platform
- [ ] **Baseline Purple Agent(s)** - A2A-compatible demo agents
- [ ] **Demo Video** - Up to 3 minutes
- [ ] **Submission Form** - Complete by 11:59pm PT TODAY

---

## Competition Judging Criteria [[3](https://rdi.berkeley.edu/agentx-agentbeats)]

**Note**: Competition page lists five criteria without percentages.

### Technical Correctness

- Code quality, documentation, robust error handling
- Docker builds reliably
- Reasonable resource requirements

### Reproducibility

- Consistent results across runs
- Fresh state per assessment

### Benchmark Design Quality

- Realistic, meaningful tasks
- Tests genuine agentic capabilities
- Avoids trivial/heuristic solutions

### Evaluation Methodology

- Clear, objective, justifiable scoring
- Automated where feasible
- Beyond binary pass/fail

### Innovation & Impact

- Addresses evaluation gaps
- Originality beyond simple ports

---

## Sources

- [AgentBeats Tutorial](https://github.com/RDI-Foundation/agentbeats-tutorial)
- [Green Agent Template](https://github.com/RDI-Foundation/green-agent-template)
- [Competition Page](https://rdi.berkeley.edu/agentx-agentbeats)
- [AgentBeats Documentation](https://docs.agentbeats.dev/tutorial/)
- [AgentBeats Docs - AAA](https://docs.agentbeats.org/)
- [Submission Form](https://docs.google.com/forms/d/e/1FAIpQLSdtqxWcGl2Qg5RPuNF2O3_N07uD0HMJpWBCwZWZbD3dxTuWmg/viewform)
