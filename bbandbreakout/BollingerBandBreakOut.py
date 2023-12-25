import pandas_ta as ta
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import math


def bbbo(code):
        
    df = fdr.DataReader(code, '2022')
    close = df['Close']
    high = df['High']
    low = df['Low']
    open = df['Open']
    volume = df['Volume']

    def nz(value1, value2 = 0):
        return value1 if value1 != 0 else value2


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

    # Entry Option by Volume and Colored bar
    vollength = 20
    avrg = ta.sma(volume, vollength)

    thresholdExtraHigh = 4
    thresholdHigh = 2.5
    thresholdMedium = 1
    thresholdNormal = 0.5

    vol1 = volume[-1] > avrg[-1] * thresholdExtraHigh
    vol2 = volume[-1] >= avrg[-1] * thresholdHigh and volume[-1] <= avrg[-1] * thresholdExtraHigh
    vol3 = volume[-1] >= avrg[-1] * thresholdMedium and volume[-1] <= avrg[-1] * thresholdHigh
    vol4 = volume[-1] >= avrg[-1] * thresholdNormal and volume[-1] <= avrg[-1] * thresholdMedium
    vol5 = volume[-1] < avrg[-1] * thresholdNormal

    l_act_low_size             = True
    l_act_normal_size          = True
    l_act_medium_size          = True
    l_act_high_size            = True
    l_act_extrahigh_size       = True

    if l_act_low_size & vol5:
        vol_long_entry = True
    elif l_act_normal_size & vol4:
        vol_long_entry = True
    elif l_act_medium_size & vol3:
        vol_long_entry = True
    elif l_act_high_size & vol2:
        vol_long_entry = True
    elif l_act_extrahigh_size & vol1:
        vol_long_entry = True
    else:
        vol_long_entry = False
        



    # Define the length of the Bollinger Bands
    active_long = True
    lbblength = 23
    lbbdev = 1.7
    lbbminwidth = 2
    lbbdiff = False
    lbbdiffperc = 0

    #Calculate and plot the Bollinger Bands
    lbb = pd.DataFrame()

    lbb['lbbmiddle'] = ta.sma(close, lbblength)
    lbb['lbbdev'] = lbbdev * ta.stdev(close, lbblength)
    #lbb['lbbdev'] = max(lbb['lbbdev'], (lbb['lbbmiddle'] * lbbminwidth) / 100)
    lbbupper = lbb['lbbmiddle'] + lbb['lbbdev']
    lbblower = lbb['lbbmiddle'] - lbb['lbbdev']
    lbb['lbbcrossover'] = ta.cross(close, lbbupper)
    lbbcrossover = lbb['lbbcrossover']
    lbbdiffcond = ((lbbupper / lbblower) * 100) - 100 >= lbbdiffperc if lbbdiff else True






    #############Define the settings for the Volatility Filter################
    volatilityFilterInput = True
    volatilityFilterStDevLength = 3
    volatilityStDevMaLength = 36

    ###############Calculate and view Volatility Filter#######################
    stdDevClose = ta.stdev(close, volatilityFilterStDevLength)
    volatilityCondition = stdDevClose > ta.sma(stdDevClose, volatilityStDevMaLength) if volatilityFilterInput == True else True

    #####################Historical Volatility Filter#########################
    enable_long_vol = True
    HVlength = 6
    HVthreshold = 1

    HV = np.log(close / close.shift(1))
    HV = HV.rolling(HVlength).std()
    HV = HV * np.sqrt(365) * 100
    HV_long_condt = (HV - HV.shift(1)) > HVthreshold if enable_long_vol == True else True

    ############################ADX Filter####################################
    enable_long_adx = True
    long_adxlen = 17


    TrueRange = ta.true_range(high, low, close)
    DM = ta.dm(high, low, long_adxlen)
    DM.columns = ['DMP', 'DMN']
    DM['TrueRange'] = TrueRange
    DM['DIplus'] = (DM['DMP'] / DM['TrueRange']) * 100
    DM['DIminus'] = (DM['DMN'] / DM['TrueRange']) * 100

    # long_DX = np.abs(long_DIPlus - long_DIMinus) / (long_DIPlus + long_DIMinus) * 100
    # long_ADX = ta.sma(long_DX, long_adxlen)
    adx_long_condt = (DM['DIplus'] > DM['DIplus'].shift(1)) & (DM['DIplus'] > DM['DIminus']) if enable_long_adx == True else True
    print(DM)
    all_true = vol_long_entry & lbbdiffcond & volatilityCondition & HV_long_condt & adx_long_condt & lbbcrossover == 1
    if all_true[-1]:
        print("find it!!!")
        return code
    else:
        print(vol_long_entry)
        print(lbbdiffcond)
        print(volatilityCondition)
        print(HV_long_condt)
        print(adx_long_condt)
        print(lbbcrossover)
        pass

    


def read_ticker_file(filename):
    with open(filename, "r") as f:
        codes = [line.strip() for line in f.readlines()]
    return codes

import os
filename = os.path.abspath("buy_list.txt")
    
#codes = ['003380', '310210', '007390', '151860', '228760', '335890', '230360', '138580', '089980', '136480', '214680', '030960', '051500', '131400', '024060', '044340', '104540', '211050', '340930', '418250', '054620', '036710', '200470', '216050', '066700', '337930', '203400', '013990', '003100', '105550', '100700', '290720', '288620', '321370', '082850', '407400', '050110', '241770', '234300', '065130', '001540', '289080', '187870', '011560', '008830', '376180', '378800', '064800', '123410', '042110', '239340', '158430', '254120', '128540', '131030', '301300', '250000', '170920', '017650', '033130', '348030', '041460', '290740', '039830', '047770', '097780', '123570', '291650', '214270', '038010', '219420', '115180', '059270', '028080', '237820', '273060', '139670', '212560', '073110', '131100', '153490', '054540', '036690', '115610', '005670', '192410', '208710', '222160', '101400', '026040', '095910', '048470', '035200', '215480', '317530', '179530', '008290', '020400', '079950', '054220', '069330', '177350', '043360', '091440', '321820']
codes = read_ticker_file(filename)
codelist = []
from tqdm import tqdm
if __name__ == "__main__":
    for code in tqdm(codes):
        print(code)
        code1 = bbbo(code)
        if code1 != None:
            codelist.append(code1)
print(codelist)

