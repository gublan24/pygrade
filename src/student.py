__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

import os
from rubric import Rubric


class Student:

    def __init__(self, std_id: str, key_file_full_path: str, key_file_name: str):
        """

        :param std_id:
        :param key_file_full_path:
        :param key_file_name:
        """
        self._std_id = std_id
        self.key_file_dir_full_path = key_file_full_path
        self.key_file_name = key_file_name

        self._first_name = None
        self._last_name = None
        self._repo_link = None
        self._repo_local_full_path = None

        self.data = {}

        self.grades = Rubric()

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get_std_id(self) -> str:
        return self._std_id

    def get_ini_root_dir(self) -> str:
        return self.key_file_dir_full_path

    def get_ini_full_path(self) -> str:
        return f"{self.key_file_dir_full_path}/{self.key_file_name}"

    def set_name(self, full_name: str):
        """
        Names are usually broken by spaces. We assume we get a "first last" names only. If there are more than two
        words then the anything beyond the first word is considered a last name.

        :param full_name: A string with the full name of student (e.g. "FirstName LastName")
        """
        full_name_list= full_name.split(" ")
        if len(full_name_list) == 1:
            # We got one very long string!
            self._first_name = full_name_list[0]
        elif len(full_name_list) == 2:
            # this is the perfect case
            self._first_name = full_name_list[0]
            self._last_name = full_name_list[1]
        else: # the list must have more than two words
            self._first_name = full_name_list[0]
            self._last_name = " ".join(full_name_list[1:])

    def get_first_name(self) -> str:
        if self._first_name is None:
            return "Anonymous"
        else:
            return self._first_name

    def get_last_name(self) -> str:
        if self._last_name is None:
            return "Anonymous"
        else:
            return self._last_name

    def get_full_name(self) -> str:
        if self._first_name is None and self._last_name is None:
            return "Anonymous Anonymous"
        elif self._first_name is not None and self._last_name is None:
            return f"{self._first_name} NoLastName"
        else:
            return f"{self._first_name} {self._last_name}"

    def set_repo_link(self, repo_link: str):
        """
        We store the given value as it is we don't check for any valid pattern (although we could). The aim, is (1) to
        simplify this task and (2) fail later if the link is broken with a message that is more descriptive.

        :param repo_link:
        :return:
        """
        self._repo_link = repo_link

    def get_repo_link(self) -> str:
        """
        Get the repo link as it is stored. This should not be called before even setting the link! Thus, we through
        an error.
        :return: The link to the git repo.
        """
        if self._repo_link is not None:
            return self._repo_link
        else:
            return "NoRepoGiven"

    def set_repo_local_location(self, full_path: str):
        self._repo_local_full_path = full_path

    def get_repo_local_location(self) -> str:
        if self._repo_local_full_path is not None:
            return self._repo_local_full_path
        else:
            return "NoLocalClone"

    def get_obscure_rep_local_location(self):
        if self._repo_local_full_path is not None:
            all_repos_dir = os.path.basename(os.path.dirname(self._repo_local_full_path))
            this_repo_dir = os.path.basename(self._repo_local_full_path)
            return f"~/{all_repos_dir}/{this_repo_dir}"
        else:
            return "NoLocalRepo"

    def set_grading_rubric(self, rubric: Rubric):
        self.grades = rubric

    def get_grading_rubric(self) -> Rubric:
        return self.grades
