# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 21:15:53 2020

@author: ashmui
"""

import pandas as pd
import numpy as np
from datetime import datetime

storageloc='C:/Users/ashmui/Downloads/Home_Energy/'

#the energy files have 2 sections: a 2-field header and a 25 field body that starts at line 14
df1=pd.read_csv(storageloc+'20201101_hourly_kwh.csv',skiprows=12)

#rename the unnamed column
df1.rename(columns = {'Unnamed: 0':'date'}, inplace = True)

#print info about dataframe
df1.info(verbose=True)

#solution 1
df2=pd.melt(df1, id_vars=['date'], var_name='time', value_name='kwh')

df2['datetime']=pd.to_datetime(df2['date']+' '+df2['time'],format="%m/%d/%Y %I:%M %p")

df2['hour']=df2['datetime'].dt.hour

#df2 = df2.drop(columns=["date", "time"])

df2.sort_values('datetime', inplace=True)

#df2.index=df2['datetime']

df2.plot('datetime', 'kwh', kind='bar')

#access date column as series
#date=orig.date

#access hour0 as series
#hour=orig.hour0

#convert into a long table with date column, hour column, and kWh column
#orig_t=orig.transpose()

#orig_stack=orig.stack(0)

#stack=pd.DataFrame(index=date,data=orig_t)

