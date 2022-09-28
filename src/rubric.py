__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

import math
import logging
from typing import Dict, List

from pygrade.src.task import ReportableTask


class Rubric:

    def __init__(self, possible_points=100, extra_credit=False):
        self.total_possible_points = possible_points
        self.extra_credit = extra_credit
        self._task_counter = 0
        self.task_report_dict: Dict[int, ReportableTask] = {}
        self.is_late = False
        self.late_days_count = 0.0
        self.log = logging.getLogger(self.__class__.__name__)

        self.late_fee_per_day = .2

    def add_task(self, task: ReportableTask):
        self.task_report_dict.update({task.task_id: task})

    def get_tasks(self) -> List[ReportableTask]:
        tasks_list = []
        for key in sorted(self.task_report_dict):
            tasks_list.append(self.task_report_dict[key])
        return tasks_list

    def get_total_points(self) -> int:
        total = 0
        for key, task in self.task_report_dict.items():
            total += task.points
        if total > self.total_possible_points:
            self.log.error(f'Total grade found {total} is larger than possible points {self.total_possible_points}')
        return total

    def get_total_points_when_late(self) -> int:
        total = 0
        for key, task in self.task_report_dict.items():
            total += task.points
        if total > self.total_possible_points:
            self.log.error(f'Total grade found {total} is larger than possible points {self.total_possible_points}')

        # calling this method should only be when this is true, but double-checking
        if self.is_late:
            # the max percentage we deduct is 100% (duh), thus we want to make sure if they are more than 5 days late
            # given the percentage 20% per day, then there grade doesn't get to be negative.
            penalty_percentage = min(1.0, self.late_fee_per_day * self.late_days_count)

            # now simply find the total given the penalty
            total = (1 - penalty_percentage) * total

        # round up to an integer. Reminder int(x.x) will not always round up.
        return math.ceil(total)

    def get_late_calculation_explanation(self) -> str:
        message = f"Deducting {self.late_fee_per_day*100}% per late-day " \
                  f"(number of late-days = {self.late_days_count}).\n"
        message += f"Total deducting percentage = {self.late_fee_per_day*100}% * {self.late_days_count} = " \
                   f"{self.late_fee_per_day*self.late_days_count*100}%\n"
        message += f"Total points before deducting late percentage penalty is {self.get_total_points()}.\n"
        message += f"Final total points after deducting {self.late_fee_per_day*self.late_days_count*100}% " \
                   f"is {self.get_total_points_when_late()}"
        return message



