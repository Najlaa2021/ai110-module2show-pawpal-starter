import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a small pet-care planning assistant.
This version uses the backend classes from the logic layer so your pet and task data persists while you use the app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Owner & Pets")
owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
if owner_name != owner.name:
    owner.name = owner_name

with st.expander("Add a pet", expanded=True):
    pet_name = st.text_input("Pet name", key="pet_name_input")
    species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")
    age = st.number_input("Age", min_value=0, max_value=30, value=1, key="pet_age")

    if st.button("Add pet"):
        if pet_name.strip():
            new_pet = Pet(name=pet_name.strip(), species=species, age=int(age))
            owner.add_pet(new_pet)
            st.success(f"Added {new_pet.name} to {owner.name}'s profile.")
            st.session_state.pet_name_input = ""
            st.session_state.pet_species = "dog"
            st.session_state.pet_age = 1
        else:
            st.warning("Please enter a pet name before adding a pet.")

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
st.caption("Add a task for one of your pets and it will be stored in the owner's session state.")

pet_options = [pet.name for pet in owner.pets]
if pet_options:
    selected_pet_name = st.selectbox("Assign to pet", pet_options, key="selected_pet")
    task_title = st.text_input("Task title", key="task_title_input")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")

    if st.button("Add task"):
        if task_title.strip():
            selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
            task = Task(title=task_title.strip(), duration_minutes=int(duration), priority=priority)
            selected_pet.add_task(task)
            st.success(f"Added '{task.title}' for {selected_pet.name}.")
            st.session_state.task_title_input = ""
        else:
            st.warning("Please enter a task title before adding a task.")

    for pet in owner.pets:
        if pet.tasks:
            st.write(f"{pet.name}'s tasks:")
            for task in pet.tasks:
                st.write(f"- {task.title} ({task.duration_minutes} min, {task.priority})")
else:
    st.info("Add a pet first, then you can add tasks.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    scheduled = scheduler.schedule(date.today())
    if scheduled:
        st.write(f"Today's schedule for {owner.name}:")
        for task in scheduled:
            pet_name = task.pet.name if task.pet else "unknown"
            time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "unscheduled"
            st.write(f"- {time_str} — {task.title} for {pet_name} ({task.duration_minutes} min) [priority: {task.priority}]")
    else:
        st.info("No tasks to schedule yet.")
