# PawPal+ Reflection

## System Design

### 1a. Initial Design

For PawPal+, I identified four core classes that map directly to the real-world problem:

- **Task** — Represents a single pet care activity. It holds a description, scheduled time (HH:MM), frequency (daily/weekly/once), which pet it belongs to, and a completion status. I chose a dataclass because the data-centric structure is clean and readable.
- **Pet** — Stores a pet's name and species, and owns a list of Task objects. The Pet class is responsible for holding and returning its own tasks, which keeps concerns separated.
- **Owner** — Acts as the top-level container. It holds multiple Pet objects and provides a single method to aggregate all tasks across pets, which the Scheduler relies on.
- **Scheduler** — This is the "brain." It doesn't own any data but operates on the Owner's data to provide sorting, filtering, conflict detection, and schedule printing.

The three core user actions I identified were: add a pet, schedule a task, and view today's schedule sorted by time.

### 1b. Design Changes

After scaffolding the skeletons, I added `pet_name` as a field on `Task` directly rather than relying on traversal. This made filtering by pet much simpler without having to walk the object graph every time. I also moved conflict detection into the `Scheduler` instead of `Owner`, since scheduling logic belongs in the scheduler, not the data container.

---

## Algorithmic Layer

### 2a. Sorting & Filtering

For sorting, I used Python's built-in `sorted()` with a lambda: `key=lambda t: t.time`. Since times are in consistent `HH:MM` string format, lexicographic sorting correctly produces chronological order. This was suggested by Copilot when I asked about sorting string times, and it was cleaner than converting to `datetime` objects for this use case.

For filtering, I implemented a method that accepts optional keyword arguments (`completed`, `pet_name`) and chains conditions. This approach is flexible — you can filter by one or both simultaneously.

### 2b. Tradeoffs

One key tradeoff in conflict detection: I check for exact time string matches (e.g., both at `"08:00"`), not overlapping time *windows*. This means a 30-minute task starting at 8:00 and one starting at 8:15 won't be flagged. For a real app, you'd want duration-aware conflict checking, but for this scope, exact-match is simple and reliable.

Another tradeoff: recurring tasks reset immediately on `mark_complete()` rather than waiting until the new due date arrives. This keeps the logic simple but means a "daily" task shows as pending again instantly rather than the next day.

---

## AI Strategy

### Copilot Features Used

- **Agent Mode** — Used to flesh out all four class implementations in `pawpal_system.py` from my UML skeleton. This was the most effective feature because it could see the full file context and generate cohesive code.
- **Inline Chat** — Used on specific methods like `sort_by_time()` to ask targeted questions like "how do I sort these task objects by their HH:MM string time?" This kept the changes scoped to one method without regenerating the whole file.
- **Generate Tests** — Used to draft the initial pytest functions in `test_pawpal.py`. I then reviewed each test to make sure it was actually testing meaningful behavior, not just that the function runs.
- **Generate Documentation** — Used to add docstrings to methods in `pawpal_system.py` after implementation.

### AI Suggestion I Modified

Copilot initially suggested converting `HH:MM` strings to `datetime.time` objects for sorting. I kept the lambda-on-string approach instead because my time values are always zero-padded and consistent — the extra conversion would add complexity without benefit for this scope.

### Separate Chat Sessions

Using separate Copilot chat sessions for different phases (design vs. implementation vs. testing) helped a lot. Each session stayed focused — the testing session didn't get confused by design-phase context, and Copilot's suggestions stayed relevant to the current task.

### Being the Lead Architect

The most important lesson was that AI is a powerful *implementer* but a poor *decision-maker*. Copilot could generate sorting code instantly, but it didn't know whether to sort in the Scheduler or the Owner — that was an architectural decision I had to make. Being the lead architect meant setting the structure, asking precise questions, and evaluating AI output critically rather than accepting it wholesale.