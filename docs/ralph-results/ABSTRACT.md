# GraphJudge: Graph-Based Coordination Assessor for Multi-Agent Systems

## Abstract

We present GraphJudge, a graph-centric evaluation framework for AgentBeats that
measures **how agents coordinate**, not just whether they succeed. Traditional
benchmarks focus on task completion, overlooking interaction quality. GraphJudge
addresses this gap by measuring coordination network complexity against execution
outcomes through runtime structural analysis.

Derived from [Agents-eval](https://github.com/qte77/Agents-eval) — which
aims to evaluate autonomous research agents on the PeerRead dataset —
GraphJudge captures interaction traces during task execution and transforms
them into directed graphs (nodes = agents, edges = communication). We extract
**structural metrics** (centrality, density, efficiency) that quantify
bottlenecks, information flow, and collaboration quality.

**LLM-as-judge assessment** complements graph analysis with qualitative
evaluation via real LLM API calls (rule-based fallback). A **plugin
architecture** enables domain-specific evaluators (demonstrated via text metrics
for PeerRead). Metrics combine into an overall multi-agent system efficacy
score.

We validated the framework on a baseline purple agent across 5 runs, achieving
perfect reproducibility. GraphJudge operates as an A2A-compliant assessor with
standard endpoints, Docker deployment, and AgentBeats leaderboard integration.

![Agentic Graph Benchmark Architecture](../../assets/AgenticBenchArch.png)

**Categories**: Multi-agent Evaluation, Research Agent

**Contribution**: Agentified benchmark for multi-agent systems, quantifying
coordination quality through graph structural analysis. Demonstrated through
integration with agents-eval (research MAS using PeerRead dataset), GraphJudge
enables researchers to understand not just if agents coordinate, but how
effectively.

**Agent Registry**: <https://agentbeats.dev/qte77/graphjudge>

**Note**: Competition time constraints limited implementation scope; current
release focuses on core graph-based coordination assessment with demonstrated
reproducibility.
