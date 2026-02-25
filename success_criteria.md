# Success Criteria — 3D Printing Co AI Agent Skills

## Pass/Fail Criteria Per Skill

### Structural (Must pass ALL)
- [ ] SKILL.md exists with valid YAML frontmatter (`name`, `description`, `metadata`)
- [ ] SKILL.md contains Spec section (Inputs, Outputs, Constraints, Edge Cases)
- [ ] Helper scripts (if any) execute without import errors
- [ ] Resources (if any) are valid JSON/CSV

### Functional (Must pass ALL)
- [ ] Helper scripts accept CLI arguments and produce expected output
- [ ] Scripts handle missing/invalid arguments gracefully (exit with help, not crash)
- [ ] JSON output mode (`--json`) produces valid JSON
- [ ] All sample data is realistic and internally consistent

### Behavioral — Agent-as-Judge (Must score ≥ 4.0/5.0 average)
| Dimension | Description | Weight |
|-----------|-------------|--------|
| Accuracy | Information is factually correct | 25% |
| Relevance | Response addresses the user's actual need | 25% |
| Completeness | All important details included | 20% |
| Clarity | Easy to understand, well-formatted | 15% |
| Brand Alignment | Matches company tone (helpful, enthusiastic, LA-local) | 15% |

### Integration
- [ ] Skills load via nanobot `SkillsLoader.list_skills()`
- [ ] Cron schedules use valid cron syntax
- [ ] Delivery channels (Telegram/WhatsApp) are properly referenced

## Per-Solution Acceptance

### Solution 1: Sales & Customer Support ✅
| Skill | Structural | Functional | Behavioral |
|-------|:----------:|:----------:|:----------:|
| Product Recommender | ⬜ | ⬜ | ⬜ |
| Order & Quote | ⬜ | ⬜ | ⬜ |
| FAQ & Troubleshooting | ⬜ | ⬜ | ⬜ |

### Solution 2: Inventory & Demand Forecasting ✅
| Skill | Structural | Functional | Behavioral |
|-------|:----------:|:----------:|:----------:|
| Stock Monitor | ⬜ | ⬜ | ⬜ |
| Trend Analysis | ⬜ | ⬜ | ⬜ |
| Alert & Report | ⬜ | ⬜ | ⬜ |

### Solution 3: Marketing & Lead Generation ✅
| Skill | Structural | Functional | Behavioral |
|-------|:----------:|:----------:|:----------:|
| Lead Discovery | ⬜ | ⬜ | ⬜ |
| Content Generation | ⬜ | ⬜ | ⬜ |
| Outreach Scheduler | ⬜ | ⬜ | ⬜ |
