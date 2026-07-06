# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

The CLI demo script produces a readable daily schedule in the terminal:

```text
Sorted tasks:
- 08:30 — Feeding (10 min)
- 08:30 — Grooming (20 min)
- 09:00 — Morning walk (30 min)
- 10:00 — Daily meds (5 min)

Pending tasks for Mochi:
- Feeding
- Morning walk

Conflicts:
- Conflict: Feeding and Grooming are both scheduled at 08:30.

Recurring follow-up:
- Created Daily meds for Biscuit
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/queen/ai110-module2show-pawpal-starter
collected 2 items

tests/test_pawpal.py ..                                                  [100%]

============================== 5 passed in 0.01s ===============================
```

## 📐 Smarter Scheduling

The scheduler now includes lightweight intelligence for everyday pet-care planning:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks by scheduled time so the plan reads clearly. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by pet name and completion state. |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns when two tasks share the same scheduled time. |
| Recurring tasks | `Task.mark_complete_and_schedule_next()` | Creates the next daily or weekly occurrence after completion. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
