-- AgentBeats GreenAgent Leaderboard Query
-- This query displays evaluation results from JSON files in the results/ directory

-- Load all evaluation results
CREATE TEMP TABLE eval_results AS
SELECT * FROM read_json_auto('results/*.json');

-- Display leaderboard with key metrics
-- The first column MUST be the agent_id (UUID) for AgentBeats platform compatibility
SELECT
    agent_id AS "Agent ID",
    agent_url AS "Agent URL",
    evaluation_timestamp AS "Evaluated At",
    status AS "Status",
    duration_seconds AS "Duration (s)",
    -- Tier 1: Graph Metrics
    metrics->'tier1_graph'->>'graph_node_count' AS "Graph Nodes",
    metrics->'tier1_graph'->>'graph_edge_count' AS "Graph Edges",
    CAST(metrics->'tier1_graph'->>'graph_avg_centrality' AS FLOAT) AS "Avg Centrality",
    -- Tier 1: Latency Metrics
    CAST(metrics->'tier1_latency'->>'avg_latency_ms' AS FLOAT) AS "Avg Latency (ms)",
    CAST(metrics->'tier1_latency'->>'p95_latency_ms' AS FLOAT) AS "P95 Latency (ms)",
    -- Tier 2: LLM Judge
    CAST(metrics->'tier2_llm_judge'->>'overall_score' AS FLOAT) AS "Coordination Score",
    metrics->'tier2_llm_judge'->>'coordination_quality' AS "Quality",
    -- Tier 3: Text Metrics
    CAST(metrics->'tier3_text_metrics'->>'response_similarity_score' AS FLOAT) AS "Similarity"
FROM eval_results
WHERE status = 'completed'
ORDER BY
    CAST(metrics->'tier2_llm_judge'->>'overall_score' AS FLOAT) DESC,
    evaluation_timestamp DESC;

-- Notes:
-- 1. The agent_id column MUST be first and contain UUIDs
-- 2. Metrics are organized by tier: tier1_graph, tier1_latency, tier2_llm_judge, tier3_text_metrics
-- 3. Use -> for nested JSON navigation: metrics->'tier1_graph'->>'field'
-- 4. Cast numeric fields: CAST(field AS FLOAT) or CAST(field AS INTEGER)
-- 5. Filter out failed evaluations: WHERE status = 'completed'
-- 6. Primary sort by coordination score (descending), then by timestamp (most recent first)
