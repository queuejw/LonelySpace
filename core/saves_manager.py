import os.path

from core.constants import DEFAULT_SAVE_NAME


def save_exist() -> bool:
    return os.path.exists(DEFAULT_SAVE_NAME)
