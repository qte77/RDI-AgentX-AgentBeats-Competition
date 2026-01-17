# Reproducibility Analysis

This document demonstrates consistent evaluation results across multiple runs of
the AgentBeats GreenAgent assessor evaluating the baseline Purple Agent.

## Executive Summary

We conducted 5 independent evaluation runs using the same configuration to
measure reproducibility. **All evaluation metrics showed perfect consistency
(0% variance) except for execution duration**, which is expected due to
system-level timing variations.

**Key Finding**: The GreenAgent evaluation framework produces **100%
reproducible results** for all assessment metrics across multiple runs.

## Test Configuration

| Parameter | Value |
| --------- | ----- |
| Test Date | 2026-01-15 |
| Agent Under Test | Purple Agent (baseline demo agent) |
| Agent URL | `http://localhost:9010` |
| Number of Runs | 5 |
| Success Rate | 100% (5/5 successful) |
| Evaluation Messages | 3 coordination prompts (standard test set) |

### Evaluation Messages

The same three messages were sent in each run:

1. "Hello, can you help me coordinate a task?"
2. "What are your coordination capabilities?"
3. "How would you handle a multi-agent scenario?"

## Results

### Run-by-Run Data

| Run | Duration | Nodes | Edges | Centrality | Quality | Similarity |
| --- | -------- | ----- | ----- | ---------- | ------- | ---------- |
| 1   | 0.1951   | 2     | 1     | 0.0        | 0.0     | 1.0        |
| 2   | 0.0385   | 2     | 1     | 0.0        | 0.0     | 1.0        |
| 3   | 0.0618   | 2     | 1     | 0.0        | 0.0     | 1.0        |
| 4   | 0.0492   | 2     | 1     | 0.0        | 0.0     | 1.0        |
| 5   | 0.0305   | 2     | 1     | 0.0        | 0.0     | 1.0        |

*Latency evaluator was implemented after this reproducibility test
(STORY-008)

### Variance Analysis

#### Tier 1: Graph Metrics (Structural Analysis)

##### Graph Metrics: Perfect Reproducibility (0% variance)

| Metric | Mean | Std Dev | Min | Max | Range | CV% |
| -------------- | ---- | ------- | --- | --- | ----- | ----- |
| Node Count | 2.0 | 0.0 | 2 | 2 | 0 | 0.00% |
| Edge Count | 1.0 | 0.0 | 1 | 1 | 0 | 0.00% |
| Avg Centrality | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A |

**Interpretation**: The graph structure derived from agent interactions is
identical across all runs. This demonstrates deterministic behavior in the
Purple Agent's response patterns and the GreenAgent's graph construction
algorithm.

#### Tier 2: LLM Judge (Coordination Quality)

##### LLM Judge: Perfect Reproducibility (0% variance)

| Metric | Mean | Std Dev | Min | Max | Range | CV% |
| ------------- | ---- | ------- | --- | --- | ----- | --- |
| Quality Score | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | N/A |

**Interpretation**: The LLM judge produced identical assessments across all
runs. The baseline Purple Agent does not implement substantive coordination
capabilities, resulting in a consistent score of 0.0.

#### Tier 3: Text Metrics (Response Similarity)

##### Text Metrics: Perfect Reproducibility (0% variance)

| Metric | Mean | Std Dev | Min | Max | Range | CV% |
| ---------------- | ---- | ------- | --- | --- | ----- | ----- |
| Similarity Score | 1.0 | 0.0 | 1.0 | 1.0 | 0.0 | 0.00% |

**Interpretation**: The Purple Agent generates identical responses to identical
inputs, resulting in perfect similarity scores (1.0) across all evaluations.

#### Tier 1: Latency Metrics (Performance Analysis)

**Note**: Latency evaluator (STORY-008) was implemented after this
reproducibility test. Future reproducibility runs will include:

| Metric            | Expected Behavior                     |
|-------------------|---------------------------------------|
| Avg Latency (ms)  | Baseline response time measurement    |
| P50 Latency (ms)  | Median latency (should be stable)     |
| P95 Latency (ms)  | 95th percentile (detects outliers)    |
| P99 Latency (ms)  | 99th percentile (detects worst-case)  |
| Slowest Agent URL | Identifies performance bottlenecks    |

**Expected Reproducibility**: Latency metrics show timing variance (similar to
execution duration) but should be consistent in relative ordering and agent
identification.

#### Execution Duration

##### Expected Variance (90.86% CV)

| Metric       | Mean  | Std Dev | Min   | Max   | Range | CV%    |
| ------------ | ----- | ------- | ----- | ----- | ----- | ------ |
| Duration (s) | 0.075 | 0.068   | 0.031 | 0.195 | 0.165 | 90.86% |

**Interpretation**: Execution time varies due to system-level factors (CPU
scheduling, I/O operations, network latency). This variance is **expected and
does not affect evaluation quality**. The first run (0.195s) includes cold-start
overhead, while subsequent runs (0.031-0.062s) benefit from warm caches.

## Reproducibility Metrics

