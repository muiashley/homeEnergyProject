##################################################
## Name:                     process_home_energy.py
## Purpose:                  loops through files downloaded from the Duke energy website, appends them together and creates a time series output CSV              
## Usage:                    must define path, which is the directory where the CSVs are located.  Enclosed in quotes.
## Input Files:              files named in the following format: YYYYMMDD_hourly_kwh.csv
## Output Files:             path/outputCSVname, path/appended_raws
## Assumptions/Dependencies: all input CSV files are located in the path dir.  Output file is also saved in the path dir.
## Revisions:
#            28DEC2020 add min max date ranges in output text and summary statistics after processing
#            29DEC2020 add deduping and weather callout and merge
##################################################

import os, glob
import pandas as pd
import import_weather
from datetime import datetime
from datetime import timedelta


#############################################
#      upfront definitions - user input     #
############################################# 
this_zipcode=27612
this_path='C:/Users/ashmui/Downloads/Home_Energy'
this_outputCSVname='finalHomeEnergy.csv'


#################################
#      start script             #
#################################  

#loop through a directory and process all files
def import_all(path,outputCSVname):
    
    all_files = glob.glob(os.path.join(path, "*_hourly_kwh*.csv"))
    
    df_from_each_file = (pd.read_csv(f, sep=',',skiprows=12) for f in all_files)
    df_appended   = pd.concat(df_from_each_file, ignore_index=True)

    #include source file name when reading in
    df_appended=pd.DataFrame()
    for f in all_files:
        print('processing file '+f.replace(path+'\\',''))
        temp_df=pd.read_csv(f, sep=',',skiprows=12)  
        temp_df['origin_file']=f.split('\\')[-1]
        df_appended=df_appended.append(temp_df)
    
    #export the appended files to another csv file
    df_appended.to_csv( path+"appended_raws.csv")
       
    #rename the unnamed column
    df_appended.rename(columns = {'Unnamed: 0':'date'}, inplace = True)
    
    #restructure from wide to time series data
    out_df=pd.melt(df_appended, id_vars=['origin_file','date'], var_name='time', value_name='kwh')
    
    #################################
    #   create datetime variables   #
    #################################
    
    #create datetime and sort by it
    out_df['datetime']=pd.to_datetime(out_df['date']+' '+out_df['time'],format="%m/%d/%Y %I:%M %p")
    out_df.sort_values('datetime', inplace=True)
        
    #remove duplicates on datetime column in case there are any
    out_df=out_df.drop_duplicates(['datetime'])
    
    #date, time
    out_df['date']=pd.to_datetime(out_df['date']).dt.date
    out_df['time']=pd.to_datetime(out_df['time']).dt.time
    
    #hour
    out_df['hour']=out_df['datetime'].dt.hour
    
    
    #################################
    #set datetime as index and sort #
    #################################
    
    #make a duplicate copy of datetime for the index
    out_df['datetime2']=out_df['datetime']
    out_df.set_index(keys='datetime2',inplace=True)
    
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
    
energy_df = import_all(path=this_path,outputCSVname=this_outputCSVname)

energy_df['kwh'].plot()

#################################
# calculate summary statistics  #
#################################

#summary statistics for kwh for entire dataset
print('summary statistics for kwh for entire dataset')
all_summary=energy_df["kwh"].describe()

#summary statistics for kwh by day
print('summary statistics for kwh by day')
by_day_summary=energy_df[["date","kwh"]].groupby("date").describe()

min_date=energy_df["date"].min()
max_date=energy_df["date"].max()

mid_date=min_date+timedelta(days=14) 

#################################
# obtain weather data for dates #
#################################
output_weather_df1=import_weather.main(startDate=str(min_date),endDate=str(mid_date),zipcode=str(this_zipcode))

output_weather_df2=import_weather.main(startDate=str(mid_date),endDate=str(max_date),zipcode=str(this_zipcode))

weather_df=output_weather_df1.append(output_weather_df2)
weather_df['datetime']=pd.to_datetime(weather_df['datetime'],format="%m/%d/%Y %H:%M:%S")

weather_df=weather_df.drop_duplicates(['datetime'])

#################################
# merge kWh df to weather df   #
################################
energy_wth=pd.merge(energy_df,weather_df,how='left',on='datetime')

by_day_wth_summary=energy_wth[["date","kwh"]].groupby("date").describe()
