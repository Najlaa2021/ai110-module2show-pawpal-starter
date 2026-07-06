# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial design for PawPal+ centers on a small logic layer with four main classes: Owner, Pet, Task, and DailyPlan.
- The Owner represents the person using the app and manages the pets they care for. The Pet represents an individual animal and holds its profile and care tasks. The Task represents a single care activity such as a walk, meal, medication, or grooming session. The DailyPlan collects the tasks chosen for a specific day and will eventually produce a schedule.
- The three core actions a user should be able to perform are:
  - Add a pet to their account.
  - Create or edit a care task for a pet, such as scheduling a walk.
  - Review today's tasks or the generated daily plan.

**b. Design changes**

- I kept the first version intentionally simple so the design would stay focused on the core domain objects and their relationships.
- I reviewed the class skeleton and noticed that a task should clearly belong to a specific pet, rather than only being stored inside a pet list. That led me to add an explicit pet reference on the Task class so the ownership is easier to understand and later use in scheduling logic.
- I chose to make Task and Pet data-oriented objects with small methods so the logic layer stays clear and easy to test as the app grows.
- The main building blocks I identified are:
  - Owner: attributes include name, availability minutes, preferred time window, and a list of pets; methods include adding/removing pets and creating a daily plan.
  - Pet: attributes include name, species, age, preferences, and a list of tasks; methods include adding/removing tasks and updating preferences.
  - Task: attributes include title, duration, priority, category, scheduled time, and completion status; methods include marking a task complete, rescheduling it, and updating its priority.
  - DailyPlan: attributes include the owner, a date, and a list of tasks; methods include adding tasks, sorting them, generating a schedule, and explaining the plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers task timing, task duration, priority, and whether a task is completed or still pending.
- I chose these constraints because they are simple to model, easy to explain to a user, and enough to create a useful first version of a pet-care planner.
- I treated time and priority as the most important factors because they directly affect whether a plan is understandable and practical for a busy owner.

**b. Tradeoffs**

- One tradeoff in the current scheduler is that it only detects conflicts when two tasks share the exact same scheduled time, rather than when their time ranges overlap.
- I kept this approach because it makes the conflict check easier to read and explain, even though it is less precise than a full interval-overlap check.
- For this starter version, that tradeoff is reasonable because it stays fast, simple, and suitable for a small pet-care scheduling app.

---

## 3. AI Collaboration

**a. How you used AI**

- I used my AI coding assistant for design brainstorming, generating test ideas, refining the class structure, and explaining unfamiliar code patterns.
- The most helpful prompts were specific ones that asked for a test plan, a refactoring suggestion, or a comparison between a simple and a more advanced implementation.
- I also used the assistant to help write clearer docstrings and improve the readability of the scheduling methods.

**b. Judgment and verification**

- One AI suggestion I did not accept as-is was a more compact version of the conflict-checking logic because it was elegant but less clear for a beginner-friendly project.
- I kept the more explicit version because it is easier for a human reader to follow and explain.
- I verified AI suggestions by running the test suite and the CLI demo, which confirmed whether the proposed idea actually improved behavior rather than just appearing more concise.

---

## 4. Testing and Verification

**a. What you tested**

- I tested sorting behavior, recurring task creation, conflict detection, task completion, and filtering by pet and completion status.
- These tests were important because they cover the core features that make the scheduler useful rather than just checking basic object creation.

**b. Confidence**

- I am moderately confident that the current scheduler works well for its intended scope because the automated tests and CLI demo both passed.
- If I had more time, I would test edge cases like unscheduled tasks, overlapping time ranges with durations, and a pet with no tasks.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with how the backend logic, UI, and tests now work together as a coherent system rather than as disconnected pieces.
- The scheduler feels simple, readable, and usable, which made the project feel complete.

**b. What you would improve**

- In a future iteration, I would improve the scheduling logic to handle overlapping durations more realistically instead of only checking exact time matches.
- I would also add a more polished task-editing experience in the UI.

**c. Key takeaway**

- One important lesson was that the human still needs to act as the lead architect: AI can generate suggestions quickly, but it is the developer’s job to decide what fits the project’s goals, keep the design clean, and verify the result.
