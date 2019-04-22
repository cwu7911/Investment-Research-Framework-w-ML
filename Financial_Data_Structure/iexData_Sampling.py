# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 12:43:51 2019

Data provided for free by IEX. View IEX’s Terms of Use.
@author: cwu7911
"""

import pandas as pd
import numpy as np 
import requests
import math
#get data through IEX

sym='SPY'

temp=requests.get('https://api.iextrading.com/1.0/stock/'+sym+'/chart/5y').json()

#sampling using daily volume bar or price bar, target the next decimal. i.e. daily volume  is 10, threshold is 100, closer to iid compared to time series(constant information flow)

def find_AvgSamplingMetrics(data=temp, metric='volume'):
    if metric == 'volume':
        return sum(d[metric] for d in data) / len(data)
    elif metric == 'dollar':
        return sum((d['high']+d['low'])*0.5*d['volume'] for d in data) / len(data)

def digits(metric):
    return(int(math.log10(find_AvgSamplingMetrics(metric=metric)))+1)

'''
sample=[]
counter=0
for i in range(len(temp)):
    counter+= temp[i][criteria]
    if counter >= threshold:
        counter=0
        sample.append(temp[i])
'''

#Sampler returns 2 list of samples time index
def volume_Anddollarsampler(data=temp):
    volume_str, dollar_str='volume', 'dollar'
    volume_sample, dollar_sample=[], []
    volume_counter, dollar_counter=0.0, 0.0
    for i in range(len(data)):
        sample_date=data[i]['date']
        volume_counter+= data[i][volume_str]
        dollar_counter+= float((data[i]['high'] + data[i]['low']) * data[i][volume_str] * 0.5)
        if volume_counter >= float(10**(digits(metric=volume_str)+1)):
            volume_counter=0 
            volume_sample.append(sample_date)
        if dollar_counter>= float(10**(digits(metric=dollar_str)+1)):
            dollar_counter=0
            dollar_sample.append(sample_date)
    return volume_sample, dollar_sample
    
def Indexer(date_list,data=temp):
    return list(filter(lambda d: d['date'] in date_list, data))

volumelist, dollarlist=volume_Anddollarsampler()

def df_Constructer(date_List):
    return pd.DataFrame.from_dict(Indexer(date_list=date_List))

volume_Sample=df_Constructer(volumelist)
dollar_Sample=df_Constructer(dollarlist)


