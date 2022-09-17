__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

import os
import shutil
import argparse
import datetime
import logging

from src import credentials as su, report, config, util, git
from src.command import PythonCommand
from src.task import ExecutableTask, ReportableTask
from src.student import Student

logger = logging.getLogger(__name__)


def copy_file_to_repo(student: Student):
    try:
        shutil.copy("../project-0/hello.py", f"{student.get_repo_local_location()}/original-hello.py")
        message = f"Copied original 'hello.py' file to '{student.get_obscure_rep_local_location()}'"
        result = True
    except Exception as e:
        message = f"Could not copy the original file 'hellp.py' to '{student.get_obscure_rep_local_location()}'. " \
                  f"Error: {e}"
        logger.warning(message)
        result = False
    return result, message


def diff_check(student: Student):
    try:
        with open(f"{student.get_repo_local_location()}/hello.py") as f:
            student_file = f.read()
        with open(f"{student.get_repo_local_location()}/original-hello.py") as f:
            original_file = f.read()
    except Exception as e:
        message = f"No repo found locally! Error: {e}"
        logger.warning(message)
        return False, message

    if student_file == original_file:
        message = f"No changes applied to the file 'hello.py'\n\n" \
                  f"Content of student version of 'hello.py':\n" \
                  f"===========================================\n" \
                  f"{student_file}\n" \
                  f"===========================================\n\n" \
                  f"Content of original 'hello.py':\n" \
                  f"===========================================\n"\
                  f"{original_file}" \
                  f"==========================================="
        logger.warning(message)
        return False, message
    else:
        message = f"The file hello.py changed successfully!\n\n" \
                  f"Content of student version of 'hello.py':\n" \
                  f"===========================================\n" \
                  f"{student_file}\n" \
                  f"===========================================\n\n" \
                  f"Content of original 'hello.py':\n" \
                  f"===========================================\n" \
                  f"{original_file}" \
                  f"==========================================="
        return True, message


def main(path: str, deadline: datetime = None):
    key_files = util.get_ini_files(path)
    print(deadline)
    students = su.get_students_objects_from_path(key_files)
    for student in students:

        # for each student, we want a rubric that will be filled using the tasks below
        student_rubric = student.get_grading_rubric()

        tasks = [
            ExecutableTask(1, "Get the file credentials.ini", possible_points=10,
                           command=PythonCommand(su.dummy_get_file)),
            ExecutableTask(2, "Get author from credentials.ini", possible_points=10,
                           command=PythonCommand(su.get_name_from_ini, args=[student])),
            ExecutableTask(3, "Get quid from credentials.ini", possible_points=10,
                           command=PythonCommand(su.get_student_id_from_ini, args=[student])),
            ExecutableTask(4, "Get repository link from credentials.ini", possible_points=10,
                           command=PythonCommand(su.get_student_repo_link_from_ini, args=[student])),
            ExecutableTask(5, "Clone repository to local file", possible_points=30,
                           command=PythonCommand(git.clone, args=[student])),
            ExecutableTask(6, "Check if repo has any late edits", possible_points=0,
                           command=PythonCommand(git.validate_last_change_date, args=[student, config.P0_DEADLINE])),
            ExecutableTask(7, "Copy original hello file to local repo", possible_points=0,
                           command=PythonCommand(copy_file_to_repo, args=[student])),
            ExecutableTask(8, "Check if hello.py was updated", possible_points=30,
                           command=PythonCommand(diff_check, args=[student]))

        ]
        for task in tasks:
            task.command.execute()
            task.execute()
            student_rubric.add_task(ReportableTask(*task.cast()))

    # done grading, now to generating report
    report.generate_reports(students, 0)
    report.csv_overall_report(students, 0)


if __name__ == '__main__':
    """
    All the user needs for each assignment is to pass a directory where the .ini files are. Any other special handling
    (e.g., copying a file or some similar task) should be handled on the code above. This is because it is hard to 
    anticipate the different requirement for each assignment.  
    """

    parser = argparse.ArgumentParser(description='Download Student Files!')
    parser.add_argument('path', metavar='path', help='Relative/Absolute path to the directory where'
                                                     '.ini files are saved!')

    args = parser.parse_args()

    dl = datetime.datetime(2021, 10, 5, 20, 0)
    main(os.path.abspath(args.path), deadline=dl)
