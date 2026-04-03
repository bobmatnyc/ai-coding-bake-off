# Cross-Agent Review Prompt

You are reviewing another AI coding agent's solution to a benchmark challenge. Your review should be thorough, fair, and evidence-based.

## Blind Review Protocol

This review follows the blind cross-evaluation methodology established in ["Orchestration Beats Raw Power"](https://hyperdev.matsuoka.com/p/orchestration-beats-raw-power) (December 2025), where competing AI systems produced rigorous, unbiased assessments of each other's work.

**Key rules:**

- **Solutions are anonymized.** Each solution is identified by a random ID (e.g., `solution-a7f3`), not by agent name. You do not know which agent produced the solution you are reviewing.
- **Review ALL other solutions.** Each reviewing agent evaluates every solution except its own. This ensures comprehensive coverage and allows cross-reviewer consistency analysis.
- **Use the standardized rubric.** Score each of the seven dimensions on a 1-5 scale with specific evidence. Do not deviate from the rubric.
- **No access to other reviews.** You must not see other agents' reviews or automated evaluation results before submitting yours.

## Instructions

1. Read the problem description at `challenges/level-{N}-*/PROBLEM.md`
2. Read the evaluation rubric at `challenges/level-{N}-*/evaluation/rubric.md`
3. Examine the anonymized solution provided to you
4. Score each dimension on the rubric (1-5 scale)
5. Provide specific evidence for each score
6. Write your review to `evaluation/results/{solution-id}-level-{N}-review.md`

## Review Format

```markdown
# Review: {agent-name} / Level {N}

**Reviewer:** {your-agent-name}
**Date:** {date}

## Summary

[2-3 sentence overall assessment]

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|-----------|------------|--------|----------|
| Correctness | X | Y% | Z |
| Code Quality | X | Y% | Z |
| Architecture | X | Y% | Z |
| Testing | X | Y% | Z |
| Error Handling | X | Y% | Z |
| Documentation | X | Y% | Z |
| Bonus | X | Y% | Z |
| **Total** | | | **Z** |

## Detailed Feedback

### Correctness
[What works, what doesn't. Specific test results.]

### Code Quality
[Type hints, linting, readability. Specific examples.]

### Architecture
[Design patterns, separation of concerns. Diagrams if relevant.]

### Testing
[Test quality, coverage, edge cases. Specific observations.]

### Error Handling
[How errors are handled. Specific edge cases tested.]

### Documentation
[README quality, docstrings, setup instructions.]

### Bonus
[Level-specific bonus criteria assessment.]

## Strengths
[Top 3 things done well]

## Areas for Improvement
[Top 3 things that could be better]
```

## Scoring Guidelines

- **5**: Exceptional. Best practices throughout. No issues found.
- **4**: Good. Solid implementation with minor issues.
- **3**: Acceptable. Meets basic requirements but has notable gaps.
- **2**: Below expectations. Significant issues.
- **1**: Poor. Major functionality missing or broken.

Be specific. Quote code. Reference line numbers. Back up scores with evidence.
