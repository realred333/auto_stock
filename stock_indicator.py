'''
주가 데이터 계산을 여기다 모아두고 나중에 이거 불러다가 쓰자.
트루레인지, ATR, 볼린저밴드, 켈트너채널, VWMA

추가해야할 것!!!
몇몇 전략 지표들을 추가하자.
스퀴즈 모멘텀, 슈퍼트렌드, 파라볼릭SAR, 
'''

import pandas as pd
import numpy as np


class Stock_indicator:
    def __init__(self, df):
        self.df = pd.DataFrame(df)
        self.open_price = self.df['Open']
        self.high_price = self.df['High']
        self.low_price = self.df['Low']
        self.close_price = self.df['Close']
        self.volume = self.df['Volume']
        self.price = (self.close_price + self.high_price + self.low_price) / 3

    def calculate_true_range(self):
        self.tr1 = self.high_price - self.low_price
        self.tr2 = abs(self.high_price - self.close_price.shift())
        self.tr3 = abs(self.low_price - self.close_price.shift())
        self.true_range = pd.concat([self.tr1, self.tr2, self.tr3], axis=1).max(axis=1)
        return self.true_range

    def calculate_atr(self, period=16):
        self.TrueRange = self.calculate_true_range()
        self.ATR = self.TrueRange.rolling(window=period).mean()
        return self.ATR

    def calc_vwma(self, period):        
        self.VWMA = (self.price * self.volume).rolling(window=period).sum() / self.volume.rolling(window=period).sum()
        return self.VWMA
    
    def calc_BBand(self, periodBB=14, stddev=2):
        self.calc_vwma(periodBB)
        self.UpperBB = self.VWMA + (self.price.rolling(window=periodBB).std() * stddev)
        self.LowerBB = self.VWMA - (self.price.rolling(window=periodBB).std() * stddev)
        
        return self.UpperBB, self.LowerBB
    
    def calc_Keltner(self, periodKC=16, multKC=1.5):
        
        self.calc_vwma(periodKC)
        self.calculate_atr(periodKC)
        self.UpperKC = self.VWMA + (self.ATR * multKC)
        self.LowerKC = self.VWMA - (self.ATR * multKC)
        return self.UpperKC, self.LowerKC
    

 
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
        self.sma_close = self.close_price.rolling(window=periodKC).mean()
        self.val = (self.close_price - ((self.highest_high + self.lowest_low) / 2 + self.sma_close) / 2).rolling(window=periodKC).apply(np.sum)

        return self.val, self.sqz_on, self.sqz_off, self.no_sqz



 
    