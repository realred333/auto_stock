import pandas as pd
import numpy as np
import FinanceDataReader as fdr

#주가 불러오기
code = '109610'
df = fdr.DataReader(code, '2022')
df = pd.DataFrame(df)
open = df['Open']
close = df['Close']
high = df['High']
low = df['Low']

#초기 조건
prd = 20    #Pivot Period
ppsrc = 'High/Low'  #Source
maxnumpp = 20   #Maximum Number of Pivot
ChannelW = 10   #Maximum Channel Width %
maxnumsr = 5    # Maximum Number of S/R
min_strength = 2    # Minum Strength


# pivothigh 함수 구현
# def pivothigh(high, period):
#     pivot_highs = []
#     for i in range(len(high) - period + 1):
#         window = high[i:i + period]
#         if high[i] == max(window):
#             pivot_highs.append(high[i])
#     return pivot_highs

# # pivotlow 함수 구현
# def pivotlow(low, period):
#     pivot_lows = []
#     for i in range(len(low) - period + 1):
#         window = low[i:i + period]
#         if low[i] == min(window):
#             pivot_lows.append(low[i])
#     return pivot_lows

def pivothigh(high, period):
    pivot_highs = []
    for i in range(period - 1, len(high)):
        window = high[i - period + 1:i + 1]
        if high[i] == max(window):
            pivot_highs.append(high[i])
        else:
            pivot_highs.append(np.nan)
    return pivot_highs

def pivotlow(low, period):
    pivot_lows = []
    for i in range(period - 1, len(low)):
        window = low[i - period + 1:i + 1]
        if low[i] == min(window):
            pivot_lows.append(low[i])
        else:
            pivot_lows.append(np.nan)
    return pivot_lows



src1 = high
src2 = low
ph = pivothigh(src1, prd)
pl = pivotlow(src2, prd)

prdhighest = high.tail(300).max()
prdlowest = low.tail(300).min()
cwidth = (prdhighest - prdlowest) * ChannelW / 100

pivotvals = []

def add_to_pivotvals(value):
    pivotvals.insert(0, value)  # 값을 pivotvals 리스트의 맨 앞에 추가
    if len(pivotvals) > maxnumpp:  # 배열 크기가 maxnumpp보다 크다면
        pivotvals.pop()  # 배열 끝에서 값을 제거

# ph 또는 pl이 true일 때 값을 추가
# if ph or pl:
#     if ph:
#         add_to_pivotvals(ph)
#     else:
#         add_to_pivotvals(pl)

# ph 또는 pl이 true일 때 값을 추가
# if len(ph) > 0:
#     add_to_pivotvals(ph[-1])
# if len(pl) > 0:
#     add_to_pivotvals(pl[-1])

# ph 또는 pl이 true일 때 값을 추가
if len(ph) > 0:
    for val in ph:
        add_to_pivotvals(val)
if len(pl) > 0:
    for val in pl:
        add_to_pivotvals(val)



def get_sr_vals(ind):
    lo = pivotvals[ind]
    hi = lo
    numpp = 0

    for y in range(len(pivotvals)):
        cpp = pivotvals[y]
        wdth = hi - cpp if cpp <= lo else cpp - lo
        if wdth <= cwidth:
            if cpp <= hi:
                lo = min(lo, cpp)
            else:
                hi = max(hi, cpp)

            numpp += 1

    return hi, lo, numpp

sr_up_level = []
sr_dn_level = []
sr_strength = []

def find_loc(strength, sr_strength):
    ret = len(sr_strength)
    for i in range(ret - 1, -1, -1):
        if strength <= sr_strength[i]:
            ret = i
        else:
            break
    return ret

def check_sr(hi, lo, strength, sr_up_level, sr_dn_level, sr_strength):
    ret = False
    i = 0

    while i < len(sr_up_level):
        if (len(sr_up_level) > 0 and i < len(sr_up_level) - 1) or i is None:
            if (
                (sr_up_level[i] >= lo and sr_up_level[i] <= hi) or
                (sr_dn_level[i] >= lo and sr_dn_level[i] <= hi)
            ):
                if strength >= sr_strength[i]:
                    del sr_strength[i]
                    del sr_up_level[i]
                    del sr_dn_level[i]
                    ret = True
                else:
                    i += 1
            else:
                i += 1
    return ret

# 코드의 나머지 부분은 이전 코드와 동일합니다

# Check if ph or pl is True
if len(ph) > 0 or len(pl) > 0:
    # Remove old S/R levels due to new calculation
    sr_up_level.clear()
    sr_dn_level.clear()
    sr_strength.clear()
    
    # Find S/R zones
    for x in range(len(pivotvals)-1):
        hi, lo, strength = get_sr_vals(x)
        if check_sr(hi, lo, strength, sr_up_level, sr_dn_level, sr_strength):
            loc = find_loc(strength, sr_strength)
            if loc < maxnumsr and strength >= min_strength:
                sr_strength.insert(loc, strength)
                sr_up_level.insert(loc, hi)
                sr_dn_level.insert(loc, lo)
                if len(sr_strength) > maxnumsr:
                    sr_strength.pop()
                    sr_up_level.pop()
                    sr_dn_level.pop()
    
    # Print support and resistance levels
    for x in range(len(sr_up_level)):
        print(f"Support: {sr_dn_level[x]}, Resistance: {sr_up_level[x]}")
