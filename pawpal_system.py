from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    description: str
    time: str  # "HH:MM" format
    frequency: str  # "daily", "weekly", "once"
    pet_name: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        self.completed = True
        if self.frequency == "daily":
            self.due_date = date.today() + timedelta(days=1)
            self.completed = False
        elif self.frequency == "weekly":
            self.due_date = date.today() + timedelta(weeks=1)
            self.completed = False

    def __repr__(self):
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.time} - {self.description} ({self.frequency}) [{self.pet_name}]"


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def __repr__(self):
        return f"Pet({self.name}, {self.species}, {len(self.tasks)} tasks)"


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def get_all_tasks(self):
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def __repr__(self):
        return f"Owner({self.name}, {len(self.pets)} pets)"


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self):
        return self.owner.get_all_tasks()

    def sort_by_time(self):
        tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None):
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name:
            tasks = [t for t in tasks if t.pet_name.lower() == pet_name.lower()]
        return tasks

    def detect_conflicts(self):
        tasks = self.get_all_tasks()
        conflicts = []
        seen = {}
        for task in tasks:
            if task.time in seen:
                conflicts.append((seen[task.time], task))
            else:
                seen[task.time] = task
        return conflicts

    def print_schedule(self):
        sorted_tasks = self.sort_by_time()
        print(f"\n📅 Today's Schedule for {self.owner.name}:")
        print("-" * 45)
        if not sorted_tasks:
            print("  No tasks scheduled.")
        for task in sorted_tasks:
            print(f"  {task}")

        conflicts = self.detect_conflicts()
        if conflicts:
            print("\n⚠️  Conflicts Detected:")
            for t1, t2 in conflicts:
                print(f"  {t1.description} & {t2.description} both at {t1.time}")
        print("-" * 45)