import os
import sys
import csv

import constants
import util.file_handler as file_handler
from util.rooster_parser import RoosterParser
from util.git_handler import GitHandler

import util.grader_style_a1_v2 as a0
import pathlib
import util.TA as TA
import zipfile
import glob

global counter
counter = 1

def process_student_submission():
    student_name = submission_zip.split(file_name_separator)[constants.FILE_STUDENT_NAME_INDEX]
    student_id = rooster.get_student(student_name)
    student_id = student_id if student_id else "unknown_student_id"
    print("Processing student: " + student_name + "(" + str(student_id) + ")")

    if os.path.isdir(submission_dir_location + '/' + submission_zip):
        file_handler.extract_zip_file(submission_dir_location + '/' + submission_zip, output_dir)
        print("Skipped file: " + submission_zip)
    checks = [False] * 4
    if os.path.exists(output_dir):
        repo = GitHandler(output_dir)
        checks = repo.run_checks()
        file_handler.delete_dir(output_dir)

    student_row = [student_id, student_name] + checks
    student_validation.append(student_row)

    


def write_student_validation():
    sorted_results = sorted(student_validation, key=lambda x: x[1])
    with open(constants.DEFAULT_VALIDATION_OUTPUT_FILE, 'w') as out_file:
        csvwriter = csv.writer(out_file)
        csvwriter.writerow(constants.OUTPUT_COLUMNS)
        csvwriter.writerows(sorted_results)


def A0_write_student_validation(filePath):
    with open(filePath, 'w') as out_file:
        csvwriter = csv.writer(out_file)
        csvwriter.writerow()
        csvwriter.writerows(student_validation)

    return

def grader(folder,f,studentDict):

    global counter

    for s in studentDict:
        if(s in str(f)):
            student = s
            break

    lst = [student]
    folder = os.path.dirname(folder)
    exclude_file_list = ['a1_grader_style.py', 'a1_w2023_grader.py',
                         'a1_validitychecker_v2023w.py']
    max_points_to_deduct_style = 4
    max_points_to_deduct_readme = 1

    try:
        style_deduction = a0.calculate_all_grade_deductions(folder, exclude_file_list,max_points_to_deduct_style ,max_points_to_deduct_readme)
    
    except Exception as e:
        with open("./fail_to_grade.txt", "a+") as file1:
                    file1.write(str(f))
                    file1.write("\n")
                    file1.write(str(folder))
                    file1.write("\n")
                    file1.write(str(e))
                    file1.write("\n")
                    file1.write("\n")
        return
    
    lst.append(counter)
    lst.append(str(style_deduction['frac_style_ded']))
    lst.append(str(style_deduction['frac_readme_ded']))
    lst.append(str(style_deduction['points_style_ded']))
    lst.append(str(style_deduction['points_readme_ded']))
    lst.append(str(style_deduction['total_ded']))
    counter += 1

    with open("/Users/adithya/Desktop/grades.csv", "a+",newline='') as file1:
        csvwriter = csv.writer(file1)
        csvwriter.writerow(lst)

    return

#------------------------------------------------------------------
def runAutograder(folderPath,studentDict):
    p = pathlib.Path(folderPath)
    ctr = 0
    for f in p.iterdir():
        temp_folder_path = folderPath+'/p'+str(ctr)
        if(not os.path.exists(temp_folder_path)):
            try:
                os.mkdir(temp_folder_path)
            except:
                print("Please Enable permissions")
                print("Alternatively, Please create folders with names 'G0','G1'... so on in the submissions directory")
        
        d = os.path.join(temp_folder_path, f)
        if os.path.isdir(d):
                continue
        
        try:
            with zipfile.ZipFile(f, 'r') as zip_ref:
                zip_ref.extractall(temp_folder_path)
        
            depth = ''
            flag = False
            for i in range(10):
                for name in glob.glob(temp_folder_path + depth + '/*.py'):
                    #print(name)
                    grader(name,f,studentDict)
                    flag = True
                    break
                depth = '/**' + depth

            if not flag:   
                with open("./fail_to_find_file.txt", "a+") as file1:
                    file1.write(str(f))
                    file1.write("\n")
                    file1.write(str(temp_folder_path))
                    file1.write("\n")
                    file1.write("\n")

        except Exception as e: 
            with open("./fail_to_unzip.txt", "a+") as file1:
                file1.write(str(f))
                file1.write("\n")
                file1.write(str(temp_folder_path))
                file1.write("\n")
                file1.write(str(e))
                file1.write("\n")
                file1.write("\n")

        ctr+=1
    

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

    #Possible Code flow - Execute splitter to put into different groups 
    # Then execute git checker for each of the folders
    # Then execute the autograder script

    studentDict,numGroups,directoryPath = TA.initFunction()
    for i in range(numGroups):
        directory = "G"+str(i)
        #print(directoryPath)
        path = directoryPath + directory
        runAutograder(path,studentDict)
        #break
