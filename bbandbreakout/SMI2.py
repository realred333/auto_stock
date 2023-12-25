
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from stock_indicator import Stock_indicator

def read_ticker_file(filename):
    with open(filename, "r") as f:
        codes = [line.strip() for line in f.readlines()]
    return codes

import os
filename = os.path.abspath("kosdaq.txt")

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
    
for code in codes:
    
    stock_df = fdr.DataReader(code, '2022')
    si = Stock_indicator(stock_df)
    buycond = status_sq()
    atr = si.calculate_atr(20)
    close = si.close_price
    
    if buycond == '신호 떴다. 사러 가자':
        codelist.append(code)
    else:
        pass

with open('buy_list.txt', 'w') as file:
    for code in codelist:
        file.write(code + '\n')
