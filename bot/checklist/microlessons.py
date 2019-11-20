import os

from core.exceptions import NoLessonWasFoundError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MICROLESSONS_DIR = os.path.join(BASE_DIR, 'bot/checklist/microlessons')
MICROLESSONS = {i: name for i, name in enumerate(os.listdir(MICROLESSONS_DIR), start=1) if name.startswith('lesson')}


def get_lesson_file(number: int) -> str: 
    lesson = MICROLESSONS.get(number)
    if not lesson:
        raise NoLessonWasFoundError(f"no lesson was found with number {number}")
    return os.path.join(MICROLESSONS_DIR, lesson)


def get_lesson_text(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def get_lt_from_number(number: int) -> str:
    return get_lesson_text(get_lesson_file(number))