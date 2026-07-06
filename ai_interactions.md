# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI assistant to implement JSON persistence for owner/pet/task data, add advanced priority-based scheduling, and connect those features into the Streamlit UI.

**What did the agent do?**

- Updated `pawpal_system.py` with `Owner.save_to_json()` and `Owner.load_from_json()`.
- Added `Task.to_dict()` / `Task.from_dict()` and `Pet.to_dict()` / `Pet.from_dict()` for JSON serialization.
- Added `Scheduler.sort_by_priority_then_time()` and `Scheduler.find_next_available_slot()`.
- Updated `app.py` to load saved state from `data.json`, persist changes after adding pets/tasks, and expose a next-available-slot lookup.
- Updated the test suite and README to document the new features.

**What did you have to verify or fix manually?**

- I verified the new persistence logic with unit tests and by checking that `data.json` can round-trip owner data.
- I fixed a syntax issue in `app.py` where the task form block had malformed indentation after patching UI logic.
- I adjusted one test expectation for the next available slot behavior to match the intended algorithm.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Same AI coding assistant | Same AI coding assistant |
| **Prompt** | "Implement JSON persistence for Owner/Pet/Task objects and connect it to the Streamlit app." | "Improve scheduling by adding priority-first sorting and a next available slot finder." |
| **Response summary** | Provided a JSON serialization design using `to_dict()`/`from_dict()` methods and file I/O helpers. | Suggested priority-aware sorting and a helper to find the next free block within availability. |
| **What was useful** | The persistence design was practical and fit the current object model without requiring third-party libraries. | The scheduling enhancement matched the rubric and added a valuable advanced feature quickly. |
| **Problems noticed** | The initial UI patch left a broken task form block, which required manual syntax cleanup. | The first slot-finding implementation needed an expectation update to clarify the behavior of the earliest available time. |
| **Decision** | I used the persistence strategy in the final implementation because it was straightforward and robust. | I used the priority sorting and next-slot logic in the final implementation because it added a true advanced algorithmic capability. |

**Which approach did you use in your final implementation and why?**

I used both approaches: one prompt focused on persistence, and the other focused on advanced scheduling. This allowed me to build the required stretch features in separate, manageable steps while keeping the design clean and verifiable.
