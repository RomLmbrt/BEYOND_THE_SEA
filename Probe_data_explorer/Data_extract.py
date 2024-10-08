import pandas as pd
import numpy as np

def extract_probe_data(
        file_txt : str, 
        without_time_zero : bool = False
    ) -> pd.DataFrame :
    """Extract the data from the airspeed probe .txt file and calculate the True Air Speed from Quentin Aubourg's equations

    Args:
        file_txt (str): the relative path to the .txt file
        without_time_zero (bool): delete the logs without the time recorded

    Returns:
        pd.DataFrame: a pandas data frame object
    """

    # Read the .txt file
    df_probe = pd.read_csv(file_txt, sep=';')

    # Calculate the true air speed from the probe data
    df_probe["DP"] = df_probe["Pressure_Kiel"] / df_probe["Abs_Pressure"] * 0.966 # Pa
    df_probe["IAS_raw"] = (2/1.225*np.abs(df_probe["DP"]))**0.5 # m/s
    df_probe["IAS"] = -2.8209*10**(-4) * df_probe["IAS_raw"]**2 + 9.80669*10**(-1) * df_probe["IAS_raw"] + 4.74779*10**(-2) # m/s
    df_probe["Rho"]  = (1.1885*df_probe["Abs_Pressure"])*(293.15/(273.15+df_probe["Vector_Temp"]))# kg/m3
    df_probe["TAS"] = (1.225/df_probe["Rho"])**0.5 * df_probe["IAS"] # m/s
    df_probe["TAS_knots"] = df_probe["TAS"] * 1.94384 # knots

    # Write the time in a "datetime" format, with +2hours of time zone difference
    df_probe['UTC_h'] += 2
    df_probe['Time_UTC'] = pd.to_timedelta(
        df_probe['UTC_h'].astype(str) + 'h ' +
        df_probe['UTC_m'].astype(str) + 'm ' +
        df_probe['UTC_s'].astype(str) + 's'
    )
    df_probe['Time_UTC'] = pd.to_datetime('2000-01-01') + df_probe['Time_UTC']

    # Delete the logs without the time recorded
    if without_time_zero :
        df_probe = df_probe[df_probe['Time_UTC'] != pd.to_datetime('2000-01-01') + pd.to_timedelta('02:00:00')]

    return(df_probe)

def extract_cyclops_data(
        file_csv: str, 
    ) -> pd.DataFrame :
    """Extract the data from the cyclopes .csv file and adapt the time format

    Args:
        file_csv (str): the relative path to the .csv file

    Returns:
        pd.DataFrame: a pandas data frame object
    """

    # Read the .csv file
    df_cyclops = pd.read_csv(file_csv, sep=',', header =0)

    # Adapt the time format
    df_cyclops.rename(columns={'Timestamp': 'Time_UTC'}, inplace=True)
    df_cyclops["Time_UTC"] = pd.to_datetime(df_cyclops["Time_UTC"])

    return(df_cyclops)

def merge_df(
        df_probe: pd.DataFrame, 
        df_cyclops: pd.DataFrame, 
        save_result: bool = False,
        ) -> pd.DataFrame :
    """Merge both data frames synchonizing their times

    Args:
        df_probe (pd.DataFrame): the probe data frame
        df_cyclops (pd.DataFrame): the cyclopes data frame
        save_result (bool): save the result in the processed data folder

    Returns:
        pd.DataFrame: a pandas data frame object 
    """
    # Exctract hour, minute & second as keys for merging
    df_probe['hour'] = df_probe['Time_UTC'].dt.hour
    df_probe['minute'] = df_probe['Time_UTC'].dt.minute
    df_probe['second'] = df_probe['Time_UTC'].dt.second

    df_cyclops['hour'] = df_cyclops['Time_UTC'].dt.hour
    df_cyclops['minute'] = df_cyclops['Time_UTC'].dt.minute
    df_cyclops['second'] = df_cyclops['Time_UTC'].dt.second

    # Merge both files
    df_merged = pd.merge(df_probe, df_cyclops, on=['hour', 'minute', 'second'], how='inner')

    # Drop the hour, minute & second previously added
    df_merged.drop(columns=['hour', 'minute', 'second'], inplace=True)
    df_cyclops.drop(columns=['hour', 'minute', 'second'], inplace=True)
    df_probe.drop(columns=['hour', 'minute', 'second'], inplace=True)

    # Save the result in a .csv file
    if save_result :
        df_merged.to_csv(f'processed_data/result.csv', index=False)

    return(df_merged)