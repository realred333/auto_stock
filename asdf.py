import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from stock_indicator import Stock_indicator


def read_ticker_file(filename):
    with open(filename, "r") as f:
        codes = [line.strip() for line in f.readlines()]
    return codes

import os
filename = os.path.abspath("code.txt")

def status_sq():
    momentum_vals, squeeze_on, squeeze_off, no_squeeze = si.squeeze_momentum()
    histogram_status = 'Plus' if momentum_vals[-1] > 0 else 'Minus'

    if squeeze_off[-2] == False and squeeze_off[-1] == True:
        if histogram_status == 'Plus':
            long_cond = '신호 떴다. 사러 가자' 
        else:
            long_cond = '어 대기해라. 아직 아니다.'
    else:
        long_cond = '응 신호 없다. 다른거 찾아봐라'
    return long_cond

codelist = []

codes = read_ticker_file(filename)
for code in codes:
    stock_df = fdr.DataReader(code, '2023-01-01', '2023-12-31')
    si = Stock_indicator(stock_df)
    buycond = status_sq()
    atr = si.calculate_atr(20)
    close = si.close_price
    print(f"{code} 종목의 오늘 종가는 {close[-1]}원 이고 ATR은 {atr[-1]}원 이다. 그리고 {buycond}")

    if buycond == '신호 떴다. 사러 가자':
        codelist.append(code)

print(codelist)



