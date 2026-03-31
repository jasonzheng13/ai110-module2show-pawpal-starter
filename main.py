from pawpal_system import Task, Pet, Owner, Scheduler

# Create owner
owner = Owner(name="Jason")

# Create pets
buddy = Pet(name="Buddy", species="Dog")
luna = Pet(name="Luna", species="Cat")

# Add tasks to Buddy
buddy.add_task(Task("Morning Walk", "07:00", "daily", "Buddy"))
buddy.add_task(Task("Feeding", "08:00", "daily", "Buddy"))
buddy.add_task(Task("Evening Walk", "18:00", "daily", "Buddy"))

# Add tasks to Luna
luna.add_task(Task("Feeding", "08:00", "daily", "Luna"))  # conflict with Buddy's feeding
luna.add_task(Task("Medication", "12:00", "weekly", "Luna"))
luna.add_task(Task("Vet Appointment", "15:00", "once", "Luna"))

# Add pets to owner
owner.add_pet(buddy)
owner.add_pet(luna)

# Create scheduler and print schedule
scheduler = Scheduler(owner)
scheduler.print_schedule()

# Demo filtering
print("\n🔍 Incomplete tasks only:")
incomplete = scheduler.filter_tasks(completed=False)
for t in incomplete:
    print(f"  {t}")

# Demo mark complete + recurrence
print("\n✅ Marking Buddy's Morning Walk complete...")
buddy.tasks[0].mark_complete()
print(f"  New due date: {buddy.tasks[0].due_date}")

# Demo filtering by pet
print("\n🐱 Luna's tasks:")
luna_tasks = scheduler.filter_tasks(pet_name="Luna")
for t in luna_tasks:
    print(f"  {t}")