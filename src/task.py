__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

from typing import Tuple

import util
from command import Command
from feedback import Feedback


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
        feedback = self.command.get_result()
        if isinstance(feedback, Feedback):
            self.set_feedback_based_result(feedback)
        else:
            self.set_result(feedback[0], feedback[1])

    def set_result(self, is_pass: bool, message: str):
        self.is_pass = is_pass
        self.result_desc = message
        if self.is_pass:
            self.points = self.possible_points
        else:
            self.points = 0

    def set_feedback_based_result(self, feedback: Feedback):
        self.is_pass = feedback.is_pass

        # scaling the score from 0-100 scale to 0-[whatever the possible points here are]
        # self.points = round((feedback.get_score() - 0)/(100 - 0) * (self.possible_points - 0) + 0, 2)
        self.points = util.scale_to_range(value=feedback.get_score(), range_min=0, range_max=100, target_min=0,
                                          target_max=self.possible_points)
        self.result_desc = feedback.get_message()

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
