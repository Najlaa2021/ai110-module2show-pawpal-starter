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
- Let a user add and edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly and explain the reasoning behind the ordering
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

Run the automated test suite with:

```bash
python -m pytest
```

These tests cover the core scheduler behaviors, including task sorting, recurring task creation, conflict detection, task completion, filtering by pet and status, JSON persistence, and next-available-slot logic.

Successful test run output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/queen/ai110-module2show-pawpal-starter
collected 10 items

tests/test_pawpal.py ..........                                            [100%]

============================== 10 passed in 0.02s
```

Confidence Level: ★★★★★

## 💾 Data Persistence

PawPal+ saves pets and tasks to `data.json` so your data persists between app runs.

- `pawpal_system.py` implements `Owner.save_to_json(path)` and `Owner.load_from_json(path)`.
- `app.py` loads saved state from `data.json` on startup and writes updates back whenever pets or tasks change.

This means pets, task details, priorities, frequencies, and completion state are preserved across restarts.

## 📐 Smarter Scheduling

The scheduler now includes more advanced intelligence for everyday pet-care planning:

- Priority scheduling: `Scheduler.sort_by_priority_then_time()` orders tasks by priority first, then by scheduled time.
- Time-based sorting: `Scheduler.sort_by_time()` still provides a chronological fallback view.
- Conflict detection: `Scheduler.detect_conflicts()` warns when two tasks share the same scheduled time.
- Recurring task logic: `Task.mark_complete_and_schedule_next()` creates the next daily or weekly occurrence after completion.
- Next available slot: `Scheduler.find_next_available_slot()` locates the earliest free window for a given duration inside the owner's availability window.

## 🎬 Demo Walkthrough

PawPal+ is designed as a simple, human-friendly pet-care planning tool. A user can add pets, create tasks, and generate a day plan without needing to understand the full scheduling engine behind the scenes.

1. Open the Streamlit app and enter an owner name.
2. Add one or more pets to the profile, then create care tasks such as feeding, walks, grooming, or medication.
3. Use the schedule view to generate a sorted plan for the day. The app shows pending tasks in chronological order and highlights any time-slot conflicts.
4. Mark recurring tasks as complete to create the next daily or weekly follow-up automatically.
5. Review the generated schedule in a table, filter it by pet, and use the warnings to adjust overlapping tasks.

### Example workflow

Add a pet → create a feeding task → add a walk task → generate the schedule → review the sorted plan and any conflict warnings.

### Scheduler behaviors shown in the demo

- Sorting by time: tasks are ordered chronologically in the generated schedule.
- Conflict warnings: duplicate time slots are flagged clearly for the user.
- Daily recurrence: completing a recurring task creates the next occurrence automatically.
- Pet filtering: the schedule can be viewed for all pets or one specific pet.

### Sample CLI output

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
