import streamlit as st
from datetime import date
from pathlib import Path

from pawpal_system import Owner, Pet, Scheduler, Task

DATA_FILE = Path("data.json")

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    if DATA_FILE.exists():
        try:
            st.session_state.owner = Owner.load_from_json(str(DATA_FILE))
        except Exception:
            st.session_state.owner = Owner(name="Jordan")
    else:
        st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner


def save_owner_state() -> None:
    try:
        owner.save_to_json(str(DATA_FILE))
    except Exception:
        pass

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a small pet-care planning assistant.
This version uses the backend classes from the logic layer so your pet and task data persist while you use the app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

with st.expander("Owner settings", expanded=True):
    owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
    availability = st.number_input(
        "Available minutes today",
        min_value=60,
        max_value=1440,
        value=owner.availability_minutes,
        key="owner_availability_input",
    )

    if owner_name != owner.name or availability != owner.availability_minutes:
        owner.name = owner_name
        owner.availability_minutes = int(availability)
        save_owner_state()

with st.expander("Add a pet", expanded=False):
    pet_name = st.text_input("Pet name", key="pet_name_input")
    species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")
    age = st.number_input("Age", min_value=0, max_value=30, value=1, key="pet_age")

    if st.button("Add pet"):
        if pet_name.strip():
            new_pet = Pet(name=pet_name.strip(), species=species, age=int(age))
            owner.add_pet(new_pet)
            save_owner_state()
            st.success(f"Added {new_pet.name} to {owner.name}'s profile.")
            st.session_state.pet_name_input = ""
            st.session_state.pet_species = "dog"
            st.session_state.pet_age = 1
        else:
            st.warning("Please enter a pet name before adding a pet.")

st.divider()

st.subheader("Pets and Tasks")
if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets yet. Add one above.")

if owner.pets:
    pet_options = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Assign task to pet", pet_options, key="selected_pet")
    task_title = st.text_input("Task title", key="task_title_input")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key="task_frequency")

    if st.button("Add task"):
        if task_title.strip():
            selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
            task = Task(
                title=task_title.strip(),
                duration_minutes=int(duration),
                priority=priority,
                frequency=None if frequency == "once" else frequency,
            )
            selected_pet.add_task(task)
            save_owner_state()
            st.success(f"Added '{task.title}' for {selected_pet.name}.")
            st.session_state.task_title_input = ""
        else:
            st.warning("Please enter a task title before adding a task.")

    for pet in owner.pets:
        if pet.tasks:
            st.write(f"Tasks for {pet.name}:")
            for task in pet.tasks:
                status = "completed" if task.completed else "pending"
                task_label = f"- {task.title} ({task.duration_minutes} min, {task.priority}, {status})"
                st.write(task_label)
                if task.frequency and not task.completed:
                    if st.button(f"Complete: {task.title}", key=f"complete_{pet.name}_{task.title}"):
                        next_task = task.mark_complete_and_schedule_next(date.today())
                        if next_task is not None:
                            pet.add_task(next_task)
                            save_owner_state()
                            st.success(f"Completed {task.title} and created the next {task.frequency} occurrence.")
                        else:
                            task.mark_complete()
                            save_owner_state()
                            st.success(f"Marked {task.title} as complete.")
else:
    st.info("Add a pet first, then you can add tasks.")

if owner.pets:
    with st.expander("Edit or remove an existing task", expanded=False):
        edit_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets], key="edit_pet")
        edit_pet = next(pet for pet in owner.pets if pet.name == edit_pet_name)
        if edit_pet.tasks:
            task_labels = [f"{task.title} ({task.priority}, {task.duration_minutes}m)" for task in edit_pet.tasks]
            selected_index = st.selectbox(
                "Choose a task",
                list(range(len(task_labels))),
                format_func=lambda index: task_labels[index],
                key="edit_task",
            )
            task_to_edit = edit_pet.tasks[selected_index]

            edit_title = st.text_input("Task title", value=task_to_edit.title, key="edit_task_title")
            edit_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=task_to_edit.duration_minutes, key="edit_task_duration")
            edit_priority = st.selectbox(
                "Priority",
                ["low", "medium", "high"],
                index=["low", "medium", "high"].index(task_to_edit.priority),
                key="edit_task_priority",
            )
            edit_frequency = st.selectbox(
                "Frequency",
                ["once", "daily", "weekly"],
                index=["once", "daily", "weekly"].index(task_to_edit.frequency or "once"),
                key="edit_task_frequency",
            )
            edit_completed = st.checkbox("Completed", value=task_to_edit.completed, key="edit_task_completed")

            if st.button("Save changes", key="save_task_changes"):
                task_to_edit.title = edit_title.strip() or task_to_edit.title
                task_to_edit.duration_minutes = int(edit_duration)
                task_to_edit.priority = edit_priority
                task_to_edit.frequency = None if edit_frequency == "once" else edit_frequency
                task_to_edit.completed = edit_completed
                save_owner_state()
                st.success(f"Saved changes for '{task_to_edit.title}'.")

            if st.button("Delete task", key="delete_task"):
                edit_pet.remove_task(task_to_edit.title)
                save_owner_state()
                st.success(f"Removed '{task_to_edit.title}' from {edit_pet.name}.")
        else:
            st.info(f"{edit_pet.name} has no tasks yet.")

st.divider()

st.subheader("Build Schedule")
if owner.pets:
    selected_schedule_pet = st.selectbox("View schedule for", ["All pets", *[pet.name for pet in owner.pets]], key="schedule_pet_filter")
else:
    selected_schedule_pet = "All pets"

slot_minutes = st.number_input(
    "Next available slot duration (minutes)",
    min_value=5,
    max_value=240,
    value=30,
    key="next_slot_duration",
)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.build_plan(date.today())
    scheduled_tasks = plan.generate_schedule()
    save_owner_state()

    pet_filter = None if selected_schedule_pet == "All pets" else selected_schedule_pet
    filtered_tasks = scheduler.filter_tasks(scheduled_tasks, pet_name=pet_filter)
    conflicts = scheduler.detect_conflicts(scheduled_tasks)

    if filtered_tasks:
        st.success("Schedule generated. Pending tasks were ordered by priority and time.")
        schedule_rows = []
        for task in filtered_tasks:
            pet_name = task.pet.name if task.pet else "unknown"
            time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "unscheduled"
            schedule_rows.append(
                {
                    "Time": time_str,
                    "Task": task.title,
                    "Pet": pet_name,
                    "Priority": task.priority,
                    "Duration (min)": task.duration_minutes,
                }
            )
        st.dataframe(schedule_rows, use_container_width=True, hide_index=True)
        st.markdown("**Why this plan?**")
        st.text(plan.explain_plan())
        st.caption(
            "Tasks are scheduled starting at 08:00 and ordered by priority, then filled into the owner's available time window."
        )
    else:
        st.info("No pending tasks to schedule yet.")

    if conflicts:
        st.warning("Conflict warnings")
        for warning in conflicts:
            st.write(f"- {warning}")
        st.caption(
            "These tasks share the same time slot. Consider moving one earlier or later so the plan stays clear for the pet owner."
        )
    else:
        st.caption("No scheduling conflicts detected for the current task list.")

if st.button("Find next available slot"):
    scheduler = Scheduler(owner)
    slot = scheduler.find_next_available_slot(slot_minutes)
    if slot:
        st.info(f"Next available slot starts at {slot.strftime('%H:%M')}.")
    else:
        st.warning("No available slot was found within the owner's availability window.")
