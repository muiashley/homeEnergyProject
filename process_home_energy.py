# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 12:05:18 2020

@author: ashmui
"""

import os, glob
import pandas as pd
import numpy as np
from datetime import datetime

#loop through a directory and process all files

path = os.getcwd()

path='C:/Users/ashmui/Downloads/Home_Energy'

print(path)


all_files = glob.glob(os.path.join(path, "*_hourly_kwh*.csv"))
df_from_each_file = (pd.read_csv(f, sep=',',skiprows=12) for f in all_files)
df_merged   = pd.concat(df_from_each_file, ignore_index=True)


df_merged.to_csv( "merged.csv")
   
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
df2.to_csv(path+'/full_data.csv', index = True)
