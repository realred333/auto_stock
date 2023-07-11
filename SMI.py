import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import FinanceDataReader as fdr

def squeeze_momentum_indicator(data, bb_length=20, bb_multfactor=1.5, kc_length=20, kc_multfactor=1.5, use_truerange=True):

    # Calculate Bollinger Bands
    basis = data['Close'].rolling(window=bb_length).mean()
    dev = bb_multfactor * data['Close'].rolling(window=bb_length).std()
    upper_bb = basis + dev
    lower_bb = basis - dev

    # Calculate Keltner Channels
    ma = data['Close'].rolling(window=kc_length).mean()
    if use_truerange:
        tr1 = pd.DataFrame(data['High'] - data['Low'])
        tr2 = pd.DataFrame(abs(data['High'] - data['Close'].shift()))
        tr3 = pd.DataFrame(abs(data['Close'].shift() - data['Low']))
        frame = pd.concat([tr1, tr2, tr3], axis=1)
        range_val = np.max(frame, axis=1)
    else:
        range_val = data['High'] - data['Low']
    
    rangema = range_val.rolling(window=kc_length).mean()
    upper_kc = ma + rangema * kc_multfactor
    lower_kc = ma - rangema * kc_multfactor

    # Determine squeeze criteria
    sqz_on = (lower_bb > lower_kc) & (upper_bb < upper_kc)
    sqz_off = (lower_bb < lower_kc) & (upper_bb > upper_kc)
    no_sqz = (~sqz_on) & (~sqz_off)

    # Calculate Squeeze Momentum value
    highest_high = data['High'].rolling(window=kc_length).max()
    lowest_low = data['Low'].rolling(window=kc_length).min()
    sma_close = data['Close'].rolling(window=kc_length).mean()
    val = (data['Close'] - ((highest_high + lowest_low) / 2 + sma_close) / 2).rolling(window=kc_length).apply(np.sum)

    return val, sqz_on, sqz_off, no_sqz

# Read stock data
stock_code = input("종목 코드 입려해줄래?  ")
startdate = "2020-01-01"
enddate = "2023-07-11"
stock_data = fdr.DataReader(stock_code, startdate, enddate)

# Calculate Squeeze Momentum Indicator values
momentum_vals, squeeze_on, squeeze_off, no_squeeze = squeeze_momentum_indicator(stock_data)

def get_color(noSqz, sqzOn):
    if noSqz:
        return '대기상태'
    elif sqzOn:
        return 'on'
    else:
        return 'off'
    
# squeeze_status = get_color(no_squeeze, squeeze_on)
squeeze_status = get_color(no_squeeze.iloc[-1], squeeze_on.iloc[-1])


histogram_status = 'Plus' if momentum_vals.iloc[-1] >= 0 else 'Minus'


print(f"종목코드 {stock_code}에 대한 정보:")
print(f"스쿼이즈 상태: {squeeze_status}")
print(f"히스토그램 상태: {histogram_status}")
print(f"오늘 종가는 {stock_data['Close'].iloc[-1]} 입니다.")