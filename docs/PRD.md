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

**TDD Mandate:** All feature stories follow TEST→IMPL pattern. Tests written
first define the contract, implementation makes tests pass.

### PHASE 1: A2A Protocol Compliance (PREREQUISITE)

#### STORY-001-TEST: Write A2A SDK messenger tests

Write tests defining messenger contract for A2A SDK integration.

**Acceptance Criteria:**

- `tests/test_messenger.py` updated with A2A SDK tests
- Tests define expected behavior for `ClientFactory.connect()`
- Tests define expected behavior for `create_text_message_object()`
- Tests mock async iteration over `send_message()` events
- Tests verify client caching per agent URL
- Test file is syntactically valid Python

**Files:** tests/test_messenger.py

---

#### STORY-001-IMPL: Refactor messenger to use A2A SDK

Implement messenger.py to pass A2A SDK tests.

**Acceptance Criteria:**

- `src/agentbeats/messenger.py` imports `ClientFactory`,
  `create_text_message_object` from `a2a.client`
- `talk_to_agent()` uses `await ClientFactory.connect(agent_url)`
- Messages created via `create_text_message_object(content=message)`
- Response extracted from `TaskState.completed` events
- Client caching per agent URL implemented
- `uv run pytest tests/test_messenger.py` passes
- `make type_check` passes

**Files:** src/agentbeats/messenger.py

---

#### STORY-002-TEST: Write TraceData task_id field tests

Write tests defining TraceData task_id field requirement.

**Acceptance Criteria:**

- `tests/test_messenger.py` updated with task_id tests
- Tests verify TraceData model has `task_id: str | None = None` field
- Tests verify `task.id` is captured in TraceData
- Tests verify existing fields preserved
- Test file is syntactically valid Python

**Files:** tests/test_messenger.py

---

#### STORY-002-IMPL: Add task_id field to TraceData

Implement task_id tracking in TraceData model.

**Acceptance Criteria:**

- `TraceData` model has new field: `task_id: str | None = None`
- `talk_to_agent()` captures `task.id` from A2A Task object
- Existing fields preserved
- `uv run pytest tests/test_messenger.py` passes
- `make type_check` passes

**Files:** src/agentbeats/messenger.py

---

#### STORY-003-TEST: Write Executor A2A cleanup tests

Write tests defining Executor cleanup contract for A2A clients.

**Acceptance Criteria:**

- `tests/test_executor.py` updated with cleanup tests
- Tests verify `Executor.execute()` calls `await messenger.close()`
- Tests verify `Messenger.close()` cleans up cached clients
- Test file is syntactically valid Python

**Files:** tests/test_executor.py

---

#### STORY-003-IMPL: Implement Executor A2A cleanup

Implement executor cleanup to pass tests.

**Acceptance Criteria:**

- `Executor.execute()` calls `await messenger.close()` after collecting traces
- `Messenger` has `close()` method to cleanup cached clients
- `uv run pytest tests/test_messenger.py tests/test_executor.py` passes
- `make type_check` passes

**Files:** src/agentbeats/executor.py, src/agentbeats/messenger.py

---

### PHASE 2: Real LLM Integration

#### STORY-004: Add OpenAI dependency

Add openai SDK to project dependencies.

**Acceptance Criteria:**

- `pyproject.toml` contains `openai>=1.0` in dependencies
- `uv sync` succeeds
- `uv run python -c "import openai"` succeeds

**Files:** pyproject.toml

---

#### STORY-005-TEST: Write LLM client config tests

Write tests defining LLM client configuration contract.

**Acceptance Criteria:**

- `tests/test_llm_judge.py` updated with config tests
- Tests verify LLMJudge reads `AGENTBEATS_LLM_API_KEY`
- Tests verify LLMJudge reads `AGENTBEATS_LLM_BASE_URL` (default:
  `https://api.openai.com/v1`)
- Tests verify LLMJudge reads `AGENTBEATS_LLM_MODEL` (default: `gpt-4o-mini`)
- Tests verify OpenAI-compatible endpoint support
- Test file is syntactically valid Python

**Files:** tests/test_llm_judge.py

---

