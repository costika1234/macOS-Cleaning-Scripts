#!/usr/local/bin/python

import os
import re
import shutil
import subprocess

from datetime import datetime

IMESSAGE_ATTACHMENTS_PATH = '/Users/{0}/Library/Messages/Attachments/'.format(subprocess.check_output(['whoami']).strip())
DELETE_UNTIL_DATE = '9/01/2018'

def main():
    print('Cleaning iMessage...')

    no_deleted_files = 0
    delete_until_date = datetime.strptime(DELETE_UNTIL_DATE, "%d/%m/%Y")
    
    for root, directories, filenames in os.walk(IMESSAGE_ATTACHMENTS_PATH):
        # Skip the parent directory as we are dealing with files few levels deep.
        if root == IMESSAGE_ATTACHMENTS_PATH:
            continue

        for filename in filenames:
            path_to_file = os.path.join(root,filename)
            attachment_metadata = subprocess.check_output(['GetFileInfo', path_to_file])

            created_date_regex = re.search('created:\s+([\/0-9]+)', attachment_metadata)
            created_date = datetime.strptime(created_date_regex.group(1), '%m/%d/%Y')

            if created_date < delete_until_date:
                print 'Deleting file: {0}'.format(path_to_file)
                os.remove(path_to_file)
                no_deleted_files = no_deleted_files + 1

    no_empty_directories = 0

    # Value inferred from the directory tree in Finder.app.
    max_depth_level = 3
    depth_level = 0

    while depth_level < 3:
        for root, directories, filenames in os.walk(IMESSAGE_ATTACHMENTS_PATH):
            for directory in directories:
                path_to_dir = os.path.join(root, directory)
                if os.listdir(path_to_dir) == []:
                    print 'Deleting empty directory: {0}'.format(path_to_dir)
                    shutil.rmtree(path_to_dir, ignore_errors=True)
                    no_empty_directories = no_empty_directories + 1
        depth_level = depth_level + 1

    print('\nDeleted {0} files and deleted {1} empty directories\n'.format(no_deleted_files, no_empty_directories))

if __name__ == "__main__":
    main()
