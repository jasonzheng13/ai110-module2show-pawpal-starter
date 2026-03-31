import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def make_scheduler():
    owner = Owner("TestOwner")
    pet1 = Pet("Rex", "Dog")
    pet2 = Pet("Mochi", "Cat")
    pet1.add_task(Task("Walk", "09:00", "daily", "Rex"))
    pet1.add_task(Task("Feed", "07:00", "daily", "Rex"))
    pet2.add_task(Task("Feed", "09:00", "daily", "Mochi"))  # conflict with Rex Walk
    pet2.add_task(Task("Medication", "12:00", "weekly", "Mochi"))
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    return Scheduler(owner)


def test_task_completion():
    task = Task("Walk", "08:00", "once", "Rex")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_task_addition_increases_count():
    pet = Pet("Rex", "Dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "08:00", "daily", "Rex"))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Feed", "09:00", "daily", "Rex"))
    assert len(pet.tasks) == 2


def test_sort_by_time():
    scheduler = make_scheduler()
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_recurrence_daily():
    task = Task("Walk", "08:00", "daily", "Rex")
    task.mark_complete()
    assert task.completed == False
    assert task.due_date == date.today() + timedelta(days=1)


def test_conflict_detection():
    scheduler = make_scheduler()
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0
    times = [t1.time for t1, t2 in conflicts]
    assert "09:00" in times


def test_filter_by_pet():
    scheduler = make_scheduler()
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi")
    assert all(t.pet_name == "Mochi" for t in mochi_tasks)


def test_filter_incomplete():
    scheduler = make_scheduler()
    incomplete = scheduler.filter_tasks(completed=False)
    assert all(not t.completed for t in incomplete)