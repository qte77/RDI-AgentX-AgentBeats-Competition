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

-- Notes:
-- 1. The agent_id column MUST be first and contain UUIDs
-- 2. Use ->>'field' to extract JSON string fields
-- 3. Cast numeric fields: CAST(field AS FLOAT) or CAST(field AS INTEGER)
-- 4. Filter out failed evaluations: WHERE status = 'completed'
-- 5. Primary sort by coordination score (descending), then by timestamp (most recent first)
