import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from stock_indicator import Stock_indicator

import warnings
warnings.filterwarnings('ignore')  # 모든 경고 메시지 무시

'''
매수 전략이랑 매도 전략이랑 짜보자
먼저 조건 검색으로 조건에 부합하는 종목을 불러오자(BuyList.txt)
조건검색으로 쓸 내용 만들어서 키움 HTS에 저장해두자
(이건 키움API로 불러와야 함.)

그리고 스퀴즈 모멘텀에 부합하는 애들을 불러오자.(Stock_indicator로 가져와)
그리고 나서 리스트에 저장하고
해당하는 애들은 매수한다.(밑에 있는거 갖다 써라)

매수 방식은 터틀트레이딩을 따라간다.
매수 수량 = 가용금액 * 0.02 / 2ATR (총 금액 대비 2% 손절 목표이고 금액이 모자라면 매수하지 않는다.)
(매수 수량을 결정하는 함수를 하나 짜)
'''
def buy_quantity(code, close, money = 1000000):
    atr = si.calculate_atr()
    quantity = round((money * 0.02)/(atr[-1]))

    if close[-1] * quantity < 1000000:
        return quantity
    else:
        return

'''


매도 전략은 두가지로 나누어서 하나라도 만족하면 처분하는걸로 하자.
1. 고니원칙
매수 이후에 매수가에 대해 최고점 대비 50%가 빠지면 즉 (최고점 - 매수가)/2 가격이 되면 매도

2. 스퀴즈 모멘텀의 매도 조건이 뜨면 매도한다.
일단 val값이 0보다 작아지거나 혹은 역시 매수시점 val값에 대해 최고점의 val값이 일정 구간 내려오면 매도
(약 50~60%정도 일때가 보통 그나마 낮드라.)

3. 손절조건은 터틀방식에 따라서 1 혹은 2 ATR만큼 빠지면 매도

4. 1.5:1 혹은 2:1의 손익비를 따져서 매도한다. 보통은 전 저점 기준(피봇포인트);

각 내용을 함수로 만들어서 정리한다.


'''




def read_ticker_file(filename):
    with open(filename, "r") as f:
        codes = [line.strip() for line in f.readlines()]
    return codes

import os
filename = os.path.abspath("code1.txt")

def status_sq():
    momentum_vals, squeeze_on, squeeze_off, no_squeeze = si.squeeze_momentum()
    histogram_status = 'Plus' if momentum_vals[-1] > 0 else 'Minus'

    if no_squeeze[-2] == True and squeeze_off[-2] == False and squeeze_off[-1] == True:
        if histogram_status == 'Plus':
            long_cond = '신호 떴다. 사러 가자' 
        else:
            long_cond = '어 대기해라. 아직 아니다.'
    else:
        long_cond = '응 신호 없다. 다른거 찾아봐라'
    return long_cond

codelist = []

from tqdm import tqdm

codes = read_ticker_file(filename)
    

for code in tqdm(codes):
    try:    
        stock_df = fdr.DataReader(code, '2022')
        si = Stock_indicator(stock_df)
        buycond = status_sq()
        atr = si.calculate_atr(20)
        close = si.close_price
        quantity = buy_quantity(code, close)
        
        sum_indi = si.calc_10indicator()
        # print(sum_indi)
        # print(type(sum_indi))
        if (sum_indi[-2] < 9 and sum_indi[-1] >= 9):
            codelist.append(code)
            print(code)
            print(sum_indi)
        # print(code)
        '''
        if buycond == '신호 떴다. 사러 가자':
            print(f"{code} 종목 {buycond} {quantity}개 사라. {code} 종목의 오늘 종가는 {close[-1]}원 이고 ATR은 {atr[-1]}원 이다.")
            codelist.append(code)
            #print(f"{code} 종목 신호 떴다. {quantity}개 사라")
        else:
            #print(f"{code} 종목의 오늘 종가는 {close[-1]}원 이고 ATR은 {atr[-1]}원 이다.")
            pass
            '''
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

print(codelist)