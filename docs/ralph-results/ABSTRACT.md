# GreenAgent: Graph-Based Coordination Assessor for Multi-Agent Systems

## Abstract

We present GreenAgent, a novel evaluation framework for the AgentBeats competition that measures **how agents coordinate**, not just whether they succeed. Traditional agent benchmarks focus on task completion metrics, overlooking the quality of inter-agent interactions. GreenAgent addresses this gap through multi-tier runtime coordination analysis.

Our approach combines three complementary evaluation methodologies: (1) **Graph-based structural analysis** using NetworkX to quantify coordination patterns through metrics like node centrality, edge density, and communication efficiency; (2) **LLM-as-judge assessment** that provides qualitative evaluation of coordination quality, adaptability, and collaborative behaviors; (3) **Text similarity scoring** for measuring response consistency across multiple evaluation runs.

GreenAgent operates as an A2A-compliant assessor that captures interaction traces between agents during task execution. These traces are transformed into directed graphs where nodes represent agents and edges represent communication events. We extract structural metrics that reveal coordination bottlenecks, information flow patterns, and collaboration quality. The LLM judge layer provides semantic understanding of agent behaviors, while text metrics ensure reproducibility.

We demonstrate the framework's effectiveness through evaluation of a baseline purple agent, achieving perfect reproducibility (0% variance) across all metrics in 5 independent runs. The system exposes standard A2A endpoints, supports containerized deployment via Docker, and integrates with the AgentBeats platform leaderboard for transparent result sharing.

GreenAgent fills a critical gap in multi-agent evaluation by providing quantitative graph metrics and qualitative behavioral assessment, enabling researchers to understand not just if coordination occurred, but how effectively agents collaborate.

**Word Count**: 243 words
