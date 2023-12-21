import pandas_ta as ta
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import math

df = fdr.DataReader('035600', '2022')
close = df['Close']
high = df['High']
low = df['Low']

def nz(value1, value2 = 0):
    return value1 if value1 != 0 else value2

##일단 하나하나씩 만들어서 합치자.
#데스크탑이랑 이거랑 뭐랑 뭐랑 다 섞든 뭐든 일단 한개씩 차례대로 만들어보자
#데스크탑에는 볼린저밴드 만드는거 했음.



################Autonomous Recursive Moving Average#######################
#이거 빼고 가자..안돼....ㅠㅠ
# enable_long_arma = True
# ara_length = 13
# gamma = 2

# ma = 0.0
# mad = 0.0
# d_temp = 0.0
# i = 0
# #src_ = close
# #ma = src_ if mad[1] == 0 else mad[1]
# while i < ara_length:
#     if len(close) > ara_length:
#         d_temp += abs(close[-1*(ara_length + i)] - close[-1*(i+1)])
#         i += 1

    
# d = d_temp / ara_length * gamma
# print(d)


#############Define the settings for the Volatility Filter################
volatilityFilterInput = True
volatilityFilterStDevLength = 15
volatilityStDevMaLength = 15

###############Calculate and view Volatility Filter#######################
stdDevClose = ta.stdev(close, volatilityFilterStDevLength)
volatilityCondition = stdDevClose > ta.sma(stdDevClose, volatilityStDevMaLength) if volatilityFilterInput == True else True

#####################Historical Volatility Filter#########################
enable_long_vol = True
HVlength = 10
HVthreshold = 1

HV = np.log(close / close.shift(1))
HV = HV.rolling(HVlength).std()
HV = HV * np.sqrt(365) * 100
HV_long_condt = (HV - HV.shift(1)) > HVthreshold if enable_long_vol == True else True

############################ADX Filter####################################
enable_long_adx = True
long_adxlen = 14

TrueRange = ta.true_range(high, low, close)
DM = ta.dm(high, low, long_adxlen)
long_DM = DM / TrueRange * 100
# long_DX = np.abs(long_DIPlus - long_DIMinus) / (long_DIPlus + long_DIMinus) * 100
# long_ADX = ta.sma(long_DX, long_adxlen)
print(long_DM)
# adx_long_condt = long_DIPlus > long_DIPlus.shift(1) and long_DIPlus > long_DIMinus if enable_long_adx else True
# print(adx_long_condt)



'''



// Autonomous Recursive Moving Average
enable_long_arma = input(true, "Enable Long     ", inline="ara1", group="Autonomous Recursive Moving Average")
enable_short_arma = input(true, "Enable Short ", inline="ara1", group="Autonomous Recursive Moving Average")

ara_length = input.int(13, title='Length ', group='Autonomous Recursive Moving Average', inline='ara2')
gamma = input.float(3.0, title='Gamma ', group='Autonomous Recursive Moving Average', inline='ara2')

ma = 0.
mad = 0.

src_ = close
ma := nz(mad[1], src_) 
d = ta.cum(math.abs(src_[ara_length] - ma)) / bar_index * gamma
mad := ta.sma(ta.sma(src_ > nz(mad[1], src_) + d ? src_ + d : src_ < nz(mad[1], src_) - d ? src_ - d : nz(mad[1], src_), ara_length), ara_length)

arma_long_condt = enable_long_arma ? close > mad : true
arma_short_condt = enable_short_arma ? close < mad : true

plot(mad, title='ARA', 
   
     color=color.new(color.orange, 20), style=plot.style_line, linewidth=2)


'''