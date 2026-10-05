# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Decimal guess (`"50.9"`) | "Identify three potential edge case inputs (e.g., negative numbers, decimals, or extremely large values) that might still break my game." | `test_decimal_guess_is_not_truncated_to_a_win`: `ok, value, _ = parse_guess("50.9")`, then `assert not ok or value != 50` | No: fails on current code (`parse_guess` returns `(True, 50, None)`) | `int(float(raw))` truncates instead of rounding or rejecting, so `50.9` becomes `50` and counts as a win against a secret of 50. |
| Negative guess (`"-5"`) | Same prompt as above | `test_negative_guess_is_rejected`: `ok, _, _ = parse_guess("-5")`, then `assert ok is False` | No: fails on current code (`-5` is accepted) | `parse_guess` never checks the difficulty's range, so impossible guesses are accepted and use up an attempt. |
| Extremely large guess (`"99999999999999999999"`) | Same prompt as above | `test_huge_guess_is_rejected`: `ok, _, _ = parse_guess("99999999999999999999")`, then `assert ok is False` | No: fails on current code (the huge number is accepted) | There is no upper bound, so an absurd value is accepted and costs the player an attempt, which hurts most on Hard's 5-attempt limit. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
