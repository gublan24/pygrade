__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

from typing import Tuple

from pygrade.src import util
from pygrade.src.command import Command
from pygrade.src.feedback import Feedback


class ExecutableTask:
    def __init__(self, task_id: int, desc: str, possible_points: int, command: Command):
        self.task_id = task_id  # the id of the task for ordering and querying purposes
        self.desc = desc  # the task description. Should be useful in reporting (e.g., "Provide a cloneable repo.")
        self.possible_points = possible_points  # if this task worth anything, how much?
        self.command = command  # the command we will run and either pass or not.
        self.points = 0   # the total points the student got based on the number of possible_points. Default: Zero
        self.is_pass = False  # did the task pass? False by default
        self.result_desc = ""  # the result to help understand what went good/bad (e.g., "Failed to clone repo x due to y").

    def execute(self):
        self.command.execute()
        self.set_result(self.command.get_result())

    def set_result(self, result: Tuple[bool, str]):
        self.is_pass = result[0]
        self.result_desc = result[1]
        if self.is_pass:
            self.points = self.possible_points
        else:
            self.points = 0

    def cast(self) -> list:
        return [self.task_id, self.desc, self.possible_points, self.points, self.is_pass, self.result_desc]


class ReportableTask:

    def __init__(self, task_id: int, desc: str, possible_points: int, points: int, is_pass: bool, result_desc: str):
        self.task_id = task_id  # the id of the task for ordering and querying purposes
        self.desc = desc  # the task description. Should be useful in reporting (e.g., "Provide a cloneable repo.")
        self.possible_points = possible_points  # if this task worth anything, how much?
        self.points = points  # the total points the student got based on the number of possible_points.
        self.is_pass = is_pass  # did the task pass? False by default
        self.result_desc = result_desc  # the result to help understand what went good/bad (e.g., "Failed to clone repo x due to y").
