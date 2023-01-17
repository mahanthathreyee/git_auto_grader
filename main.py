import sys

import constants
import util.file_handler as file_handler
from util.rooster_parser import RoosterParser
from util.git_handler import GitHandler


def process_student_submission():
    student_name = submission_zip.split(file_name_separator)[constants.FILE_STUDENT_NAME_INDEX]
    student_id = rooster.get_student(student_name)
    file_handler.extract_zip_file(submission_dir_location + '/' + submission_zip, output_dir)

    repo = GitHandler(output_dir)
    student_validation[student_id] = repo.run_checks()

    file_handler.delete_dir(output_dir)


if __name__ == '__main__':
    student_validation = {}
    output_dir = constants.DEFAULT_ZIP_EXTRACT_OUTPUT_DIR
    file_name_separator = constants.DEFAULT_SUBMISSION_FILE_NAME_SEPARATOR

    rooster_file_location = sys.argv[1]
    submission_dir_location = sys.argv[2]

    rooster = RoosterParser(rooster_file_location)
    submission_list = file_handler.get_dir_files(submission_dir_location)

    for submission_zip in submission_list:
        process_student_submission()

    print(student_validation)
