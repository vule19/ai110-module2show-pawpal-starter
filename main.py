from pawpal_system import CareTask, Owner, Pet, Priority

# --- Setup ---
jordan = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

# --- Tasks for Mochi (dog) ---
mochi.add_task(CareTask("Morning walk",      30, Priority.HIGH,   "Daily exercise"))
mochi.add_task(CareTask("Breakfast feeding", 10, Priority.HIGH,   "Scheduled meal"))
mochi.add_task(CareTask("Teeth brushing",    10, Priority.MEDIUM, "Weekly dental care"))

# --- Tasks for Luna (cat) ---
luna.add_task(CareTask("Breakfast feeding",  5,  Priority.HIGH,   "Scheduled meal"))
luna.add_task(CareTask("Litter box cleaning",10, Priority.MEDIUM, "Daily hygiene"))
luna.add_task(CareTask("Enrichment play",    20, Priority.LOW,    "Mental stimulation"))

# --- Add pets to owner ---
jordan.add_pet(mochi)
jordan.add_pet(luna)

# --- Generate and print schedule ---
schedule = jordan.get_schedule()

print("=" * 40)
print(f"  PawPal+ — {jordan.name}'s Daily Plan")
print("=" * 40)
print(schedule.display())
print()
print("--- Why these tasks? ---")
print(schedule.explain())
