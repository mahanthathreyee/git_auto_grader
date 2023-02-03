#
# grader_style.py : A simple grader for code style for the ICS32 course
#
# This code is customized for the A1 assignment
#
import pycodestyle
import sys
import ast
import pathlib
import os


def get_total_number_of_lines(filename) -> int:
    n_lines = 0
    docstring = False
    f_in = open(filename, "r")
    for line in f_in:
        n_lines = n_lines + 1
    f_in.close()
    return n_lines


def get_real_loc_from_parsed_ast(filename) -> int:
    f_in = open(filename, "r")
    data_f_in = f_in.read()
    f_in.close()
    # Create an AST object such that we can calculate the real LOCs
    ast_f_in = ast.parse(data_f_in)
    str_ast_f_in = str.splitlines(ast.unparse(ast_f_in))
    # Remove any docstring, as they are not executable code
    code_only = __remove_docstring_from_list(str_ast_f_in)
    return len(code_only)


def __remove_docstring_from_list(codelist) -> list:
    res_list = []
    for line in codelist:
        # only append the line to the resulting list if
        # the line is not a docstring
        if line.lstrip().startswith("'"):
            continue
        else:
            res_list.append(line)
    return res_list


def get_number_of_style_issues(filename) -> int:
    # Instantiate a pycodestyle PEP8 style checker
    style_checker = pycodestyle.StyleGuide(quiet=True)
    # Use the style checker to get the number of issues
    # in the python code file
    res_chk = style_checker.input_file(filename=filename)
    return res_chk


def get_style_metrics(filename) -> dict:
    n_loc_file = get_real_loc_from_parsed_ast(filename)
    n_style_issues_file = get_number_of_style_issues(filename)
    n_lines_file = get_total_number_of_lines(filename)
    res_metrics = {
        "filename": filename,
        "n_loc": n_loc_file,
        "n_style_issues": n_style_issues_file,
        "n_lines": n_lines_file
    }
    return res_metrics


def get_style_metrics_for_multiplefiles(filename_list) -> list:
    res_metrics_list = []
    for filename in filename_list:
        res_metrics_list.append(get_style_metrics(filename))
    return res_metrics_list


def merge_style_metric(metrics_list) -> dict:
    total_loc = 0
    total_lines = 0
    total_issues = 0
    for metric in metrics_list:
        total_loc = total_loc + metric['n_loc']
        total_lines = total_lines + metric['n_lines']
        total_issues = total_issues + metric['n_style_issues']
    res_dict = {
        "total_loc": total_loc,
        "total_lines": total_lines,
        "total_style_issues": total_issues
    }
    return res_dict

'''
def print_style_issues_report_singlefile(filename):
    print(f'----------------------------------------------------------------')
    print(f'Report for file      : {filename}')
    print(f'----------------------------------------------------------------')
    sty_metrics = get_style_metrics(filename)
    print(f'----------------------------------------------------------------')
    print(f"PEP8 Style issues    : {sty_metrics['n_style_issues']}")
    print(f"Total lines in file  : {sty_metrics['n_lines']}")
    print(f"Total LOC in file    : {sty_metrics['n_loc']}")
    print("Issues / total lines : " +
          f"{sty_metrics['n_style_issues']/sty_metrics['n_lines']}")
    print("Issues / LOC         : " +
          f"{sty_metrics['n_style_issues']/sty_metrics['n_loc']}")
    print(f'----------------------------------------------------------------')
'''

def remove_files_from_list_of_files(path_list, exclude_list) -> list:
    res_list = []
    for path in path_list:
        found = False
        for ex_path in exclude_list:
            if path.name == ex_path:
                found = True
        if not found:
            res_list.append(path)
    return res_list


def calculate_style_grade_deduction(assignment_path, exclude_list) -> float:
    # Get the names of the Python codes in the assignment
    #Need to add a c heck to skip the virtual environment and  __mac
    files = [path for path in pathlib.Path(assignment_path).glob("*")
             if (path.is_file() and path.suffix == ".py")]
    # Remove filenames from the exclude_list
    clean_files = remove_files_from_list_of_files(files, exclude_list)
    multipleres = get_style_metrics_for_multiplefiles(clean_files)
    medict = merge_style_metric(multipleres)
    #print(medict)
    return medict['total_style_issues']/medict['total_loc']


