import os
import re
import logging
import subprocess

from student import Student
from feedback import Feedback

logger = logging.getLogger(__name__)


def get_score_from_report(report: str) -> float:
    """
    We are looking for `rated at xx.xx/10
    :param report:
    :return:
    """
    # first get the location of the string that start with 'rated at'
    location_of_first_char = report.find("rated at")

    # from the location of the given string get a string of length 17 (this will for sure include the rate)
    short_string = report[location_of_first_char:location_of_first_char + 17]

    # from the 'rated at X.X/10' or 'rated at xx.xx/10' string, get the numbers using regex.
    list_of_numbers = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", short_string)

    # from the strings that represent numbers get the first number which is the rating.
    score = float(list_of_numbers[0])

    return score


def check_for_score(student: Student, class_name: str) -> (bool, str):
    """
    Check the score of a given class confirmation to PEP8 coding style. We use pylint to obtain the score.
    pylint --attr-naming-style any --argument-naming-style any  point.py

    :param student:
    :param class_name:
    :return:
    """

    # --attr-naming-style: we don't want to enforce any style for attributes.
    # --argument-naming-style: we don't want to enforce any style for arguments.

    try:
        run_test = subprocess.run(["pylint", "--attr-naming-style", "any", "--argument-naming-style", "any",
                                   "--disable=C0123", f"{class_name}"], cwd=student.get_repo_local_location(),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        score = get_score_from_report(run_test.stdout.decode())
        message = run_test.stdout.decode()
        logger.debug(f"{student.get_std_id()} got a score of {score}. The return code is {run_test.returncode}")
        is_pass = True if run_test.returncode == 0 else False
    except BaseException as e:
        message = f"Could not run pylint on class {class_name} for {student.get_std_id()}: {e}"
        score = 0
        is_pass = False

    return Feedback(is_pass, score*10, message)


def check_for_type_hints(student: Student, class_name: str):
    """
    I flake8 annotations, each line printed is a missing annotation or one that has a problem. Thus, for each line
    we deduct one point.

    :param student:
    :param class_name:
    :return:
    """

    # if file doesn't exist and is accessible, don't do anything.
    path = f"{student.get_repo_local_location()}/{class_name}"
    if not os.path.isfile(path):
        logger.debug(f"Didn't find the file {path}")
        return Feedback(False, 0, f"No file named {class_name}!")

    # We only focus on the following annotation errors (see https://pypi.org/project/flake8-annotations/):
    annotations = "ANN001,ANN201,ANN202,ANN203,ANN204,ANN205,ANN206"

    try:
        run_test = subprocess.run(["flake8", f"--select={annotations}", "--suppress-none-returning", f"{class_name}"],
                                  cwd=student.get_repo_local_location(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        number_of_errors = len(run_test.stdout.decode().splitlines())
        score = max(0, 10-number_of_errors)
        if run_test.returncode == 0:
            message = "No annotation issues!"
        else:
            message = run_test.stdout.decode()
        logger.debug(f"{student.get_std_id()} got a score of: {score}. Massage from System: {message}")
        is_pass = True if run_test.returncode == 0 else False
    except BaseException as e:
        message = f"Could not run flake8 on class {class_name} for {student.get_std_id()}: {e}"
        score = 0
        is_pass = False

    return Feedback(is_pass, score*10, message)
