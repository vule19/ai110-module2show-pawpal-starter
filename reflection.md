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

The scheduler considers two constraints: **time** (the owner's `available_minutes` for the day) and **task priority** (HIGH, MEDIUM, or LOW). Tasks are sorted highest priority first, and within the same priority level, shorter tasks are preferred so more tasks can fit into the available time.

Time was treated as the hard constraint — a task simply cannot be scheduled if it doesn't fit in the remaining minutes. Priority was treated as the ordering rule — it determines which tasks get first access to that time budget. I decided these two mattered most because they directly reflect the scenario: a busy owner with limited time who still needs critical care tasks done no matter what.

**b. Tradeoffs**

The scheduler uses a **greedy algorithm** — it picks the best-looking task at each step without backtracking. This means it can miss an optimal combination: for example, one HIGH priority 60-minute task might block three MEDIUM priority 20-minute tasks that together would cover more of the pet's needs.

This tradeoff is reasonable here because pet care tasks are not interchangeable — a high-priority medication task genuinely should take precedence over lower-priority enrichment activities, even if a smarter algorithm could technically fit more tasks in. Simplicity and predictability matter more than perfect optimization for a daily care planner.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used throughout the project for design brainstorming, code generation, and catching gaps in the system. The most useful prompts were specific and structural — for example, asking the AI to review the class skeleton for missing relationships or logic bottlenecks produced concrete, actionable findings (like the missing `get_all_tasks()` method and the unworkable string-based priority comparison). Asking AI to explain *why* a change was needed, not just what to change, helped build understanding rather than just copying output.

**b. Judgment and verification**

When AI suggested adding `available_minutes` to `Schedule.__init__`, I did not accept this blindly — I traced through the scheduling flow manually to confirm that `get_schedule()` in `Owner` was the right place to pass that value, and that `Schedule` actually needed it to enforce `is_feasible` correctly against remaining time rather than total time. Verifying the data flow between `Owner`, `Schedule`, and `CareTask` prevented a subtle bug where feasibility would have been checked against the full budget instead of the shrinking remainder.

---

## 4. Testing and Verification

**a. What you tested**

Two behaviors were tested:

1. **Task completion** — that calling `mark_complete()` on a `CareTask` changes `completed` from `False` to `True`. This matters because if the flag doesn't flip, any future feature that filters completed tasks (e.g., skipping already-done tasks when regenerating a schedule) would silently break.

2. **Task addition** — that calling `add_task()` on a `Pet` actually increases the pet's task count. This is the foundation of the whole system: if tasks aren't stored correctly, the scheduler has nothing to work with.

**b. Confidence**

I'm confident the scheduler handles the normal case correctly — tasks are sorted by priority, fit-checked against remaining time, and added in order. The main edge cases I would test next given more time are: scheduling with zero available minutes (expect empty schedule), all tasks having the same priority (expect shortest-first ordering), and an owner with no pets (expect empty schedule without errors).

---

## 5. Reflection

**a. What went well**

The class design held up well throughout implementation. Starting from a UML diagram made it easy to catch structural problems — like the missing link between `Schedule` and the time budget — before writing any logic. The four-class split kept each file section focused and made the Streamlit integration straightforward, since `app.py` only needed to call `owner.get_schedule()` to get a result it could display.

**b. What you would improve**

I would add a `time_of_day` or `start_time` field to `CareTask` so the schedule produces an actual timed plan (e.g., "Walk at 8:00 AM, feeding at 8:30 AM") rather than just an ordered list. I would also allow tasks to be marked as recurring or one-time, so the owner doesn't have to re-enter the same tasks every day.

**c. Key takeaway**

Designing the system on paper first — even just a rough class diagram — made every implementation step faster and more confident. Without the UML, I would have discovered the missing `get_all_tasks()` method and the `Priority` sorting problem only after writing broken code. Working with AI is most effective when you use it to stress-test a design you already understand, not as a substitute for understanding the design yourself.