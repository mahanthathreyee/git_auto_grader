import os
import glob
import shutil


def group_divider(directory_path, student_names, num_groups):
    num_submissions = len(glob.glob(directory_path + '/*.zip'))
    students_per_group = int(num_submissions / num_groups)

    num_students_in_group = 0
    current_group = 0
    restart = False

    for student in student_names:
        match = glob.glob(directory_path + "/" + student + "*")
        if len(match) != 0:
            if num_students_in_group < students_per_group:
                num_students_in_group += 1
            else:
                current_group += 1
                if current_group == num_groups:
                    current_group = 0
                    restart = True

                if restart:
                    num_students_in_group = students_per_group - 1
                else:
                    num_students_in_group = 1

            loc = "/G" + str(current_group) + "/"
            path = directory_path + loc
            shutil.move(match[-1], path)


def assign(directory_path, student_names, num_groups):
    for i in range(num_groups):
        directory = "G" + str(i)
        path = directory_path + directory
        if not os.path.exists(path):
            try:
                os.mkdir(path)

            except PermissionError:
                print("Please Enable permissions")
                print("Alternatively, Please create " + str(
                    num_groups) + " folders with names 'G0','G1'... so on in the submissions directory")

    group_divider(directory_path, student_names, num_groups)

    total_sub = 0
    for i in range(num_groups):
        directory = "G" + str(i)
        path = directory_path + directory
        num_sub = len(glob.glob(path + '/*'))
        print("The number of submissions in group " + str(i) + " is " + str(num_sub))
        total_sub += num_sub

    print("The total number of submissions are " + str(total_sub))

    return
