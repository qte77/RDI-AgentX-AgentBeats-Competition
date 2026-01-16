---
title: Product Requirements Document - AgentBeats Benchmarking Enhancements
version: 1.0
applies-to: Agents and humans
purpose: Enhance evaluation system with real LLM integration, plugin architecture, and additional metrics
---

> See [UserStory.md](UserStory.md) for vision and value proposition.

## Overview

**Project Goal:** Evaluate multi-agent coordination quality through runtime
graph analysis to measure HOW agents collaborate. These enhancements enable
accurate coordination measurement by replacing synthetic data with real A2A
interactions.

This PRD extends the existing AgentBeats GreenAgent evaluation system with:

1. **A2A Protocol Compliance** - Fix Messenger to use A2A SDK (PREREQUISITE)
2. **Real LLM Integration** - Replace rule-based LLM Judge with actual API
   calls
3. **Latency Metrics** - Add response time analysis for performance
   benchmarking
4. **Documentation** - Document extensibility pattern for future custom
   evaluators

**Design Principles:** KISS, DRY, YAGNI - minimal changes, reuse existing
patterns, defer complex abstractions.

## Critical Finding

The current Messenger uses incompatible REST protocol (`POST /message`)
instead of A2A JSON-RPC. All benchmark results are currently
synthetic/mocked data, meaning we cannot measure real coordination
patterns—the core value proposition of GreenAgent. **Phase 1 must be
completed first** to enable real agent evaluation.

## Functional Requirements

### PHASE 1: A2A Protocol Compliance (PREREQUISITE)

#### STORY-001: Replace httpx with A2A SDK ClientFactory

**Why:** Enables capturing real agent coordination interactions instead of
synthetic data.

Refactor Messenger to use A2A SDK client for protocol compliance.

**Acceptance Criteria:**

- `src/agentbeats/messenger.py` imports `ClientFactory`,
  `create_text_message_object` from `a2a.client`
- `talk_to_agent()` uses `await ClientFactory.connect(agent_url)` instead
  of httpx
- Messages created via `create_text_message_object(content=message)`
- Response extracted from `TaskState.completed` events
- Client caching per agent URL for performance
- `make type_check` passes

**Files:** src/agentbeats/messenger.py

---

#### STORY-002: Update TraceData with task_id field

**Why:** Proper A2A task tracking enables correlation of coordination events
in graph analysis.

Add A2A task tracking to TraceData model.

**Acceptance Criteria:**

- `TraceData` model has new field: `task_id: str | None = None`
- `talk_to_agent()` captures `task.id` from A2A Task object
- Existing fields (`timestamp`, `agent_url`, `message`, `response`,
  `status_code`, `error`) preserved
- `make type_check` passes

**Files:** src/agentbeats/messenger.py

---

#### STORY-003: Update Executor and tests for A2A patterns

**Why:** Ensures clean A2A client lifecycle and validates protocol compliance
in tests.

Update Executor to clean up A2A clients and update test mocks.

**Acceptance Criteria:**

- `Executor.execute()` calls `await messenger.close()` after collecting traces
- `Messenger` has `close()` method to cleanup cached clients
- `tests/test_messenger.py` mocks `ClientFactory.connect()` instead of httpx
- `tests/test_messenger.py` mocks async iteration over `send_message()`
  events
- All messenger and executor tests pass
- `uv run pytest tests/test_messenger.py tests/test_executor.py` passes

**Files:** src/agentbeats/executor.py, tests/test_messenger.py

---

### PHASE 2: Real LLM Integration

#### STORY-004: Add OpenAI dependency

**Why:** Required for LLM-based coordination pattern assessment.

Add openai SDK to project dependencies.

**Acceptance Criteria:**

- `pyproject.toml` contains `openai>=1.0` in dependencies
- `uv sync` succeeds
- `uv run python -c "import openai"` succeeds

**Files:** pyproject.toml

---

#### STORY-005: Implement LLM client configuration

**Why:** Enables flexible LLM evaluation across different providers
(OpenAI, Azure, Ollama).

Add configurable OpenAI-compatible client to LLMJudge.

**Acceptance Criteria:**

- LLMJudge reads environment variables: `AGENTBEATS_LLM_API_KEY`,
  `AGENTBEATS_LLM_BASE_URL`, `AGENTBEATS_LLM_MODEL`
