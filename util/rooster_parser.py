import csv

import constants


# region Constants
STUDENT_ID_INDEX = 0
STUDENT_NAME_INDEX = 1
# endregion


class RoosterParser:
    def __init__(self, rooster_file_location: str):
        self.__rooster_file_location = rooster_file_location
        self.__student_list = {}
        self.__parse()

    def __parse(self):
        with open(self.__rooster_file_location) as rooster_file:
            rooster_reader = csv.reader(rooster_file, delimiter='\t', quotechar='"')
            for student in rooster_reader:
                self.__add_student(student)

    def __add_student(self, student: list):
        student_id = student[STUDENT_ID_INDEX]
        student_name = student[STUDENT_NAME_INDEX].lower()
        student_name = student_name.translate(dict.fromkeys(map(ord, constants.STUDENT_NAME_EXCLUDE_CHARS)))
        self.__student_list[student_name] = student_id

    def get_student(self, student_name):
        return self.__student_list.get(student_name, 'N/A')

    def get_student_name_list(self):
        return self.__student_list.keys()

    def print_rooster(self):
        for x, y in self.__student_list.items():
            print(x, y)
