# Demo Video Script

**Duration**: Maximum 3 minutes
**Purpose**: Demonstrate GreenAgent evaluation capabilities for AgentBeats submission

## Script Outline

### Section 1: Introduction (30 seconds)

**Visual**: Title slide + repository overview

**Narration**:
> "Welcome to GreenAgent, a graph-based coordination assessor for the AgentBeats competition. Unlike traditional benchmarks that only measure task success, GreenAgent evaluates HOW agents coordinate through multi-tier analysis."

**Screen**:
- Show README.md with architecture diagram
- Highlight key features: graph metrics, LLM judge, text similarity

### Section 2: Agent Startup (45 seconds)

**Visual**: Terminal demonstrating server startup

**Commands to show**:
```bash
# 1. Start GreenAgent server
uv run src/agentbeats/server.py --host 0.0.0.0 --port 9009

# 2. Verify A2A endpoint (new terminal)
curl http://localhost:9009/.well-known/agent.json
```

**Narration**:
> "GreenAgent exposes A2A-compliant endpoints. The agent card describes our evaluation capabilities: graph-based structural analysis, LLM-as-judge coordination assessment, and text similarity metrics."

**Screen**:
- Show JSON output highlighting "skills" section
- Point out three evaluation tiers

### Section 3: Evaluation Flow (90 seconds)

**Visual**: Running evaluation against purple agent

**Commands to show**:
```bash
# 1. Start baseline purple agent
cd examples/purple-agent
uv run python -m purpleagent.server --port 9010 &

# 2. Run evaluation script
cd ../..
uv run scripts/evaluate_purple_agent.py http://localhost:9010
```

**Narration**:
> "Let's evaluate our baseline purple agent. The evaluation flow captures interaction traces as agents communicate, then analyzes coordination quality through three tiers."

**Screen**:
1. Show evaluation messages being sent
2. Display trace capture in progress
3. Show graph construction from traces
4. Highlight metrics being calculated:
   - Graph: node count, edge count, centrality
   - LLM Judge: coordination quality score
   - Text Metrics: response similarity

**Visual overlays** (if possible):
- Diagram of communication graph being built
- Metrics appearing as they're calculated

### Section 4: Results Interpretation (45 seconds)

**Visual**: Evaluation results JSON

**Commands to show**:
```bash
# Display results
cat leaderboard-results/purple-agent-baseline.json | jq
```

**Narration**:
> "Results show three evaluation tiers: Tier 1 graph metrics quantify network structure; Tier 2 LLM judge provides qualitative coordination assessment; Tier 3 text metrics ensure consistency. The baseline agent shows minimal coordination, as expected for a simple demo agent."

**Screen**:
- Highlight each tier's metrics in the JSON output
- Show interpretation:
  - 2 nodes, 1 edge = minimal interaction
  - Quality score 0.0 = no substantive coordination
  - Similarity 1.0 = deterministic responses

**Visual**: Show reproducibility results
```bash
# Demonstrate reproducibility
cat docs/REPRODUCIBILITY.md
```

**Narration**:
> "Five independent runs show perfect reproducibility: 0% variance in all evaluation metrics. This ensures fair, consistent assessment across all agents."

### Section 5: Leaderboard Integration (30 seconds)

**Visual**: GitHub leaderboard repository and DuckDB query

**Commands to show**:
```bash
# Show leaderboard structure
cat docs/leaderboard_query.sql
cat docs/scenario.toml.example
```

**Narration**:
> "Results integrate with the AgentBeats leaderboard through GitHub repositories. Our DuckDB query displays coordination scores, graph metrics, and similarity measures, enabling transparent comparison of agent capabilities."

**Screen**:
- Show example leaderboard table
- Highlight sortable columns (coordination score, graph metrics)

### Closing (10 seconds)

**Visual**: Repository and documentation links

**Narration**:
> "GreenAgent provides quantitative graph analysis and qualitative behavioral assessment, revealing not just IF coordination occurred, but HOW effectively agents collaborate. Visit our repository for full documentation."

**Screen**:
- Show README.md with links
- Display docs/ directory structure
- Final frame: Repository URL

## Recording Tips

1. **Preparation**:
   - Test all commands before recording
   - Use clean terminal with clear font size
   - Prepare agents in advance to avoid startup delays
   - Have JSON files ready to cat

2. **Terminal Settings**:
   - Large font (14-16pt for readability)
   - High contrast color scheme
   - Clear prompt (short pwd, no clutter)
   - Record in 1920x1080 for clarity

3. **Narration**:
   - Speak clearly and at moderate pace
   - Emphasize key terms: "graph-based", "multi-tier", "reproducibility"
   - Keep technical level appropriate for judges
   - Practice timing to stay under 3 minutes

4. **Screen Recording**:
   - Use OBS Studio, QuickTime, or similar
   - Record terminal window only (not full desktop)
   - Add cursor highlighting if possible
   - Consider adding text overlays for key points

5. **Post-Production**:
   - Trim dead time (long pauses, errors)
   - Add timestamps if helpful
   - Include title slide and closing credits
   - Export at high quality (1080p, 60fps)

## Upload Instructions

Once recorded:

1. **Upload to YouTube** (recommended):
   - Create unlisted or public video
   - Title: "GreenAgent: Graph-Based Coordination Assessor - AgentBeats Demo"
   - Description: Include repository link and abstract
   - Tags: agentbeats, multi-agent, coordination, evaluation

2. **Alternative platforms**:
   - Vimeo
   - Google Drive (with public link)
   - Repository releases (if < 100MB)

3. **Update README.md**:
   - Replace placeholder with actual video URL
   - Verify link is publicly accessible
   - Test link in incognito mode

## Checklist

Before recording:
- [ ] All commands tested and working
- [ ] Terminal configured for readability
- [ ] Narration script reviewed
- [ ] Recording software tested
- [ ] Backup plan if demo fails

After recording:
- [ ] Video under 3 minutes
- [ ] Audio clear and understandable
- [ ] All three evaluation tiers demonstrated
- [ ] Results interpretation shown
- [ ] Uploaded and link is public
- [ ] README.md updated with video URL