- Default base URL is `https://api.openai.com/v1`
- Default model is `gpt-4o-mini`
- Client supports any OpenAI-compatible endpoint (OpenAI, Azure, Ollama,
  vLLM)

**Files:** src/agentbeats/evals/llm_judge.py

---

#### STORY-006: Create LLM evaluation prompt

**Why:** Structured prompt ensures consistent coordination quality scoring
across evaluations.

Design prompt for agent coordination quality assessment.

**Acceptance Criteria:**

- Prompt serializes TraceData list into readable format
- Prompt asks for: overall_score (0-1), reasoning, coordination_quality,
  strengths, weaknesses
- Prompt requests JSON-formatted response matching LLMJudgment schema
- Prompt includes clear evaluation criteria for coordination quality

**Files:** src/agentbeats/evals/llm_judge.py

---

#### STORY-007: Implement LLM API calls with fallback

**Why:** Real LLM assessment provides nuanced coordination analysis beyond
rule-based logic.

Replace rule-based logic with actual LLM calls, keeping fallback.

**Acceptance Criteria:**

- If `AGENTBEATS_LLM_API_KEY` is set, use LLM API
- If LLM call fails or key not set, fall back to rule-based logic
- Log warning when using fallback (not error)
- Parse LLM JSON response into LLMJudgment object
- Handle API errors gracefully (timeout, invalid JSON, etc.)

**Files:** src/agentbeats/evals/llm_judge.py

---

#### STORY-008: Update LLM judge tests

**Why:** Validates LLM integration works correctly without requiring API keys
in tests.

Update tests to mock LLM API calls.

**Acceptance Criteria:**

- Tests mock `openai.ChatCompletion.create()` (or equivalent async call)
- Tests verify LLM response parsing
- Tests verify fallback behavior when API fails
- Tests verify fallback behavior when API key not set
- `uv run pytest tests/test_llm_judge.py` passes

**Files:** tests/test_llm_judge.py

---

### PHASE 3: Latency Metrics

#### STORY-009: Add latency metrics evaluator

**Why:** Identifies performance bottlenecks in coordination workflows.

Implement response time analysis for agent performance benchmarking.

**Acceptance Criteria:**

- `src/agentbeats/evals/latency.py` exists
- Follows existing evaluator pattern (like GraphEvaluator, LLMJudge)
- Parses timestamps from TraceData
- Computes: avg response time, p50, p95, p99
- Identifies slowest agent URL
- `tests/test_latency.py` verifies percentile calculations
- `Executor._evaluate_latency()` method added (follows tier pattern)
- Results included as `tier1_latency` in Executor response
- `make type_check` and `make test_agent` pass

**Files:** src/agentbeats/evals/latency.py, tests/test_latency.py,
src/agentbeats/executor.py

---

### PHASE 4: Documentation

#### STORY-010: Document evaluator extensibility pattern

**Why:** Enables benchmarkers to add domain-specific coordination metrics.

Document how to add custom evaluators for future plugin development.

**Acceptance Criteria:**

- `README.md` has new section: "Adding Custom Evaluators"
- Documents the current pattern: create evaluator class + add method to Executor
- Includes example code snippet showing how to add a new evaluator
- Mentions that formal plugin registry can be added later if needed
- Example follows KISS principle (no complex abstractions)
- Documentation is clear and actionable

**Files:** README.md

---

## Verification

After each phase:

1. **Tests pass**: `make test_agent`
2. **Type checking passes**: `make type_check`
3. **Formatting passes**: `make format && make lint`
4. **Manual validation**: Run green agent against purple agent, verify new
   metrics in output

## Dependencies

New dependencies to add:

- Phase 2: `openai>=1.0`
- Phase 3-4: No new dependencies

## Deferred (Future Work)

- Plugin architecture with base classes and registry
- BLEU score evaluator (TextMetrics covers basic text similarity)
- Semantic similarity via embeddings
- Error pattern categorization
- Performance profiling (consider scalene or py-spy for future profiling needs)

## Non-Goals

- Real-time streaming evaluation
- Persistent metrics storage (database)
- Metrics visualization UI
- Custom LLM fine-tuning
