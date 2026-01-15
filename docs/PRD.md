# Product Requirements Document - AgentBeats GreenAgent

> See [UserStory.md](UserStory.md) for vision and value proposition.

## Functional Requirements

### STORY-001: Create pyproject.toml with dependencies

Initialize Python project with A2A and graph dependencies.

**Acceptance Criteria:**

- `pyproject.toml` exists with a2a-sdk[http-server]>=0.3.20
- `pyproject.toml` contains networkx>=3.0, pydantic>=2.0, httpx>=0.27
- `uv sync` succeeds
- `uv run python -c "import a2a, networkx"` succeeds

**Files:** pyproject.toml

---

### STORY-002-TEST: Write messenger tests

Write tests defining messenger contract (test file creation = passing).

**Acceptance Criteria:**

- `tests/test_messenger.py` exists with focused tests
- Tests define expected behavior for Messenger.talk_to_agent()
- Tests define expected behavior for Messenger.get_traces()
- Test file is syntactically valid Python

**Files:** tests/test_messenger.py

---

### STORY-002-IMPL: Implement messenger with trace capture

Implement messenger.py to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/messenger.py` exists
- `uv run pytest tests/test_messenger.py` passes
- `make type_check` passes

**Files:** src/agentbeats/**init**.py, src/agentbeats/messenger.py

---

### STORY-003-TEST: Write graph evaluator tests

Write tests defining graph evaluator contract.

**Acceptance Criteria:**

- `tests/test_graph.py` exists with focused tests
- Tests define expected behavior for GraphEvaluator.build_graph(traces)
- Tests define expected metrics: node_count, edge_count, centrality
- Test file is syntactically valid Python

**Files:** tests/test_graph.py

---

### STORY-003-IMPL: Implement graph evaluator (Tier 1)

Implement graph.py to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/evals/graph.py` exists
- `uv run pytest tests/test_graph.py` passes
- `make type_check` passes

**Files:** src/agentbeats/evals/**init**.py, src/agentbeats/evals/graph.py

---

### STORY-004-TEST: Write LLM judge tests

Write tests defining LLM judge contract.

**Acceptance Criteria:**

- `tests/test_llm_judge.py` exists with focused tests
- Tests define expected behavior for LLMJudge.evaluate(traces)
- Tests use mocks for LLM calls (no real API needed)
- Test file is syntactically valid Python

**Files:** tests/test_llm_judge.py

---

### STORY-004-IMPL: Implement LLM judge evaluator (Tier 2)

Implement llm_judge.py to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/evals/llm_judge.py` exists
- `uv run pytest tests/test_llm_judge.py` passes
- `make type_check` passes

**Files:** src/agentbeats/evals/llm_judge.py

---

### STORY-005-TEST: Write text metrics tests

Write tests defining text metrics contract.

**Acceptance Criteria:**

- `tests/test_text_metrics.py` exists with focused tests
- Tests define expected behavior for TextMetrics.evaluate(response, reference)
- Tests cover similarity score range (0-1)
- Test file is syntactically valid Python

**Files:** tests/test_text_metrics.py

---

### STORY-005-IMPL: Implement text metrics plugin (Tier 3)

Implement text_metrics.py to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/evals/text_metrics.py` exists
- `uv run pytest tests/test_text_metrics.py` passes
- `make type_check` passes

**Files:** src/agentbeats/evals/text_metrics.py

---

### STORY-006-TEST: Write executor tests

Write tests defining A2A executor contract.

**Acceptance Criteria:**

- `tests/test_executor.py` exists with focused tests
- Tests define expected behavior for Executor.execute()
- Tests define task lifecycle: pending → working → completed
- Test file is syntactically valid Python

**Files:** tests/test_executor.py

---

### STORY-006-IMPL: Implement executor module

Implement executor.py to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/executor.py` exists
- `uv run pytest tests/test_executor.py` passes
- `make type_check` passes

**Files:** src/agentbeats/executor.py

---

### STORY-007-TEST: Write agent orchestrator tests

Write tests defining agent orchestrator contract.

**Acceptance Criteria:**

- `tests/test_agent.py` exists with focused tests
- Tests define EvalRequest model structure and validation
- Tests define expected Agent.run() orchestration flow
- Test file is syntactically valid Python

**Files:** tests/test_agent.py

---

### STORY-007-IMPL: Implement agent orchestrator

Implement agent.py to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/agent.py` exists
- `uv run pytest tests/test_agent.py` passes
- `make type_check` passes

**Files:** src/agentbeats/agent.py

---

### STORY-008-TEST: Write server tests

Write tests defining A2A server contract.

**Acceptance Criteria:**

- `tests/test_server.py` exists with focused tests
- Tests define AgentCard endpoint response structure
- Tests define server startup and health behavior
- Test file is syntactically valid Python

**Files:** tests/test_server.py

---

### STORY-008-IMPL: Implement server entry point

Implement server.py to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/server.py` exists
- `uv run pytest tests/test_server.py` passes
- `curl localhost:9009/.well-known/agent.json` returns valid JSON

**Files:** src/agentbeats/server.py

---

### STORY-009: Create Dockerfile

Create container for AgentBeats deployment.

**Acceptance Criteria:**

- `Dockerfile` exists at project root
- `docker build -t green-agent .` succeeds
- `docker run -p 9009:9009 green-agent` responds to agent card request

**Files:** Dockerfile

---

### STORY-010: Add Makefile targets

Add convenience targets for development.

**Acceptance Criteria:**

- `make run_agent` starts server
- `make build_agent` builds Docker
- `make test_agent` runs agentbeats tests
- All targets work without errors

**Files:** Makefile