#### STORY-005-IMPL: Implement LLM client config

Implement LLM client configuration to pass tests.

**Acceptance Criteria:**

- LLMJudge reads environment variables: `AGENTBEATS_LLM_API_KEY`,
  `AGENTBEATS_LLM_BASE_URL`, `AGENTBEATS_LLM_MODEL`
- Default base URL is `https://api.openai.com/v1`
- Default model is `gpt-4o-mini`
- Client supports any OpenAI-compatible endpoint
- `uv run pytest tests/test_llm_judge.py` passes
- `make type_check` passes

**Files:** src/agentbeats/evals/llm_judge.py

---

#### STORY-006-TEST: Write LLM prompt tests

Write tests defining LLM evaluation prompt contract.

**Acceptance Criteria:**

- `tests/test_llm_judge.py` updated with prompt tests
- Tests verify prompt serializes TraceData list
- Tests verify prompt asks for: overall_score (0-1), reasoning,
  coordination_quality, strengths, weaknesses
- Tests verify prompt requests JSON-formatted response matching LLMJudgment
  schema
- Tests verify prompt includes evaluation criteria
- Test file is syntactically valid Python

**Files:** tests/test_llm_judge.py

---

#### STORY-006-IMPL: Implement LLM prompt

Implement LLM evaluation prompt to pass tests.

**Acceptance Criteria:**

- Prompt serializes TraceData list into readable format
- Prompt asks for: overall_score (0-1), reasoning, coordination_quality,
  strengths, weaknesses
- Prompt requests JSON-formatted response matching LLMJudgment schema
- Prompt includes clear evaluation criteria for coordination quality
- `uv run pytest tests/test_llm_judge.py` passes
- `make type_check` passes

**Files:** src/agentbeats/evals/llm_judge.py

---

#### STORY-007-TEST: Write LLM API fallback tests

Write tests defining LLM API calls with fallback contract.

**Acceptance Criteria:**

- `tests/test_llm_judge.py` updated with API fallback tests
- Tests mock `openai.ChatCompletion.create()` (or equivalent async call)
- Tests verify LLM response parsing into LLMJudgment
- Tests verify fallback behavior when API fails
- Tests verify fallback behavior when API key not set
- Tests verify warning logged when using fallback (not error)
- Test file is syntactically valid Python

**Files:** tests/test_llm_judge.py

---

#### STORY-007-IMPL: Implement LLM API with fallback

Implement LLM API calls with fallback to pass tests.

**Acceptance Criteria:**

- If `AGENTBEATS_LLM_API_KEY` is set, use LLM API
- If LLM call fails or key not set, fall back to rule-based logic
- Log warning when using fallback (not error)
- Parse LLM JSON response into LLMJudgment object
- Handle API errors gracefully (timeout, invalid JSON, etc.)
- `uv run pytest tests/test_llm_judge.py` passes
- `make type_check` passes

**Files:** src/agentbeats/evals/llm_judge.py

---

### PHASE 3: Latency Metrics

#### STORY-008-TEST: Write latency evaluator tests

Write tests defining latency metrics evaluator contract.

**Acceptance Criteria:**

- `tests/test_latency.py` exists with focused tests
- Tests define expected behavior for `LatencyEvaluator.evaluate(traces)`
- Tests verify timestamp parsing from TraceData
- Tests verify percentile calculations: avg, p50, p95, p99
- Tests verify slowest agent URL identification
- Test file is syntactically valid Python

**Files:** tests/test_latency.py

---

#### STORY-008-IMPL: Implement latency evaluator

Implement latency metrics evaluator to pass tests.

**Acceptance Criteria:**

- `src/agentbeats/evals/latency.py` exists
- Follows existing evaluator pattern (like GraphEvaluator, LLMJudge)
- Parses timestamps from TraceData
- Computes: avg response time, p50, p95, p99
- Identifies slowest agent URL
- `Executor._evaluate_latency()` method added (follows tier pattern)
- Results included as `tier1_latency` in Executor response
- `uv run pytest tests/test_latency.py` passes
- `make type_check` and `make test_agent` pass

**Files:** src/agentbeats/evals/latency.py, src/agentbeats/executor.py

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
