# Article Outline: AI Coding Agent Bake-Off

**Working Title:** "AI Coding Agent Bake-Off: Benchmarking the Future of Software Engineering"  
**Subtitle:** "A follow-up to 'Orchestration Beats Raw Power'"  
**Author:** Bob Matsuoka, CTO @ Duetto  
**Target Length:** 4,000-6,000 words  
**Target Publication:** Engineering blog, LinkedIn, HackerNews

---

## 1. Introduction (500 words)

- Hook: "We gave 8 AI coding agents the same 5 challenges. The results surprised us."
- Link to original article "Orchestration Beats Raw Power"
- Why we did this: the AI tooling landscape is exploding and CTOs need data, not hype
- What this study covers: 8 agents, 5 challenges, blind cross-evaluation
- Preview of key finding: orchestration advantage grows with complexity

## 2. Methodology (600 words)

- Challenge design philosophy (open-ended, not LeetCode)
- Agent selection criteria (commercial, open-source, orchestrated, single-model)
- Evaluation framework: automated (tests, linting, coverage) + cross-review
- Prompt standardization: each agent gets the same prompt file
- Timing and token tracking methodology
- Statistical considerations: single run, acknowledging variance
- Reproducibility: everything in the repo, anyone can re-run

## 3. The Agents (800 words)

Profile each agent with:
- Tool description and model(s) used
- Orchestration approach (single-model, multi-agent, IDE-integrated)
- Setup and configuration for this benchmark
- Expected strengths and weaknesses

Agents: Cursor, Claude Code, Claude MPM, Codex, Gemini CLI, Anti-Gravity, Qwen+Aider, DeepSeek+Aider

## 4. Results by Level (1,200 words)

### Level 1-2: The Flat Zone
- All agents perform similarly on simple problems
- Table of scores
- Key insight: raw model quality matters less than tool ergonomics

### Level 3: The Divergence Point
- API integration separates agents that plan from those that code-and-fix
- Docker setup reveals architectural thinking
- First clear gap between orchestrated and single-model

### Level 4: Architecture Matters
- The extensibility requirement exposes agents that think in patterns
- Comparison of architecture decisions across agents
- Plugin systems: who achieved true open/closed principle?

### Level 5: The Crucible
- Full-stack challenge breaks most agents
- What each agent got right and wrong
- Partial completion analysis: what did they prioritize?

## 5. Architecture Deep Dive: Level 4 Comparison (600 words)

- Side-by-side comparison of pipeline architectures
- Code examples from 3-4 agents showing different approaches
- Which designs would survive adding a new processing stage?
- Mermaid diagrams comparing architectures

## 6. Failure Analysis: Level 5 Breakdown (500 words)

- What failed first for each agent?
- Common failure modes: Docker config, WebSocket, auth flow
- Time budget analysis: where agents spent their time
- Partial completion scoring: how to credit unfinished work

## 7. Cost-Benefit Analysis (400 words)

- Quality vs. tokens vs. time scatter plot
- Cost per quality point by agent
- When does paying more for a better agent pay off?
- The 80/20 rule: diminishing returns at high complexity

## 8. Local Models: Can Open Source Compete? (400 words)

- Qwen+Aider and DeepSeek+Aider results
- Where local models hold up (L1-2) and where they fall behind (L4-5)
- Cost advantage analysis
- Privacy and IP considerations for enterprise

## 9. Conclusions (400 words)

- **Finding 1:** Orchestration advantage is real and grows with complexity
- **Finding 2:** All agents handle simple tasks well; differentiation happens at L3+
- **Finding 3:** Architecture quality is the biggest predictor of Level 4-5 success
- **Finding 4:** Local models are viable for routine work
- Recommendations for engineering leaders choosing AI tools
- What this means for the future of software engineering

## 10. Appendix

- Full rubric scores for all agents across all levels
- Raw data tables
- Methodology details
- How to reproduce the benchmark
- Link to repository

---

## Figures

1. Overall comparison radar chart (one axis per agent)
2. Score by level line chart (showing divergence)
3. Cost vs. quality scatter plot
4. Time allocation bar chart (how agents spent their time)
5. Architecture comparison diagram (Level 4)
6. Completion waterfall (Level 5 --- what each agent finished)
