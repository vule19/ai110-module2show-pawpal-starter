from pawpal_system import CareTask, Pet, Priority


def test_mark_complete_changes_status():
    task = CareTask("Morning walk", 30, Priority.HIGH)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(CareTask("Breakfast feeding", 10, Priority.HIGH))
    pet.add_task(CareTask("Evening walk", 20, Priority.MEDIUM))
    assert len(pet.get_tasks()) == 2