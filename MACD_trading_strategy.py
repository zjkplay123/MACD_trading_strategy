# -*- coding: utf-8 -*-
"""

@author: Jinkai Zhang

"""

import pandas as pd


#MACD strategy only needs the closing price data for individual stock

#First step: define Function of getting moving average data (EMA)
#the input df is dataframe with one column of closing price and N is the number of lags
def Fun_EMA(df, N):
    for i in range(len(df)):
        if i == 0:
            df.ix[i,'ema'] = df.ix[i,'close']
        if i > 0:
            df.ix[i,'ema'] = (2 * df.ix[i,'close'] + (N-1) * df.ix[i-1,'ema']) / (N+1)
    ema = list(df['ema'])
    return ema

#Second step: define Function of getting DIF and DEA in MACD trading strategy
def Fun_MACD(df, short = 12, long = 26, M = 9):
    Short_ema = Fun_EMA(df, short)
    Long_ema = Fun_EMA(df, long)
    df['dif'] = pd.Series(Short_ema) - pd.Series(Long_ema)
    for i in range(len(df)):
        if i == 0:
            df.ix[i,'dea'] = df.ix[i,'dif']
        if i > 0:
            df.ix[i,'dea'] = (2 * df.ix[i,'dif'] + (M-1) * df.ix[i-1,'dea']) / (M+1)
    df['macd'] = 2 * (df['dif'] - df['dea'])
    return df


#Key function of MACD trading strategy, data managed in dictionary
def strategy(data):
    prev_day = sorted(list(data.keys()))[-1]
    candles = data[prev_day]
    assets = list(candles.keys())
    portfolio = {}
    for asset in assets:
#Define a empty list series in order to get the historical closing data of each asset        
        series = []
        for i in range(29):
#append the historical closing data to series            
            try:                
                series.append(data[list(data.keys())[i]][asset]['close'])
            except:
                pass
#convert the historical series to dataframe so as to append MACD indices            
        try:
            df = pd.DataFrame({'close':series})
#append MACD indices including EMA, DIF, DEA            
            df = Fun_MACD(df, 12, 26, 9)
#extract the key indices DIF and DEA in MACD strategy            
            dif = list(df['dif'])
            dea = list(df['dea'])
#MACD strategy: BUY if DIF upcross DEA given positive value of DIF and DEA and SELL if DIF downcross DEA given negative value of DIF and DEA            
            if dif[-1] >= 0 and dea[-1] >= 0 and (dif[-2] <= dea[-2]) and (dif[-1] >= dea[-1]):
                    portfolio[asset] = 1
            elif dif[-1] < 0 and dea[-1] < 0 and (dif[-2] >= dea[-2]) and (dif[-1] <= dea[-1]):
                    portfolio[asset] = -1
            else:
                portfolio[asset] = 0   
        except:
            portfolio[asset] = 0
    return portfolio   

        
        
        
        














