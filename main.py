import os
import sys
import csv

import constants
import util.file_handler as file_handler
from util.rooster_parser import RoosterParser
from util.git_handler import GitHandler


def process_student_submission():
    student_name = submission_zip.split(file_name_separator)[constants.FILE_STUDENT_NAME_INDEX]
    student_id = rooster.get_student(student_name)

    file_handler.extract_zip_file(submission_dir_location + '/' + submission_zip, output_dir)
    repo = GitHandler(output_dir)

    student_row = [student_id, student_name] + repo.run_checks()
    student_validation.append(student_row)

    file_handler.delete_dir(output_dir)


def write_student_validation():
    with open(constants.DEFAULT_VALIDATION_OUTPUT_FILE, 'w') as out_file:
        csvwriter = csv.writer(out_file)
        csvwriter.writerow(constants.OUTPUT_COLUMNS)
        csvwriter.writerows(student_validation)


if __name__ == '__main__':
    student_validation = []
    output_dir = constants.DEFAULT_ZIP_EXTRACT_OUTPUT_DIR
    file_name_separator = constants.DEFAULT_SUBMISSION_FILE_NAME_SEPARATOR

    rooster_file_location = sys.argv[1]
    submission_dir_location = sys.argv[2]

    rooster = RoosterParser(rooster_file_location)
    submission_list = file_handler.get_dir_files(submission_dir_location)

    for submission_zip in submission_list:
        process_student_submission()

    os.chdir(constants.BASE_DIR)
    write_student_validation()
