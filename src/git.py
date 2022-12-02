__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

import re
import os.path
import logging
import datetime
import subprocess

from student import Student

logger = logging.getLogger(__name__)


def clone(student: Student, repos_dir_name="repos") -> (bool, str):
    """
    Given a student object and a directory name, the method will try to clone the repo where the ini is. For example,
    if the ini file is within /root/p1/credentials.ini then the repo will be cloned to
    /root/p1/<repose_dir_name>/<student_id>.

    :param student:
    :param repos_dir_name:
    :return:
    """

    repos_full_dir = f"{student.get_ini_root_dir()}/{repos_dir_name}"

    # make sure the main repos dir exists
    if not os.path.exists(repos_full_dir):
        os.makedirs(repos_full_dir)

    # clone to a directory named after the student id
    gitclone = subprocess.run(["git", "clone", "--quiet", student.get_repo_link(),
                               f"{repos_full_dir}/{student.get_std_id()}"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if gitclone.returncode != 0:
        if re.match("fatal: destination path\s'.*'\salready exists and is not an empty directory\.\n",
                    gitclone.stderr.decode()):
            result = f"A repo for {student.get_first_name()} already exists in dir " \
                     f"'~/{os.path.basename(repos_full_dir)}/{student.get_std_id()}'"
            logger.warning(result)
            student.set_repo_local_location(f'{repos_full_dir}/{student.get_std_id()}')
            success = True
        elif re.match("remote: The requested repository either does not exist or you do not have access.*",
                      gitclone.stderr.decode()):
            result = f"{student.get_first_name()}'s is most likely private with no access to it. " \
                     f"Error message from git: {gitclone.stderr.decode()}"
            logger.warning(result)
            success = False
        elif re.match("remote: Forbidden\n.*403\n", gitclone.stderr.decode()):
            result = f"{student.get_first_name()}'s link is corrupted! Error: {gitclone.stderr}"
            logger.warning(result)
            success = False
        else:
            result = f"Unhandled case during cloning for {student.get_first_name()}! Error: {gitclone.stderr.decode()}"
            logger.error(result)
            success = False
    else:
        success = True
        student.set_repo_local_location(f'{repos_full_dir}/{student.get_std_id()}')
        result = f"Repo cloned successfully (~/{os.path.basename(repos_full_dir)}/{student.get_std_id()})!"

    return success, result


def validate_last_change_date(student: Student, deadline: datetime):
    """
    to get last commit Unix epoch timestamp https://stackoverflow.com/a/64789296/3504748
    'git log -1 --format=%ct'
    'git --git-dir {repo_dir}/.git log -1 --format=%ct'

    and compare it to the given deadline.

    :param student
    :param deadline: project deadline
    """
    commits_dt = subprocess.run(["git", "--git-dir", f"{student.get_repo_local_location()}/.git", "log", "-1",
                                 "--format=%ct"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if commits_dt.returncode != 0:
        message = f"Could not get the last commit date for {student.get_full_name()}. Error: {commits_dt.stderr}"
        result = False
        logging.error(message)
    else:
        last_change_dt = datetime.datetime.fromtimestamp(int(commits_dt.stdout.decode().strip()))  # .strftime('%c')
        if last_change_dt <= deadline:
            result = True
            message = f"On time (last change='{last_change_dt}' < deadline='{deadline}')"
            logging.debug(message)
        else:
            result = False
            message = f"Late (last change='{last_change_dt}' > deadline='{deadline}'), " \
                      f"{student.get_grading_rubric().late_fee_per_day*100}% will be deducted for each day."
            logging.debug(message)
            student.get_grading_rubric().is_late = True

            # we want to find the number of days even if it is part of a day.
            # for example an assignment that is late 3 hours is 0.125 days late
            secs_per_day = 24 * 60 * 60  # hour * min * sec
            time_diff = last_change_dt - deadline
            student.get_grading_rubric().late_days_count = time_diff.total_seconds() / secs_per_day

    return result, message
