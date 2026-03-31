import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Session state init
if "owner" not in st.session_state:
    st.session_state.owner = Owner("My Household")

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("Smart pet care management system")

# --- Add a Pet ---
st.header("Add a Pet")
with st.container():
    col1, col2 = st.columns(2)
    pet_name = col1.text_input("Pet Name")
    pet_species = col2.text_input("Species (e.g. Dog, Cat)")
    if st.button("Add Pet"):
        if pet_name and pet_species:
            owner.add_pet(Pet(pet_name.strip(), pet_species.strip()))
            st.success(f"Added {pet_name} the {pet_species}!")
        else:
            st.warning("Please fill in both fields.")

# --- Add a Task ---
st.header("Schedule a Task")
pet_names = [p.name for p in owner.pets]
if pet_names:
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        selected_pet = col1.selectbox("Pet", pet_names)
        task_desc = col2.text_input("Task")
        task_time = col3.text_input("Time (HH:MM)")
        task_freq = col4.selectbox("Frequency", ["daily", "weekly", "once"])
        if st.button("Add Task"):
            if task_desc and task_time:
                pet = next(p for p in owner.pets if p.name == selected_pet)
                pet.add_task(Task(task_desc, task_time, task_freq, selected_pet))
                st.success(f"Task '{task_desc}' added for {selected_pet}!")
            else:
                st.warning("Please fill in task description and time.")
else:
    st.info("Add a pet first before scheduling tasks.")

# --- Today's Schedule ---
st.header("📅 Today's Schedule")

filter_pet = st.selectbox("Filter by pet (optional)", ["All"] + pet_names)
show_completed = st.checkbox("Show completed tasks", value=True)

all_tasks = scheduler.sort_by_time()

if filter_pet != "All":
    all_tasks = [t for t in all_tasks if t.pet_name == filter_pet]

if not show_completed:
    all_tasks = [t for t in all_tasks if not t.completed]

if all_tasks:
    for task in all_tasks:
        col1, col2 = st.columns([4, 1])
        status = "✅" if task.completed else "🔲"
        col1.write(f"{status} **{task.time}** — {task.description} *(_{task.pet_name}_, {task.frequency})*")
        if not task.completed:
            if col2.button("Done", key=f"{task.description}-{task.time}-{task.pet_name}"):
                task.mark_complete()
                st.rerun()
else:
    st.info("No tasks to show.")

# --- Conflict Warnings ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.header("⚠️ Schedule Conflicts")
    for t1, t2 in conflicts:
        st.warning(f"**{t1.description}** ({t1.pet_name}) and **{t2.description}** ({t2.pet_name}) are both scheduled at **{t1.time}**.")