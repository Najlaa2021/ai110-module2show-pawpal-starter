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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
