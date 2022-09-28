__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

import re
import os.path
import logging
import configparser
from typing import List

from pygrade.src import util
from pygrade.src import config
from pygrade.src.student import Student

logger = logging.getLogger(__name__)


def get_students_objects_from_path(key_files: List[str]) -> List[Student]:
    students = []
    student_ids = []  # this is for validation only
    for file_full_path in key_files:
        student_id = util.get_student_id_from_file_path(file_full_path)
        if student_id in student_ids:
            raise RuntimeError(f"We got the student is twice {student_id}!")
        else:
            student_ids.append(student_id)

        students.append(Student(student_id,
                                os.path.dirname(file_full_path),
                                os.path.basename(file_full_path)))
    return students


def dummy_get_file():
    return True, "Found a *.ini file!"


def get_name_from_ini(student: Student, section="DEFAULT"):
    """
    Read the author tag from the .ini file and store the value in the given student object. By the time you use this
    method the student object must have been initialized with the ini file location. This isto avoid matching errors
    between students and their ini.

    :param student: Student object.
    :param section: the section under which the key is stored in the ini file. Mostly [DEFAULT]
    :return:
    """
    ini = configparser.ConfigParser()

    try:
        ini.read(student.get_ini_full_path())
        logger.debug(f"Reading ini named '{student.get_ini_full_path()}' "
                     f"for student with id '{student.get_std_id()}' ...")

        name = ini[section]['author']
        name = strip_quotations(name)
    except BaseException as e:
        logger.warning(f"The file '{student.get_std_id()}' has a configuration issue for id 'author'. Error: {e}")
        result = f"Failed with error ({e})\n"
        return False, result
    else:
        if name.startswith("Your Name Here"):
            result = f"The author for sid='{student.get_std_id()}' was not given appropriately.\n" \
                     f"We expect 'FirstName LastName', but we got '{name}'."
            student.set_name(name)
            logger.debug(result)
            return False, result
        else:
            result = f"Got '{name}' for student with id='{student.get_std_id()}'"
            student.set_name(name)
            logger.debug(result)
            return True, result


def get_student_id_from_ini(student: Student, section="DEFAULT"):
    """
    Read the quid tag from the .ini file and validate that it matches what we have in record. This is sanity check and
    an important one as we don't want to mix grades.

    :param student: Student object.
    :param section: the section under which the key is stored in the ini file. Mostly [DEFAULT]
    :return:
    """
    ini = configparser.ConfigParser()

    try:
        ini.read(student.get_ini_full_path())
        logger.debug(f"Reading ini named '{student.get_ini_full_path()}' "
                     f"for student with id '{student.get_std_id()}' ...")
        student_id = ini[section]['quid']
        student_id = strip_quotations(student_id)
    except BaseException as e:
        logger.warning(f"The file '{student.get_std_id()}' has a configuration issue for id 'quid'. Error: {e}")
        result = f"Failed with error ({e})\n"
        return False, result
    else:
        result = f"Got '{ini[section]['quid']}' for student with id='{student.get_std_id()}'"
        if student.get_std_id() == student_id:
            result += ". The given id match the one in record!"
            logger.debug(result)
            return True, result
        else:
            result += ". The given id does NOT match the one in record!"
            logger.debug(result)
            return False, result


def get_student_repo_link_from_ini(student: Student, section="DEFAULT"):
    """
    Read the repo tag from the .ini file and store it as is. If the link is not correct or have any issues we will
    discover this when we clone the repo.

    :param student: Student object.
    :param section: the section under which the key is stored in the ini file. Mostly [DEFAULT]
    :return:
    """
    ini = configparser.ConfigParser()

    try:
        ini.read(student.get_ini_full_path())
        logger.debug(f"Reading ini named '{student.get_ini_full_path()}' "
                     f"for student with id '{student.get_std_id()}' ...")
        link = ini[section]['repo']
        link = strip_quotations(link)
    except BaseException as e:
        logger.warning(f"The file '{student.get_std_id()}' has a configuration issue for id 'repo'. Error: {e}")
        result = f"Failed with error ({e})\n"
        return False, result
    else:
        if is_our_repo(link, config.workspace, config.username):
            result = f"The link provided is the original class repo.\n" \
                     f"We expect 'git@bitbucket.org:username/projectname.git' that you own, but we got " \
                     f"'{link}'\n" \
                     f"No points (if any) will be given to this task, and we will not clone the repo."
            student.set_repo_link("ProvidedOriginalLink")
            logger.debug(result)
            return False, result
        elif not is_link_pattern_valid(link):
            result = f"The link provided doesn't match the link pattern we look for.\n" \
                     f"We expect 'git@bitbucket.org:username/projectname.git', but we got " \
                     f"'{student.get_repo_link()}'\n" \
                     f"No points (if any) will be given to this task, but we will try the link anyway."
            student.set_repo_link(link)
            logger.debug(result)
            return False, result
        else:
            result = f"Got a valid link '{link}' for student with id='{student.get_std_id()}'"
            student.set_repo_link(link)
            logger.debug(result)
            return True, result


def strip_quotations(text: str):
    """
    Students tend to surround their values (name, id, and link) with quotation marks. If that is the case,
    this method try to help by removing quotation marks only if they occur at start and end of the string.
    :param text:
    :return:
    """
    if text.startswith("'") and text.endswith("'"):
        return text.strip("\'")
    else:
        return text.strip('\"')


def is_link_pattern_valid(link: str) -> bool:
    """
    Check if the link given match the pattern we expect.
    sample patter: "git@bitbucket.org:username/projectname.git"
    :param link: The link to test.
    :return: True if the link matches our pattern, False otherwise.
    """
    patter = re.compile("^git@bitbucket\.org:(.+)\/(.+)\.git$")
    return bool(patter.match(link))


def is_our_repo(link: str, workspace_name: str, username: str) -> bool:
    """
    Check if the link given match the pattern for one of our repository.
    Some students will just give you the link you provided. And if you helped in some tasks originally,
    they will collect free points. Our repo should never be cloned as the student's repo.
    sample patter: "git@bitbucket.org:OUR_USERNAME/projectname.git"
    :param link: The link to test.
    :param workspace_name: 
    :param username:
    :return: True if the link matches our pattern, False otherwise.
    """
    pattern1 = re.compile(f"^git@bitbucket\.org:{workspace_name}\/(.+)\.git$")
    pattern2 = re.compile(f"^http(s{0,1}):\/\/bitbucket\.org\/{workspace_name}\/(.*)$")
    pattern3 = re.compile(f"^http(s{0,1}):\/\/{username}@bitbucket\.org\/{workspace_name}\/(.*)$")
    if bool(pattern1.match(link)) or bool(pattern2.match(link)) or bool(pattern3.match(link)):
        return True
    else:
        return False
