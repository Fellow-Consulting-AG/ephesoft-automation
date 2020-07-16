import datetime
import os
import yaml
from zipfile import ZipFile


def add_key_to_dicts(dicts, key):
    for dic in dicts:
        add_to_dict(dic, key)


def clear_dicts(dicts):
    for dic in dicts:
        dic.clear()


def add_to_dict(dictionary, key):
    if key not in dictionary:
        dictionary[key] = 0


def check_if_empty_or_none(val):
    return val == 'None' or val == '' or val is None


def add_count_to_dict(dictionary, key):
    if key not in dictionary:
        dictionary[key] = 0
    dict_val = dictionary[key]
    dictionary[key] = dict_val + 1


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def clean_value(val):
    if val is None:
        return val
    return val.replace(" ", "")


def extract_zip(file_path):
    dir = os.path.dirname(file_path)
    print(dir)
    #extracted_file_path = os.path.basename(file_path).replace(".zip", "")
    with ZipFile(file_path, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(path=dir)
    extracted_file_path = os.path.basename(file_path).replace(".zip", "")
    return combine_path(dir, extracted_file_path)
    #print(extracted_file_path)
    #return extracted_file_path


def get_configurations(file_path):
    if not os.path.isfile(file_path):
        print("Configurations file is missing")
        return

    with open(file_path, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        return cfg


def get_export_filename(cfg, base_dir, doc_name):
    output_dir = combine_path(base_dir,  cfg['output_dir'])

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if os.path.exists(output_dir):
        if cfg['output_file_naming_convention'] == 1:
            return combine_path(output_dir, doc_name + '.xlsx')
        elif cfg['output_file_naming_convention'] == 2:
            return combine_path(output_dir, doc_name + '-' + datetime.datetime.now().strftime("%d-%m-%Y") + '.xlsx')
        else:
            return combine_path(output_dir, doc_name + '-' + str(datetime.datetime.now().strftime("%d-%m-%Y  %H_%M_%S")) + '.xlsx')

    elif os.access(os.path.dirname(output_dir), os.W_OK):
        print("Error Exporting Results: Not enough privileges.")
        return None
    else:
        print("Error Exporting Results: Wrong path provided.")
        return None


def combine_path(directory, filename):
    if filename.startswith(directory):
        return filename
    else:
        return os.path.join(directory, filename)