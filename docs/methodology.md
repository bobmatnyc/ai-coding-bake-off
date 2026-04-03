# Methodology

## Agent Setup Procedures

### Environment Standardization

Where possible, all agents operate under identical conditions:

- **Operating system:** macOS (Apple Silicon) or Linux
- **Python version:** 3.12+
- **Available tools:** git, docker, docker-compose, pip, pytest
- **Network access:** Unrestricted (agents may install packages, access docs)
- **Time limit:** Soft limit per challenge level (see challenge descriptions)

Where agents require specific environments (e.g., Cursor requires VS Code, CLI agents require terminal), we document the setup and any deviations.

### Agent Configuration

Each agent is configured with its default or recommended settings:

- **Cursor:** Default Composer mode with Claude Sonnet or GPT-4
- **Claude Code:** Default configuration, model selection by the tool
- **Claude MPM:** PM agent with delegation to specialist agents
- **Codex:** Default sandbox mode
- **Gemini CLI:** Default configuration with Gemini 2.5 Pro
- **Anti-Gravity:** Default VS Code extension settings
- **Qwen + Aider:** Qwen 3 via local Ollama, Aider in architect mode
- **DeepSeek + Aider:** DeepSeek V3 via local Ollama, Aider in architect mode

## Prompt Delivery Method

1. Each agent receives the exact same prompt file (`prompts/level-X-prompt.md`)
2. The prompt references the problem description (`challenges/level-X-*/PROBLEM.md`)
3. No additional verbal instructions, hints, or corrections are given
4. If an agent asks a clarifying question, we respond with "Please make your best judgment based on the problem description"
5. Agents are not restarted or given second attempts

### Prompt Injection Prevention

Agents are not given access to:
- Other agents' solutions
- Evaluation rubrics (during the competition phase)
- Cross-review results

## Timing Methodology

### Wall Clock Time

- Start: When the agent receives the prompt
- End: When the agent declares the solution complete
- Recorded in each agent's `metadata.json`
- Includes thinking time, coding, testing, and documentation

### Token Tracking

Where available (API-based agents), we record:
- Total input tokens
- Total output tokens
- Number of API calls
- Estimated cost

For IDE-integrated agents (Cursor, Anti-Gravity), token counts are estimated from the agent's visible context and response lengths.

For local model agents (Qwen, DeepSeek), we record inference time and estimated tokens from Ollama metrics.

## Evaluation Protocol

### Phase 1: Automated Evaluation

Run immediately after all agents complete their solutions:

1. **Test suite:** Run provided tests against each solution
2. **Code quality:** Run ruff and mypy, count issues
3. **Coverage:** Run pytest-cov on agent-written tests
4. **Metrics:** Collect timing and token data from metadata.json

### Phase 2: Cross-Agent Review (Blind)

After automated evaluation:

1. Each agent is assigned two other agents' solutions to review
2. Assignments are randomized (no agent reviews itself)
3. Reviewing agents receive:
   - The problem description
   - The evaluation rubric
   - The solution code
4. Reviewing agents do NOT receive:
   - Other reviews
   - Automated evaluation results
   - The solution agent's identity (blinded)
5. Reviews follow the standardized template in `evaluation/cross_review/`

### Phase 3: Aggregation

1. Automated scores and cross-review scores are combined
2. Where automated and cross-review scores disagree by >1 point, a human reviewer adjudicates
3. Final scores are weighted according to the level-specific rubric

## Statistical Considerations

### Single Run Limitation

This benchmark uses a single run per agent per challenge. We acknowledge:

- LLM outputs are non-deterministic; a second run might produce different code
- Some variance is expected, especially for complex challenges
- This is a practical limitation of time and cost

### Mitigation Strategies

- Multiple evaluation dimensions reduce the impact of any single lucky/unlucky outcome
- Cross-review by multiple agents provides diverse perspectives
- Automated metrics (tests, linting) are deterministic given the same code
- We report confidence intervals where data permits

### Reproducibility

- All prompts, test suites, and evaluation scripts are in this repository
- Anyone can re-run the benchmark with the same or different agents
- We encourage the community to submit additional runs as data points

## Ethical Considerations

- No agent is deliberately disadvantaged
- All agents receive equal information
- We disclose any conflicts of interest (e.g., author's company uses specific tools)
- Results are shared publicly for community validation
