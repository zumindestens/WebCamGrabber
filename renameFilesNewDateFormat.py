import os
import sys
import re

base_folder = sys.argv[1]

# file names first
for root, dirs, files in os.walk(base_folder):
    for name in files:
        # search all files that need to be renamed
        # ignore file if name is in wrong format
        match_file_name = re.search("^([0-9a-zA-Z]+)-([0-5][0-9])[-_:]([0-5][0-9])\.([a-zA-Z]+)", name)
        if match_file_name:
            entity_name = match_file_name.group(1)
            hours = match_file_name.group(2)
            minutes = match_file_name.group(3)

            file_format = match_file_name.group(4)
            seconds = "99"

            # get data from dir
            dir_name = os.path.dirname(os.path.join(root, name))
            # NOTE first group not used this time
            match_dir_name = re.search("^(.+?)-([0-9]+)-([0-3][0-9])-([0-9]+)", dir_name)
            if not match_dir_name:
                raise Exception
            if len(match_dir_name.group(2)) == 2:
                day = match_dir_name.group(2)
                month = match_dir_name.group(3)
                year = match_dir_name.group(4)
            else:
                # dir already has been renamed
                day = match_dir_name.group(4)
                month = match_dir_name.group(3)
                year = match_dir_name.group(2)

            new_file_name = entity_name + "-" + year + "-" + month + "-" + day + "-" + hours + "_" + minutes + "_" + \
                            seconds + "." + file_format

            print(os.path.join(root, new_file_name))
            os.rename(os.path.join(root, name), os.path.join(root, new_file_name))

# dir names second
for root, dirs, files in os.walk(base_folder):
    for name in dirs:
        match_dir_name = re.search("^(.+?)-([0-9]+)-([0-3][0-9])-([0-9]+)", name)
        if match_dir_name and len(match_dir_name.group(2)) == 2:
            entity_name = match_dir_name.group(1)
            day = match_dir_name.group(2)
            month = match_dir_name.group(3)
            year = match_dir_name.group(4)

            new_dir_name = entity_name + "-" + year + "-" + month + "-" + day
            print(os.path.join(root, new_dir_name))
            os.rename(os.path.join(root, name), os.path.join(root, new_dir_name))
