##################################################
## Name:                     process_home_energy.py
## Purpose:                  loops through files downloaded from the Duke energy website, appends them together and creates a time series output CSV              
## Usage:                    must define path, which is the directory where the CSVs are located.  Enclosed in quotes.
## Input Files:              files named in the following format: YYYYMMDD_hourly_kwh.csv
## Output Files:             path/outputCSVname, path/appended_raws
## Assumptions/Dependencies: all input CSV files are located in the path dir.  Output file is also saved in the path dir.
## Revisions:
#            28DEC2020 add min max date ranges in output text and summary statistics after processing
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
    out_df=pd.melt(df_merged, id_vars=['date'], var_name='time', value_name='kwh')
    
    #################################
    #   create datetime variables   #
    #################################
    
    #datetime
    out_df['datetime']=pd.to_datetime(out_df['date']+' '+out_df['time'],format="%m/%d/%Y %I:%M %p")
    
    #date, time
    out_df['date']=pd.to_datetime(out_df['date']).dt.date
    out_df['time']=pd.to_datetime(out_df['time']).dt.time
    
    #hour
    out_df['hour']=out_df['datetime'].dt.hour
    
    
    #################################
    #set datetime as index and sort #
    #################################
    out_df.set_index(keys='datetime',inplace=True)
    out_df.sort_values('datetime', inplace=True)
    
    #################################
    #       plot                    #      
    #################################
    out_df['kwh'].plot()
    
    
    #################################
    #     export                    #      
    #################################
    out_df.to_csv(path+'/' + outputCSVname, index = True)
    
    
    
    #determine date range
    min_date=out_df["date"].min()
    max_date=out_df["date"].max()
    
    print('Import all complete for date ranges ' + str(min_date) + ' to ' + str(max_date) + '.  Output CSV written to '+ path +'/' + outputCSVname)
    
    return out_df
    
output_dataframe = import_all(path='C:/Users/ashmui/Downloads/Home_Energy',outputCSVname='finalHomeEnergy.csv')

output_dataframe['kwh'].plot()

#################################
# calculate summary statistics  #
#################################

#summary statistics for kwh for entire dataset
print('summary statistics for kwh for entire dataset')
output_dataframe["kwh"].describe()

#summary statistics for kwh by day
print('summary statistics for kwh by day')
output_dataframe[["date","kwh"]].groupby("date").describe()
