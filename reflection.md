# PawPal+ Project Reflection

## 1. System Design

users can enter basic owner 
users can add pet info
users can add/edit tasks (duration + priority at minimum)

**a. Initial design**

My initial UML design centered on four classes that map directly to the real-world entities in the scenario: a pet owner, their pet, individual care tasks, and the daily schedule that organizes those tasks.

- **`CareTask`** — represents a single pet care activity (e.g., walk, feeding, medication). It holds the task title, how long it takes (`duration_minutes`), its `priority` level (low/medium/high), and an optional `reason`. It is responsible for knowing whether it can fit within a given time budget (`is_feasible`).
- **`Pet`** — stores the pet's basic info (name, species, age) and owns a list of `CareTask` objects. It is responsible for managing which tasks belong to that pet.
- **`Owner`** — stores the owner's name, how many minutes they have available in a day, and any preferences. It owns one or more `Pet` objects and is responsible for triggering schedule generation.
- **`Schedule`** — holds the ordered list of tasks that were selected for the day and tracks total time used. It is responsible for the scheduling logic (choosing and ordering tasks within the owner's constraints) and for explaining why each task was included.

**b. Design changes**

Yes, the design changed in three ways after reviewing the initial skeleton:

1. **`Priority` became an `Enum` instead of a plain string.** The original design used `"low"`, `"medium"`, `"high"` as strings, but string comparison doesn't produce a meaningful sort order. Switching to `Priority(Enum)` with integer values (LOW=1, MEDIUM=2, HIGH=3) makes it possible to sort tasks by priority reliably using `.value`.

2. **`Schedule` was given an `available_minutes` parameter.** The initial design had `Schedule` track tasks but with no knowledge of the time budget — that lived only in `Owner`. Since the scheduling logic (deciding what fits) belongs to `Schedule`, it needed direct access to the budget rather than relying on `Owner` to pass it in piecemeal.

3. **`Owner.get_all_tasks()` was added.** The original design had no way for `get_schedule()` to collect tasks across all of an owner's pets. This helper method fills that gap and keeps `get_schedule()` clean.

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
