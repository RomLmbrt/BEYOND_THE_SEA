import datetime
import os
import pandas as pd

from Data_extract import extract_probe_data, extract_cyclops_data

def research_files_time(
        test_time : datetime.time, 
    ) -> dict :
    """research in the data folder the probe and cyclops files that contain the very hour we look for 

    Args:
        time (datetime.time): the test time we look for

    Returns:
        dict: a dictionary object
    """

    file_path_probe_cyclops = {
        "file_path_probe" : "",
        "file_path_cyclops" : "",
        }

    # We start with the probe files...
    folder_path = os.path.join(os.getcwd(), "data","Probe")

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # ensure it is a .txt file
            file_path = os.path.join(folder_path, filename)
            df_probe = extract_probe_data(file_path)
            # Look for the same hour and minute but doesn't care about day, second, etc...
            if ((df_probe['Time_UTC'].dt.hour == test_time.hour) & (df_probe['Time_UTC'].dt.minute == test_time.minute)).any():
                file_path_probe_cyclops["file_path_probe"] = file_path
    
    # Check that there is such a probe file
    if file_path_probe_cyclops["file_path_probe"] == "" :
        print(f'ERROR : there is no probe file that contains {test_time}')
        return()

    # ... Then we do the same with the cyclops files :
    folder_path = os.path.join(os.getcwd(), "data","Cyclops")

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):  # ensure it is a .csv file
            file_path = os.path.join(folder_path, filename)
            df_cyclops = extract_cyclops_data(file_path)

            if ((df_cyclops['Time_UTC'].dt.hour == test_time.hour) & (df_cyclops['Time_UTC'].dt.minute == test_time.minute)).any():
                file_path_probe_cyclops["file_path_cyclops"] = file_path
    
    # Check that there is such a cyclops file
    if file_path_probe_cyclops["file_path_cyclops"] == "" :
        print(f'ERROR : there is no cyclops file that contains {test_time}')
        return()
    
    return(file_path_probe_cyclops)