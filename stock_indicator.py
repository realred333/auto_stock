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
        # self.sqz_on = (self.LowerBB > self.LowerKC) and (self.UpperBB < self.UpperKC)
        # self.sqz_off = (self.LowerBB < self.LowerKC) and (self.UpperBB > self.UpperKC)
        # self.no_sqz = (self.sqz_on == False) and (self.sqz_off == False)

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
    

    #10 indicator
    # RSI, MACD, 200sma, 100sma, 75ema, 55ema, 50sma, 20ema, 13/48cross, pivot_level
    
    # RSI 계산 함수
    def calculate_rsi(self, period=14):   # RSI를 계산하는 함수를 정의하며, 기본적으로 14일 기간을 사용합니다.
        delta = self.close_price.diff(1)   # 가격 데이터의 차이를 계산합니다.
        gain = delta.where(delta > 0, 0)   # 양의 차이(상승)를 추출합니다.
        loss = -delta.where(delta < 0, 0)  # 음의 차이(하락)를 추출합니다.

        avg_gain = gain.rolling(window=period, min_periods=1).mean()  # 이동평균을 계산하여 양의 차이의 평균을 구합니다.
        avg_loss = loss.rolling(window=period, min_periods=1).mean()  # 이동평균을 계산하여 음의 차이의 평균을 구합니다.

        relative_strength = avg_gain / avg_loss  # 상대적인 강도를 계산합니다.
        self.rsi = 100 - (100 / (1 + relative_strength))  # RSI 값을 계산합니다.
        
        return self.rsi  # RSI 값을 반환합니다.
    

    # MACD 계산 함수
    def calculate_macd(self, short_window=12, long_window=26, signal_window=9):
        # 단기 이동평균
        short_ema = self.close_price.ewm(span=short_window, adjust=False).mean()
        
        # 장기 이동평균
        long_ema = self.close_price.ewm(span=long_window, adjust=False).mean()
        
        # MACD (단기 이동평균 - 장기 이동평균)
        self.macd = short_ema - long_ema
        
        # MACD의 시그널 라인 (MACD의 이동평균)
        self.signal_line = self.macd.ewm(span=signal_window, adjust=False).mean()
        
        # MACD 히스토그램 (MACD - 시그널 라인)
        self.macd_histogram = self.macd - self.signal_line
        
        return self.macd, self.signal_line, self.macd_histogram

    # 각 항목 계산하고 true 갯수를 출력해보자.
    #10 indicator
    # RSI, MACD, 200sma, 100sma, 75ema, 55ema, 50sma, 20ema, 13/48cross, pivot_level
    

    # 이동평균 계산 함수
    def calculate_averages(self, periods):
        self.averages = pd.DataFrame()
        for period in periods:
            if 'sma' in period:
                window = int(period.replace('sma', ''))
                self.averages[period] = self.close_price.rolling(window=window).mean()
            elif 'ema' in period:
                span = int(period.replace('ema', ''))
                self.averages[period] = self.close_price.ewm(span=span, adjust=False).mean()
        
        return self.averages
    
    '''
    def calc_10indicator(self):
        self.sum_indi = 0
        self.calculate_macd()
        self.calculate_rsi()
        periods = ['200sma', '100sma', '75ema', '55ema', '50sma', '20ema']
        self.calculate_averages(periods)
        print(self.averages)
        for average in self.averages:
           if self.close_price > average:
               self.sum_indi += 1
        if self.rsi > 55 and self.rsi:
            self.sum_indi += 1
        if self.macd > 0 and self.macd:
            self.sum_indi += 1
        
        average13 = self.close_price.ewm(span = 13, adjust=False).mean()
        average48 = self.close_price.ewm(span = 48, adjust=False).mean()

        if average13 > average48 and average13:
            self.sum_indi += 1

        return self.sum_indi
    '''

    # def calc_10indicator(self):
    #     self.sum_indi = pd.DataFrame()

    #     # 이동평균 및 MACD, RSI 계산
    #     self.calculate_macd()
    #     self.calculate_rsi()
    #     periods = ['200sma', '100sma', '75ema', '55ema', '50sma', '20ema']
    #     self.calculate_averages(periods)

    #     # 각 이동평균에 대한 조건 검사
    #     for period in periods:
    #         if (self.close_price > self.averages[period]).all():
    #             self.sum_indi += 1

    #     # RSI와 MACD 조건 검사
    #     if (self.rsi is not None and self.rsi > 55).all():
    #         self.sum_indi += 1
    #     if (self.macd is not None and self.macd > 0).all():
    #         self.sum_indi += 1

    #     # 13일 이동평균과 48일 이동평균 조건 검사
    #     average13 = self.close_price.ewm(span=13, adjust=False).mean()
    #     average48 = self.close_price.ewm(span=48, adjust=False).mean()
    #     if average13 is not None and average48 is not None and (average13 > average48).all():
    #         self.sum_indi += 1

    #     return self.sum_indi

    def calc_10indicator(self):
        # 이동평균 및 MACD, RSI 계산
        self.calculate_macd()
        self.calculate_rsi()
        periods = ['200sma', '100sma', '75ema', '55ema', '50sma', '20ema']
        self.calculate_averages(periods)

        # 각 조건에 대한 조건 검사
        self.sum_indi = pd.DataFrame()

        for period in periods:
            self.sum_indi[period] = (self.close_price > self.averages[period]).astype(int)

        # RSI와 MACD 조건 검사
        self.sum_indi['rsi_condition'] = ((self.rsi > 55) & (self.rsi.notna())).astype(int)
        self.sum_indi['macd_condition'] = ((self.macd > 0) & (self.macd.notna())).astype(int)

        # 13일 이동평균과 48일 이동평균 조건 검사
        average13 = self.close_price.ewm(span=13, adjust=False).mean()
        average48 = self.close_price.ewm(span=48, adjust=False).mean()
        self.sum_indi['average13_condition'] = ((average13 > average48) & (average13.notna()) & (average48.notna())).astype(int)

        #피봇
        #주봉데이터 만들기
        self.weekly_data = self.df.resample('W').agg({'High': 'max', 'Low': 'min', 'Close': 'last'})
        self.pivot_point = (self.weekly_data['High'] + self.weekly_data['Low'] + self.weekly_data['Close']) / 3            
        self.sum_indi['pivot_condition'] = self.close_price[-1] > self.pivot_point[-2]

        # 각 조건에 따라 총합 계산
        self.sum_indi['total_sum'] = self.sum_indi.sum(axis=1)
        return self.sum_indi['total_sum']
    ##야 피봇 빼먹었다. 피봇 만드는거도 해봐라
    # 주봉 데이터 계산
    