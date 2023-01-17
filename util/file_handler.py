import os
import zipfile
import shutil


def get_dir_files(dir_location: str) -> list[str]:
    return os.listdir(dir_location)


def extract_zip_file(input_zip_file: str, output_dir: str):
    with zipfile.ZipFile(input_zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def delete_dir(dir_location: str):
    shutil.rmtree(dir_location)
