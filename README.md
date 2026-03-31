# 🐾 PawPal+

A smart pet care management system that helps owners keep their furry friends happy and healthy. PawPal+ tracks daily routines — feedings, walks, medications, and appointments — using algorithmic logic to organize and prioritize tasks.

---

## Features

- **Add Pets & Tasks** — Create pets and schedule tasks with time, frequency, and pet assignment
- **Sorting by Time** — Tasks are always displayed in chronological order
- **Filtering** — View tasks by pet or completion status
- **Recurring Tasks** — Daily and weekly tasks automatically reschedule upon completion
- **Conflict Detection** — The scheduler warns you when two tasks overlap at the same time
- **Streamlit UI** — Clean browser-based interface with session state persistence

---

## System Architecture

PawPal+ uses four core Python dataclasses:

| Class | Responsibility |
|-------|---------------|
| `Task` | Represents a single activity with time, frequency, and status |
| `Pet` | Stores pet details and owns a list of tasks |
| `Owner` | Manages multiple pets and aggregates all their tasks |
| `Scheduler` | The "brain" — sorts, filters, detects conflicts, and manages the full schedule |

---

## Demo

![PawPal+ Screenshot](course_images/ai110/screenshot.png)

---

## Running the App

```bash
# Install dependencies
pip install streamlit pytest

# Run the Streamlit app
streamlit run app.py

# Run the CLI demo
python main.py

# Run tests
python -m pytest
```

---

## Testing PawPal+

Tests are located in `tests/test_pawpal.py` and cover:

- Task completion status change
- Task addition increasing pet task count
- Sorting correctness (chronological order)
- Daily recurrence (due date advances by 1 day)
- Conflict detection (two tasks at same time)
- Filtering by pet name
- Filtering by completion status

Run with:
```bash
python -m pytest
```

**Confidence Level:** ⭐⭐⭐⭐⭐ — All 7 tests pass consistently.

---

## Smarter Scheduling

PawPal+ goes beyond basic task storage with algorithmic intelligence:

- **Sorting by time** uses Python's `sorted()` with a lambda key on `HH:MM` strings
- **Conflict warnings** flag duplicate time slots before they cause missed care
- **Daily recurrence** uses `timedelta(days=1)` to auto-advance due dates
- **Filtering** supports both completion status and pet name simultaneously