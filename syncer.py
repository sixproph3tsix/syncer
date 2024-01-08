import os
import shutil
import time
from datetime import datetime

def get_file_metadata(file_path):
    try:
        metadata = os.stat(file_path)
        return {
            'size': metadata.st_size,
            'last_modified': time.ctime(metadata.st_mtime),
            'creation_time': time.ctime(metadata.st_ctime)
        }
    except FileNotFoundError:
        return None

def compare_metadata(file1, file2):
    metadata1 = get_file_metadata(file1)
    metadata2 = get_file_metadata(file2)

    if not metadata1 or not metadata2:
        return "One or both files not found."
    comparison_result = {}
    for key in metadata1:
        comparison_result[key] = (metadata1[key] == metadata2[key], metadata1[key], metadata2[key])

    return comparison_result

def trunc_str(string):
    mxlength = 80
    if len(string) > mxlength:
        return string[:mxlength - 3] + "..."
    return string

def log_it(log_folder_path, **kwargs):
    timestamp = datetime.now().strftime("%Y %m %d %H %M %S")
    log_entry = f"{timestamp}   " + trunc_str("   ".join(f"{value}" for key, value in kwargs.items()))
    log_file_path = os.path.join(log_folder_path, 'log.txt')
    with open(log_file_path, "a") as file:
        file.write(log_entry + "\n")

def syncer():
    
    while True:
        
        # Get current date as a string in YYYY_MM_DD format
        str_current_date = datetime.now().strftime("%Y_%m_%d")
        
        # Paths for data transfer
        pathFrom = r'/mnt/two_tb/syncthing/syncthing/Highside/Zer/Camera' # Replace with your source directory path
        pathDest = r'/mnt/two_tb/syncthing_backup' # Replace with your destination directory path
        
        # Full path of the destination folder
        dest_folder = os.path.join(pathDest, str_current_date)
        
        # Check if the folder exists in pathDest with the name str_current_date
        if not os.path.exists(dest_folder):
            
            # If the folder does not exist, create it
            os.makedirs(dest_folder)
            
            # Logger
            log_it(pathDest, action='MKFLDR', folder=str_current_date)
        
        # Iterate through files in pathFrom
        for file in os.listdir(pathFrom):
            source_file = os.path.join(pathFrom, file)
            destination_file = os.path.join(dest_folder, file)
        
            # Check if file does not exist in pathDest/str_current_date
            if not os.path.exists(destination_file):
                
                # Copy file to pathDest
                shutil.copy(source_file, destination_file)
                
                # Logger
                log_it(pathDest, action='MKFILE', file=file)
                
            else:
                
                # If file exists, compare metadata.
                exists = compare_metadata(source_file, destination_file)
                
                # Logger
                # log_it(pathDest, action='NO ACT', file=file)
                continue
        
        
        
        time.sleep(5)
        
syncer()
