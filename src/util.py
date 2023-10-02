__author__="Ziyad Alsaeed"
__email__ ="zalsaeed@qu.edu.sa"

import os
import glob
import random
import logging
import datetime
from typing import Any

logger = logging.getLogger(__name__)


def get_ini_files(path: str) -> list:
    """
    Return all .ini files within path.
    :param path: The path where we should look for ini files/
    :return: A list with an absolute path to each ini file.
    """
    if not os.path.isdir(path):
        raise RuntimeError(f"{path} is not a directory!")

    ini_files = glob.glob(path+"/*.ini")

    if not ini_files:
        raise RuntimeError(f"No .ini files found in {path}")

    logger.debug(f"Found .ini files {ini_files}")
    return ini_files


def get_student_id_from_file_path(path: str) -> str:
    """
    This is special for Blackboard. The submission file names are usually named following this pattern:
    "<assignment name which can have spaces>_<student_id>_attempt_<date-time of the attempt '-' seperated>_
        <name of file as given by student>.<file type>"
    Example: "Project 0_391108724_attempt_2022-09-12-15-45-08_credentials.ini"
    We want the student ID.
    :param path:
    :return:
    """
    # unless the assignment is named with an underscore, this is safe!
    file__base_name = os.path.basename(str(path))
    return file__base_name.split("_")[1]

# def write_dict_to_csv(data: dict, output_dir: str, file_name: str, comments: str = None):
#     project_root = f"{output_dir}{file_name}.csv"
#
#     with open(project_root, "w") as e_file:
#         if comments is not None:
#             e_file.write("# " + comments + "\n")
#         pd.DataFrame(data).to_csv(e_file, index=False)


def read_random_line_from_file(file_path: str) -> str:
    with open(file_path) as file:
        lines = file.read().splitlines()
        line = random.choice(lines)
    return line

def scale_to_range(value: float, range_min: float, range_max: float, target_min: float, target_max: float):
    """
    Scale a value in [range_min - range_max] to be within [target_min - target_max].
    See this post for more info:
    https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range

    :param value:
    :param range_min:
    :param range_max:
    :param target_min:
    :param target_max:
    :return:
    """
    # we round to two decimals!
    return round((value - range_min) / (range_max - range_min) * (target_max - target_min) + target_min, 2)


def move_item_to_index(original: list, item: Any, idx: int) -> list:
    """
    Move an element in the list to a specifi location.
    Preconditions: The list must not be empty. The item must be actually in the list.
    And the index must be within the list.

    :param original: The original list.
    :param item: An item of the list.
    :param idx: The index which we will move the item to.
    :return: The list after moving the item to the new location.
    """
    assert 0 <= idx < len(original)
    assert item in original

    original.insert(idx, original.pop(original.index(item)))

    return original


def get_absolut_path_dir(path: str) -> str:
    abspath = os.path.abspath(path)
    return os.path.dirname(abspath)


def get_filename_with_extension(path: str) -> str:
    return os.path.basename(path)


def get_filename_without_extension(path: str) -> str:
    file_name = os.path.basename(path)
    break_name = file_name.split(".")
    return ".".join(break_name[:-1])


def get_timestamp() -> str:
    return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
