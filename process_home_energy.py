##################################################
## Name:                     process_home_energy.py
## Purpose:                  loops through files downloaded from the Duke energy website, appends them together and creates a time series output CSV              
## Usage:                    must define path, which is the directory where the CSVs are located.  Enclosed in quotes.
## Input Files:              files named in the following format: YYYYMMDD_hourly_kwh.csv
## Output Files:             path/outputCSVname, path/appended_raws
## Assumptions/Dependencies: all input CSV files are located in the path dir.  Output file is also saved in the path dir.
##################################################

import os, glob
import pandas as pd

#loop through a directory and process all files
def import_all(path,outputCSVname):
    
    all_files = glob.glob(os.path.join(path, "*_hourly_kwh*.csv"))
    df_from_each_file = (pd.read_csv(f, sep=',',skiprows=12) for f in all_files)
    df_merged   = pd.concat(df_from_each_file, ignore_index=True)
    
    
    df_merged.to_csv( path+"appended_raws.csv")
       
    #rename the unnamed column
    df_merged.rename(columns = {'Unnamed: 0':'date'}, inplace = True)
    
    #restructure from wide to time series data
    df2=pd.melt(df_merged, id_vars=['date'], var_name='time', value_name='kwh')
    
    #################################
    #   create datetime variables   #
    #################################
    
    #datetime
    df2['datetime']=pd.to_datetime(df2['date']+' '+df2['time'],format="%m/%d/%Y %I:%M %p")
    
    #date, time
    df2['date']=pd.to_datetime(df2['date']).dt.date
    df2['time']=pd.to_datetime(df2['time']).dt.time
    
    #hour
    df2['hour']=df2['datetime'].dt.hour
    
    
    #################################
    #set datetime as index and sort #
    #################################
    df2.set_index(keys='datetime',inplace=True)
    df2.sort_values('datetime', inplace=True)
    
    #################################
    #       plot                    #      
    #################################
    df2['kwh'].plot()
    
    
    #################################
    #     export                    #      
    #################################
    df2.to_csv(path+'/' + outputCSVname, index = True)
    
    print('Import all complete.  Output CSV written to '+ path +'/' + outputCSVname)
    
import_all(path='C:/Users/ashmui/Downloads/Home_Energy',outputCSVname='finalHomeEnergy.csv')