### Coefficient of Variation (CV)

The CV measures relative variability as `(std_dev / mean) * 100%`:

- **CV < 10%**: Excellent reproducibility
- **CV 10-20%**: Good reproducibility
- **CV > 20%**: High variability (investigation needed)

### Results Summary

| Metric Category | CV% | Assessment |
| -------------------------- | ------ | -------------------------- |
| Graph Node Count | 0.00% | Perfect reproducibility |
| Graph Edge Count | 0.00% | Perfect reproducibility |
| Graph Avg Centrality | 0.00% | Perfect reproducibility |
| Coordination Quality Score | 0.00% | Perfect reproducibility |
| Response Similarity Score | 0.00% | Perfect reproducibility |
| Execution Duration | 90.86% | Expected variance (non-metric) |

## Conclusions

### Key Findings

1. **Perfect Metric Reproducibility**: All evaluation metrics (graph structure,
   LLM judge scores, text similarity) show 0% variance across 5 independent runs.

2. **Deterministic Agent Behavior**: The Purple Agent produces identical
   responses to identical inputs, demonstrating proper stateless operation.

3. **Stable Evaluation Pipeline**: The GreenAgent evaluation framework
   (Messenger, GraphEvaluator, LLMJudge, TextMetrics) produces consistent
   results when given identical inputs.

4. **Timing Variance is Expected**: Execution duration varies due to
   system-level factors but does not affect evaluation quality.

### Implications for AgentBeats Competition

- **Fair Evaluation**: All purple agents will be assessed using the same
  reproducible methodology.
- **Comparable Results**: Results from different evaluation runs can be directly
  compared.
- **Reliable Leaderboard**: The leaderboard reflects true agent capabilities,
  not random variation.

### Reproducibility Best Practices

To ensure reproducible evaluations:

1. **Use Fixed Message Sets**: Always use the same evaluation messages for
   comparability
2. **Document Configuration**: Record all evaluation parameters (agent URL,
   message content, timestamps)
3. **Multiple Runs**: Run evaluations 3-5 times to verify consistency
4. **Track Variance**: Monitor CV% to detect unexpected variability
5. **Version Control**: Lock dependency versions (`uv.lock`) for deterministic
   builds

## Raw Data

Full reproducibility test results are available at:

```text
reproducibility-results/reproducibility-20260115-184659.json
```

This file contains:

- Individual run results with task IDs
- Complete variance analysis
- Timestamps for all operations
- Full metric breakdowns

## Reproducing These Results

To reproduce this analysis:

```bash
# 1. Start the purple agent
cd examples/purple-agent
uv run python -m purpleagent.server --port 9010 &

# 2. Run reproducibility test
cd ../..
PYTHONPATH=src uv run python scripts/test_reproducibility.py \
  http://localhost:9010 5

# 3. View results
cat reproducibility-results/reproducibility-*.json
```

The test script (`scripts/test_reproducibility.py`) automatically:

- Runs N evaluation iterations with the same configuration
- Computes mean, standard deviation, range, and CV% for all metrics
- Identifies high-variance metrics (CV > 10%)
- Generates timestamped JSON reports

## Statistical Notes

### Sample Size

We used **n=5 runs**, which provides:

- Sufficient data for variance analysis (n ≥ 2 required for std dev)
- Fast execution (< 1 second total runtime)
- Clear demonstration of reproducibility

For production leaderboard evaluations, we recommend:

- **Standard evaluation**: 3 runs (fast, detects gross inconsistencies)
- **Challenge evaluation**: 5 runs (better variance estimates)
- **Research evaluation**: 10+ runs (publication-quality statistics)

### Zero Variance Interpretation

When std dev = 0.0 (perfect consistency):

- CV% is reported as 0.00% for metrics with non-zero mean
- CV% is undefined (N/A) for metrics with zero mean
- This indicates **deterministic behavior** (not random chance)

## Appendix: Test Environment

### Software Versions

```text
Python: 3.13
a2a-sdk: 0.3.20
networkx: 3.0+
pydantic: 2.0+
```

### Hardware

Test was conducted on:

- Platform: Linux (containerized environment)
- System: Development workstation
- Network: localhost (no external latency)

### Evaluation Framework Components

1. **Messenger** (`src/agentbeats/messenger.py`): A2A client with trace capture
2. **GraphEvaluator** (`src/agentbeats/evals/graph.py`): NetworkX-based
   structural analysis
3. **LatencyEvaluator** (`src/agentbeats/evals/latency.py`): Response time
   performance analysis
4. **LLMJudge** (`src/agentbeats/evals/llm_judge.py`): Coordination quality
   assessment with real LLM API
5. **TextMetrics** (`src/agentbeats/evals/text_metrics.py`): Response
   similarity scoring
6. **Agent Orchestrator** (`src/agentbeats/agent.py`): End-to-end evaluation
   pipeline

---

**Document Version**: 1.0
**Generated**: 2026-01-15
**Test ID**: `reproducibility-20260115-184659`
**Status**: ✅ All metrics demonstrate perfect reproducibility
