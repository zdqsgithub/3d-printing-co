# RALPH Loop Evaluation — 3D Printing Co AI Agent Skills

## Process

**R**eview → **A**djust → **L**oop → **P**olish → **H**alt

```
RALPH Cycle:
  1. REVIEW  — Run test_specs.py + agent_judge.py → identify failures
  2. ADJUST  — Fix failing skills (spec gaps, script bugs, prompt issues)
  3. LOOP    — Re-run full evaluation suite
  4. POLISH  — Refine prompts, add edge cases, improve formatting
  5. HALT    — Stop when ALL skills score ≥ 4.0/5.0 average
```

## Cycle Log

### Cycle 1 — Initial Build (Feb 24, 2026)

**Status**: 🔄 Running

| Check | Result | Notes |
|-------|:------:|-------|
| SKILL.md structure (9/9) | ⬜ | Pending test run |
| Script syntax (8/8) | ⬜ | Pending test run |
| Resource validation (2/2) | ⬜ | Pending test run |
| Agent-as-Judge avg ≥ 4.0 | ⬜ | Pending evaluation |

**Adjustments Made**: N/A (initial build)

**Decision**: ⬜ Continue / ⬜ Halt

---

## Evaluation Commands

```bash
# Step 1: Run structural + functional tests
cd z:\Users\ZDQsm\Desktop\_Desktop_Organization\3d-printing-co
python -m pytest tests/test_specs.py -v --tb=short

# Step 2: Run Agent-as-Judge evaluation
python tests/agent_judge.py --all --threshold 4.0

# Step 3: Check specific skill
python tests/agent_judge.py --skill product-recommender

# Step 4: View rubric
python tests/agent_judge.py --rubric
```

## Quality Gates

| Gate | Criteria | Status |
|------|----------|:------:|
| G1: Structure | All 9 SKILL.md files pass frontmatter validation | ⬜ |
| G2: Syntax | All 8 helper scripts compile without errors | ⬜ |
| G3: Resources | catalog.json + faq_knowledge_base.json are valid | ⬜ |
| G4: Help | All scripts accept --help without crashing | ⬜ |
| G5: Judge Avg | Agent-as-Judge average ≥ 4.0/5.0 | ⬜ |
| G6: No Fails | Zero individual skill scores below 3.5 | ⬜ |
