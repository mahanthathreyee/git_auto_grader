import os
import git
import subprocess

import constants


class GitHandler:

    def __init__(self, dir_location):
        self._dir_location = dir_location

    def __is_git_init(self):
        try:
            self._repo = git.Repo(self._dir_location)
            self._git_init = True
        except git.InvalidGitRepositoryError:
            self._git_init = False

        return self._git_init

    def __is_repo_dirty(self):
        return self._git_init and not self._repo.is_dirty()

    def __file_check(self):
        if not self._git_init:
            return False

        err_file = constants.DEFAULT_FSCK_ERROR_LOG_FILE

        os.chdir(self._dir_location)
        with open(err_file, 'w') as fsck_result:
            subprocess.call(['git', 'fsck'], stderr=fsck_result)
            if os.stat(err_file).st_size == 0:
                return True

        return False

    def __get_commit_count(self):
        if not self._git_init:
            return -1
        return len(list(self._repo.iter_commits()))

    def run_checks(self):
        return [self.__is_git_init(), self.__is_repo_dirty(), self.__file_check(), self.__get_commit_count()]
