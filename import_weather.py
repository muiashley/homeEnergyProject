import requests
import time
import urllib2
import getpass
import string
import datetime
import csv
import pandas as pd
import http.client

import os.path
from os import path

import sys
from StringIO import StringIO


def main(startDate, endDate, zipcode):

    conn = http.client.HTTPSConnection("visual-crossing-weather.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "f3a577a161msh6cc58c82fdbce89p15cf8fjsn37074354d9ca",
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
        }
    
    conn.request("GET", 
                 "/history?startDateTime="+startDate
                 +"T00%3A00%3A00&aggregateHours=1"
                 +"&location="+zipcode
                 +"&endDateTime="+endDate
                 +"T00%3A00%3A00&unitGroup=us&contentType=csv&shortColumnNames=True"
                 ,headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    data=StringIO(data)
    
    weather_df = pd.read_csv(data)
    return weather_df
    
#sample call
#output_weather_df=import_weather(startDate="2019-01-03",endDate="2019-01-04",zipcode="27612")