__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

import os
import csv
from typing import List

from student import Student


def markdown_student_feedback(student: Student, project_id: int) -> str:
    """
    A method that takes a student object and rerturn a report based on the tasks they have with a final grade
    in a Markdown format.

    We looked into the markdown framwork that comes with python, but we don't see a benefit in using it yet.

    :param student: The student for which the report will be genenrated.
    :param project_id: The project id (e.g., 1, 2, 3, ... etc).
    :return: A string in a Markdown format.
    """
    markdown = ""
    markdown += f"# Project-{project_id} Detailed Grades for {student.get_full_name()}\n\n"
    markdown += f"This is your detailed grade for the Project-{project_id}.\n"
    markdown += f"Please read everything carefully and try to understand where you made mistakes (if any).\n"
    markdown += f"We tried to be as descriptive in the grading script messages as possible.\n"
    markdown += f"However, if you don't understand any message, please ask for an explanation!.\n"
    markdown += f"The file is divided into smaller subsections.\n"
    markdown += f"Each section represent a task/test we examined.\n"
    markdown += f"There are tasks with points and there are other that have zero points.\n"
    markdown += f"Thus, if you see a zero that is not necessarily a bad thing.\n"
    markdown += f"At the end of this report, you will see the total points you got.\n"
    markdown += f"\n\n"

    grading_rubric = student.get_grading_rubric()
    tasks = grading_rubric.get_tasks()
    for task in tasks:
        markdown += f"#### Task-{task.task_id} [{'PASSED' if task.is_pass else 'FAILED'}, " \
                    f"{task.points}/{task.possible_points}]\n"
        markdown += f"- **Goal**: {task.desc}\n"
        markdown += f"- **Result**: Feedback from us and/or the system:\n\n"
        markdown += f"```\n"
        markdown += f"{task.result_desc}\n"
        markdown += f"```\n\n"

    markdown += f"\n"
    markdown += f"## Grading Summary:\n"

    # | Task-ID | Possible Points | Earned Points | Description |
    # |:-------:|:----------------|:--------------|:------------|
    # | 1 | 10 | 0 | Run x |
    # | 2 | 20 | 10 | Run y |
    # | 3 | 10 |10 | Check z |
    # | *Total* | *40* | *20* | **Was late n days ** |

    markdown += f"| Task-ID | Status | Possible Points | Earned Points | Description |\n"
    markdown += f"|:-------:|:------:|:---------------:|:-------------:|:------------|\n"
    number_of_passed_tasks = 0
    for task in tasks:
        # found the cool idea of green and red symbols here https://stackoverflow.com/a/70616224/3504748
        markdown += f"| {task.task_id} | {'🟢' if task.is_pass else '🔴'} | {task.possible_points} | {task.points} | " \
                    f"{task.desc} |\n"
        if task.is_pass:
            number_of_passed_tasks += 1
    if grading_rubric.is_late:
        markdown += f"| **Total** | {number_of_passed_tasks}/{len(tasks)} | " \
                    f"**{grading_rubric.total_possible_points}** | " \
                    f"**{grading_rubric.get_total_points_when_late()}** | " \
                    f"**Was late {grading_rubric.late_days_count:.2f} days** |\n"
    else:
        markdown += f"| **Total** | {number_of_passed_tasks}/{len(tasks)} | " \
                    f"**{grading_rubric.total_possible_points}** | " \
                    f"**{grading_rubric.get_total_points()}** | |\n"

    if grading_rubric.is_late:
        markdown += f"Late deduction explanation!\n"
        markdown += f"{grading_rubric.get_late_calculation_explanation()}\n\n"

    return markdown


def csv_overall_report(students: List[Student], project_id: int, dir_name="reports"):
    """
    Exporting a csv files with the following columns:
    sid, name, repo_link, t_0, ..., t_n, is_late, late_days, penalty_percentage_per_late_day, total_considering_late_days
    :param students:
    :param project_id:
    :param dir_name:
    :return:
    """
    report_full_dir = f"{students[0].get_ini_root_dir()}/{dir_name}"

    # make sure the main report dir exists
    if not os.path.exists(report_full_dir):
        os.makedirs(report_full_dir)

    # field names
    fields = ['sid', 'name', 'repo_link']  # we will add more based on tasks (e.g., t1, t2, t3, total

    sample_tasks = students[0].get_grading_rubric().get_tasks()
    for sample_task in sample_tasks:
        fields.append(f"t{sample_task.task_id}[{sample_task.possible_points}]")
    fields += ['is_late', 'late_days', 'penalty_percentage_per_late_day', 'total_if_was_not_late', 'total']
    rows = []
    for student in students:
        row = [f"{student.get_std_id()}", f"{student.get_full_name()}", f"{student.get_repo_link()}"]
        for task in student.get_grading_rubric().get_tasks():
            row.append(f"{task.points}")
        row.append(student.get_grading_rubric().is_late)
        row.append(student.get_grading_rubric().late_days_count)
        row.append(student.get_grading_rubric().late_fee_per_day)
        row.append(f"{student.get_grading_rubric().get_total_points()}")
        row.append(student.get_grading_rubric().get_total_points_when_late())

        rows.append(row)

    # name of csv file
    filename = f"project{project_id}-full-report.csv"

    # writing to csv file
    with open(f"{report_full_dir}/{filename}", 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)


def email_list_csv(students: List[Student], project_id: int, dir_name="reports"):
    report_full_dir = f"{students[0].get_ini_root_dir()}/{dir_name}"

    # make sure the main report dir exists
    if not os.path.exists(report_full_dir):
        os.makedirs(report_full_dir)

    # field names
    fields = ['sid', 'first_name', 'email', 'attachment']

    rows = []
    for student in students:
        row = [f"{student.get_std_id()}", f"{student.get_first_name()}", f"{student.get_std_id()}@qu.edu.sa",
               f"{report_full_dir}/{student.get_std_id()}-{student.get_first_name()}-project-{project_id}.md"]
        rows.append(row)

    # name of csv file
    filename = f"project{project_id}-mailing-report.csv"

    # writing to csv file
    with open(f"{report_full_dir}/{filename}", 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)


def generate_reports(students: List[Student], project_id: int, dir_name="reports"):
    """
    Generate the detailed report for student.

    :param students: A list of student objects.
    :param project_id: The project id (e.g., 1, 2, 3, ... etc).
    :param dir_name: The nested directory name where these reports should be saved.
    """

    report_full_dir = f"{students[0].get_ini_root_dir()}/{dir_name}"

    # make sure the main report dir exists
    if not os.path.exists(report_full_dir):
        os.makedirs(report_full_dir)

    for student in students:
        detailed_report = markdown_student_feedback(student, project_id)
        with open(f"{report_full_dir}/{student.get_std_id()}-{student.get_first_name()}-"
                  f"project-{project_id}.md", "w") as md:
            md.write(detailed_report)