def check_for_readme(path, possible_names) -> bool:
    exists = False
    for filename in possible_names:
        file_with_path = pathlib.Path(path) / pathlib.Path(filename)
        if file_with_path.exists():
            exists = True
    return exists


def check_for_readme_data(path, possible_names) -> bool:
    readme_bytes = 0
    for filename in possible_names:
        file_with_path = pathlib.Path(path) / pathlib.Path(filename)
        if file_with_path.exists():
            try:
                readme_in = open(file_with_path, "r")
                readme_in.seek(0, os.SEEK_END)
                readme_bytes = readme_in.tell()
            except OSError as oser:
                print("README could not be opened/read due to:", oser)
            else:
                readme_in.close()
    contain_data = False
    if readme_bytes > 10:
        # If the readme contains at least 10 bytes...
        contain_data = True
    return contain_data


def calculate_readme_deduction(path) -> float:
    readme_names = ['README', 'README.txt', 'README.md']
    readme_deduction = 0
    # Does a README exists?
    readme_exists = check_for_readme(path, readme_names)
    if readme_exists:
        # Does the README contains data?
        readme_contains_data = check_for_readme_data(path, readme_names)
        if not readme_contains_data:
            # If the readme exists but contains no data
            readme_deduction = 0.025
    else:
        # If there is no README in the assignment
        readme_deduction = 0.025
    return readme_deduction


def calculate_all_grade_deductions(assignment_path, exclude_file_list,
                                   max_deduction_style,
                                   max_deduction_readme) -> dict:
    style_deduction = calculate_style_grade_deduction(assignment_path,
                                                      exclude_file_list)
    frac_style_ded = round(style_deduction, 3)
    frac_readme_ded = round(
                           calculate_readme_deduction(assignment_path)/0.025,
                           3)
    points_style_ded = round(max_deduction_style * frac_style_ded, 3)
    points_readme_ded = round(max_deduction_readme * frac_readme_ded, 3)
    total_ded = round(points_style_ded + points_readme_ded, 1)
    res_dict = {
        "frac_style_ded": frac_style_ded,
        "frac_readme_ded": frac_readme_ded,
        "points_style_ded": points_style_ded,
        "points_readme_ded": points_readme_ded,
        "total_ded": total_ded
    }
    return res_dict


def print_all_grade_deductions(assignment_path, exclude_file_list,
                               max_deduction_style,
                               max_deduction_readme) -> None:
    print("------------------------------------------------------------------")
    print(f"Analysing grade deduction for path: {assignment_path}")
    style_deduction = calculate_all_grade_deductions(
                       assignment_path,
                       exclude_file_list, max_deduction_style,
                       max_deduction_readme)
    print("------------------------------------------------------------------")
    print("Deduction for PEP8 style issues [0-1]       : " +
          f"{style_deduction['frac_style_ded']}")
    print("Deduction for lacking a README file [0-1]   : " +
          f"{style_deduction['frac_readme_ded']}")
    print("------------------------------------------------------------------")
    print("Points deduction for PEP8 style [points]    : " +
          f"{style_deduction['points_style_ded']}")
    print("Points deduction for lack of README [points]: " +
          f"{style_deduction['points_readme_ded']}")
    print("------------------------------------------------------------------")
    print("Total assignment deduction [in points]      : " +
          f"{style_deduction['total_ded']}")
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    # ------------------------------------------------------------
    # Configuration parameters for ICS32 Assignment 1
    exclude_file_list = ['a1_grader_style.py', 'a1_w2023_grader.py',
                         'a1_validitychecker_v2023w.py']
    max_points_to_deduct_style = 4
    max_points_to_deduct_readme = 1
    # ------------------------------------------------------------
    print_all_grade_deductions(sys.argv[1], exclude_file_list,
                               max_points_to_deduct_style,
                               max_points_to_deduct_readme)
