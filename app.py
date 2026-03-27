import streamlit as st
from pawpal_system import CareTask, Owner, Pet, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state vault initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Owner & Pet setup ---
st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=90)

if st.button("Set up owner & pet"):
    pet = Pet(name=pet_name, species=species, age=0)
    owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.pet = pet
    st.session_state.tasks = []
    st.success(f"Set up {owner_name} with pet {pet_name}!")

st.divider()

# --- Task entry ---
st.subheader("Add Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.pet is None:
        st.warning("Please set up an owner & pet first.")
    else:
        priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
        task = CareTask(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority_map[priority],
        )
        st.session_state.pet.add_task(task)
        st.session_state.tasks.append(
            {"title": task_title, "duration_minutes": int(duration), "priority": priority}
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule generation ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.warning("Please set up an owner & pet first.")
    elif not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = st.session_state.owner.get_schedule()
        st.success("Schedule generated!")
        st.text(schedule.display())
        st.markdown("**Why these tasks?**")
        st.text(schedule.explain())