'''
주가 데이터 계산을 여기다 모아두고 나중에 이거 불러다가 쓰자.
트루레인지, ATR, 볼린저밴드, 켈트너채널, VWMA

추가해야할 것!!!
몇몇 전략 지표들을 추가하자.
스퀴즈 모멘텀, 슈퍼트렌드, 파라볼릭SAR, 
'''

import pandas as pd
import numpy as np

def Linreg(source, length:int):
    size = len(source)
    linear = np.zeros(size)

    for i in range(length, size):

        sumX = 0.0
        sumY = 0.0
        sumXSqr = 0.0
        sumXY = 0.0

        for z in range(length):
            val = source[i-z]
            per = z + 1.0
            sumX += per
            sumY += val
            sumXSqr += per * per
            sumXY += val * per

        slope = (length * sumXY - sumX * sumY) / (length * sumXSqr - sumX * sumX)
        average = sumY / length
        intercept = average - slope * sumX / length + slope

        linear[i] = intercept
    return linear


class Stock_indicator:
    def __init__(self, df):
        self.df = pd.DataFrame(df)
        self.open_price = self.df['Open']
        self.high_price = self.df['High']
        self.low_price = self.df['Low']
        self.close_price = self.df['Close']
        self.volume = self.df['Volume']
        self.price = (self.close_price + self.high_price + self.low_price) / 3

    #트루레인지 만들기
    def calculate_true_range(self):
        self.tr1 = self.high_price - self.low_price
        self.tr2 = abs(self.high_price - self.close_price.shift())
        self.tr3 = abs(self.low_price - self.close_price.shift())
        self.true_range = pd.concat([self.tr1, self.tr2, self.tr3], axis=1).max(axis=1)
        return self.true_range

    #ATR만들기
    def calculate_atr(self, period=16):
        self.TrueRange = self.calculate_true_range()
        self.ATR = self.TrueRange.rolling(window=period).mean()
        return self.ATR

    #VWMA만들기
    def calc_vwma(self, period):        
        self.VWMA = (self.price * self.volume).rolling(window=period).sum() / self.volume.rolling(window=period).sum()
        return self.VWMA
    
    #볼린저밴드 만들기
    def calc_BBand(self, periodBB=14, stddev=2):
        self.calc_vwma(periodBB)
        self.UpperBB = self.VWMA + (self.price.rolling(window=periodBB).std() * stddev)
        self.LowerBB = self.VWMA - (self.price.rolling(window=periodBB).std() * stddev)
        
        return self.UpperBB, self.LowerBB
    
    #켈트너 채널 만들기
    def calc_Keltner(self, periodKC=16, multKC=1.5):
        
        self.calc_vwma(periodKC)
        self.calculate_atr(periodKC)
        self.UpperKC = self.VWMA + (self.ATR * multKC)
        self.LowerKC = self.VWMA - (self.ATR * multKC)
        return self.UpperKC, self.LowerKC
    

    
    #스퀴즈 모멘텀 만들기
    def squeeze_momentum(self, periodBB=14, periodKC=16, stddevBB=2, multKC = 1.5):
        self.calc_BBand(periodBB, stddevBB)
        self.calc_Keltner(periodKC, multKC)
        # Determine squeeze criteria
        self.sqz_on = (self.LowerBB > self.LowerKC) & (self.UpperBB < self.UpperKC)
        self.sqz_off = (self.LowerBB < self.LowerKC) & (self.UpperBB > self.UpperKC)
        self.no_sqz = (~self.sqz_on) & (~self.sqz_off)
       
        # Calculate Squeeze Momentum value
        self.highest_high = self.high_price.rolling(window=periodKC).max()
        self.lowest_low = self.low_price.rolling(window=periodKC).min()
        # self.vwma_close = self.close_price.rolling(window=periodKC).mean()
        vwma = self.calc_vwma(periodKC)

        self.val = Linreg(self.close_price - ((self.highest_high + self.lowest_low)/ 2 + vwma) / 2, periodKC)

        return self.val, self.sqz_on, self.sqz_off, self.no_sqz


    #스토캐스틱 slow
    def calculate_stochastic_slow(self, k_period=20, d_period=10, k_slow_period=10):
        self.highest_high = self.high_price.rolling(window=k_period).max()
        self.lowest_low = self.low_price.rolling(window=k_period).min()
        self.K_fast = 100 * ((self.close_price - self.lowest_low) / (self.highest_high - self.lowest_low))
        self.D_slow = self.K_fast.rolling(window=d_period).mean()
        self.K_slow = self.D_slow.rolling(window=k_slow_period).mean()
        return self.D_slow, self.K_slow
    

