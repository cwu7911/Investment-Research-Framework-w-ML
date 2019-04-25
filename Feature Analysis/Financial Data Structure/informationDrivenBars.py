# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:53:05 2019

@author: cwu7911
data from AlphaVantage
"""

import numpy as np
import pandas as pd
from scipy.stats import jarque_bera

from alpha_vantage.timeseries import TimeSeries
Alpha_vantage_key= 'YourKey'

ts = TimeSeries(key=Alpha_vantage_key,
                output_format='pandas')
data, meta_d = ts.get_daily(symbol=['AAPL'],  
                            outputsize='full')
'''
Tick Imbalance Bar, sampling based on information flow, or run larger than expectation
sample=np.sign(pd.DataFrame((data['4. close']).diff().fillna(0)))

only record the dates when tick imbalance > expectations
sample['tick imbalance']=sample.cumsum()
sample['expected tick imbalance']=sample['tick imbalance'].ewm(min_periods=10,ignore_na=False,span=10,adjust=True).mean()
sample['expected tick']=sample.iloc[:,0].ewm(min_periods=10,ignore_na=False,span=10,adjust=True).mean()
sample['expectations']=(sample['expected tick imbalance'] * sample['expected tick']).shift(1)
ilist=sample[sample['tick imbalance'] > sample['expectations']].index.tolist()
returns=[data.loc[ilist[i+1]]['4. close']/data.loc[ilist[i]]['4. close']-1 for i in range(len(ilist)-1)]

print('Serial correlation for sample returns: ', serr_corr(pd.Series(returns).sort_index(ascending=False)))
'''

def serr_corr(series, lag=1):
    series=series.dropna()
    n=len(series)
    y1=series[lag:]
    y2=series[:n-lag]
    corr=np.corrcoef(y1, y2)[0,1]
    return corr

#more generalized function
def tickConverter(df):
    return np.sign(df.diff().fillna(0))

def imbalanceBarIndex(df):
    df['tick imbalance']=df.cumsum()
    df['expected tick imbalance']=df['tick imbalance'].ewm(min_periods=10,ignore_na=False,span=10,adjust=True).mean()
    df['expected tick']=df.iloc[:,0].ewm(min_periods=10,ignore_na=False,span=10,adjust=True).mean()
    df['expectations']=(df['expected tick imbalance'] * abs(df['expected tick'])).shift(1)
    ilist=df[abs(df['tick imbalance']) >= df['expectations']].index.tolist()
    return ilist

def JB_Test_score(series):
    return jarque_bera(series)[1]

def ImbalanceBars(df):
    frame=tickConverter(df)
    ilist=imbalanceBarIndex(frame)
    returns=[data.loc[ilist[i+1]]['4. close']/data.loc[ilist[i]]['4. close']-1 for i in range(len(ilist)-1)]
    print('Sample returns serial correlation: ', serr_corr(pd.Series(returns).sort_index(ascending=False)))
    print('Sample returns JB p-stats: ', JB_Test_score(pd.Series(returns).sort_index(ascending=False)))
    print('Sample returns size: ', len(returns))
    return data.loc[ilist]

tickSample=pd.DataFrame(data['4. close'])
dollarSample=pd.DataFrame(data['5. volume']*(data['2. high']+data['3. low'])*0.5)
volumeSample=pd.DataFrame(data['5. volume'])








