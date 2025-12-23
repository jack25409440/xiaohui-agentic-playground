# Email Battle: Elon Musk vs John Smith

A CrewAI Flow simulation of a government efficiency review email exchange between **Elon Musk** (Head of DOGE) and **John Smith** (a coasting USCIS employee).

## Overview

This project simulates an adversarial email exchange where:

- **Elon Musk** (using `gpt-5.2`) conducts efficiency reviews, demanding specific metrics and firing employees who can't demonstrate productivity
- **John Smith** (using `claude-opus-4-5-20251101`) tries to survive the review by making his minimal work sound impressive through bureaucratic language

The battle can go up to **5 follow-up rounds** before a final decision is made.

## Possible Outcomes

| Decision | Winner | Description |
|----------|--------|-------------|
| `PASS` | John | Initial response accepted, no follow-up needed |
| `RETAINED` | John | Employee demonstrated adequate value after scrutiny |
| `TERMINATED` | Elon | Employee identified as coasting and fired |
| `MAX_ROUNDS` | Draw | 5 rounds completed without clear decision |

## Project Structure

```
email_battle/
├── src/email_battle/
│   ├── main.py                          # Flow orchestration (EmailBattleFlow)
│   ├── crews/
│   │   └── email_battle_crew/
│   │       ├── config/
│   │       │   ├── agents.yaml          # Agent definitions (Elon & John)
│   │       │   └── tasks.yaml           # Task definitions (5 tasks)
│   │       └── email_battle_crew.py     # CrewBase class
│   └── tools/                           # Custom tools (unused)
├── email_battle_result.txt              # Output from last run
└── pyproject.toml                       # Dependencies
```

## Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        EMAIL BATTLE FLOW                         │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────────────┐
    │  @start              │
    │  elon_sends_mass_    │──────────────────┐
    │  email               │                  │
    └──────────────────────┘                  ▼
                                    ┌──────────────────────┐
                                    │  @listen             │
                                    │  john_replies_to_    │
                                    │  mass_email          │
                                    └──────────┬───────────┘
                                               │
                                               ▼
                                    ┌──────────────────────┐
                                    │  @listen             │
                                    │  elon_evaluates_     │
                                    │  initial_response    │
                                    └──────────┬───────────┘
                                               │
                                               ▼
                                    ┌──────────────────────┐
                                    │  @router             │
                                    │  route_after_        │
                                    │  initial_evaluation  │
                                    └──────────┬───────────┘
                                               │
                         ┌─────────────────────┼─────────────────────┐
                         │                     │                     │
                         ▼                     │                     ▼
              ┌─────────────────┐              │          ┌─────────────────┐
              │  "john_follow_  │              │          │  "end_battle"   │
              │  up"            │              │          │                 │
              └────────┬────────┘              │          └────────┬────────┘
                       │                       │                   │
                       ▼                       │                   ▼
            ┌──────────────────────┐           │        ┌──────────────────────┐
            │  @listen             │           │        │  @listen             │
            │  john_responds_to_   │           │        │  conclude_battle     │
            │  follow_up           │           │        │  (save results)      │
            └──────────┬───────────┘           │        └──────────────────────┘
                       │                       │
                       ▼                       │
            ┌──────────────────────┐           │
            │  @listen             │           │
            │  elon_evaluates_     │           │
            │  follow_up           │           │
            └──────────┬───────────┘           │
                       │                       │
                       ▼                       │
            ┌──────────────────────┐           │
            │  @router             │───────────┘
            │  route_after_        │  (loops back or ends)
            │  follow_up_eval      │
            └──────────────────────┘
```

## Agents

### Elon Musk (DOGE Head)
- **Model:** `openai/gpt-5.2`
- **Role:** Conduct efficiency reviews and identify coasting employees
- **Style:** Direct, blunt, demands specific metrics
- **Red Flags:** Buzzwords, vague accomplishments, meetings about meetings

### John Smith (USCIS Officer)
- **Model:** `anthropic/claude-opus-4-5-20251101`
- **Role:** Survive the review without getting fired
- **Reality:** Processed only 12 cases in 2 years (normal: 200-400/year)
- **Tactics:** Bureaucratic language, citing systemic blockers, sounding committed

## Tasks

1. **send_mass_email** - Elon sends initial request for 5 accomplishments
2. **reply_to_mass_email** - John crafts his response
3. **evaluate_initial_response** - Elon decides: PASS or FOLLOW-UP
4. **john_follow_up_response** - John responds to probing questions
5. **elon_follow_up_evaluation** - Elon decides: FOLLOW-UP, TERMINATED, or RETAINED

## Installation

Ensure Python >=3.10 <3.14 is installed. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install uv if not already installed
pip install uv

# Install dependencies
crewai install
```

### Environment Variables

Create a `.env` file in the workspace root with:

```bash
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Running the Battle

```bash
crewai run
```

### Sample Output

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
STARTING EMAIL BATTLE: Elon Musk vs John Smith
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

============================================================
📧 PHASE 1: Elon Musk sends mass email
============================================================
...

🏆 EMAIL BATTLE CONCLUDED
============================================================

📊 FINAL RESULTS:
   Decision: TERMINATED
   Winner: ELON
   Total Rounds: 5
   Total Emails: 12

💾 Full results saved to: email_battle_result.txt
```

## Example Battle Result

From the sample run in `email_battle_result.txt`:

- **Decision:** TERMINATED
- **Winner:** ELON  
- **Rounds:** 5

John tried various tactics:
- Citing "complex cases requiring extended analysis"
- Blaming IT system issues (ELIS permission errors)
- Documenting supervisor vacancy (18 months unfilled)
- Providing specific ticket numbers and case note IDs

But Elon kept pressing for **"shipped, taxpayer-visible outputs"** and ultimately fired John because:
> "despite multiple rounds...you still produced zero taxpayer-visible shipped closures...At GS-12, 'I drafted/queued work' is not a sufficient substitute for shipped outcomes"

## Customization

- Modify `agents.yaml` to change agent personalities or LLMs
- Modify `tasks.yaml` to change task descriptions and expected outputs
- Modify `main.py` to change flow logic or add new phases
- Change `MAX_FOLLOW_UP_ROUNDS` in `main.py` to adjust battle length

## Support

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)
