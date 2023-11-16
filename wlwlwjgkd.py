import pandas as pd
import numpy as np
import FinanceDataReader as fdr

#주가 불러오기
code = '109610'
df = fdr.DataReader(code, '2020')
df = pd.DataFrame(df)
open = df['Open']
close = df['Close']
high = df['High']
low = df['Low']

#초기 조건
prd = 12    #Pivot Period
maxnumpp = 20   #Maximum Number of Pivot
ChannelW = 10   #Maximum Channel Width %
maxnumsr = 5    # Maximum Number of S/R
min_strength = 2    # Minum Strength

def round_to_mintick(value):
    if value < 1000:
        return round(value, 2)
    elif value < 5000:
        return round(value / 5) * 5
    elif value < 10000:
        return round(value / 10) * 10
    elif value < 50000:
        return round(value / 50) * 50
    elif value < 100000:
        return round(value / 100) * 100
    else:
        return round(value / 500) * 500

def pivothigh(source, period):
    pivot_highs = []
    for i in range(period, len(source)-period):
        if source[i] > max(source[i-period:i]) and source[i] >= max(source[i+1:i+period+1]):
            pivot_highs.append(source[i])
    return pivot_highs

def pivotlow(source, period):
    pivot_lows = []
    for i in range(period, len(source)-period):
        if source[i] < min(source[i-period:i]) and source[i] <= min(source[i+1:i+period+1]):
            pivot_lows.append(source[i])
    return pivot_lows

def pivothl(source1, source2, period):
    pivot_hl = []
    for i in range(period, len(source1)-period):
        if source1[i] > max(source1[i-period:i]) and source1[i] >= max(source1[i+1:i+period+1]):
            pivot_hl.append(source1[i])
        elif source2[i] < min(source2[i-period:i]) and source2[i] <= min(source2[i+1:i+period+1]):
            pivot_hl.append(source2[i])
    return pivot_hl


src1 = high
src2 = low
ph = pivothigh(src1, prd)
pl = pivotlow(src2, prd)
phl = pivothl(src1, src2, prd)

prdhighest = high.tail(300).max()
prdlowest = low.tail(300).min()
cwidth = (prdhighest - prdlowest) * ChannelW / 100

pivotvals = []

def add_to_pivotvals(value):
    pivotvals.insert(0, value)  # 값을 pivotvals 리스트의 맨 앞에 추가
    if len(pivotvals) > maxnumpp:  # 배열 크기가 maxnumpp보다 크다면
        pivotvals.pop()  # 배열 끝에서 값을 제거
    
    


# ph 또는 pl이 true일 때 값을 추가
# if phbool or plbool:
#     if phbool:
#         for val in ph:
#             add_to_pivotvals(val)
            
#     else:
#         for val in pl:
#             add_to_pivotvals(val)
#     phbool = False
#     plbool = False


# if len(ph) > 0 or len(pl) > 0:
#     for val in ph:
#         add_to_pivotvals(val)
#     for val in pl:
#         add_to_pivotvals(val)

if len(phl) > 0:
    for val in phl:
        add_to_pivotvals(val)

# print(pivotvals)

def get_sr_vals(ind):
    lo = pivotvals[ind]
    hi = lo
    numpp = 0

    for y in range(len(pivotvals)-1):
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

def find_loc(strength):
    ret = len(sr_strength)
    if ret > 0:
        for i in range(len(sr_strength) - 1, -1, -1):
            if strength <= sr_strength[i]:
                break
            ret = i
            #return ret
    return ret

def check_sr(hi, lo, strength):
    ret = True

    for i in range(len(sr_up_level)):
        if (sr_up_level[i] >= lo and sr_up_level[i] <= hi) or (sr_dn_level[i] >= lo and sr_dn_level[i] <= hi):
            if strength >= sr_strength[i]:
                del sr_strength[i]
                del sr_up_level[i]
                del sr_dn_level[i]
                #return ret
            else:
                ret = False
                #return ret
            break
    return ret
                
# Check if ph or pl is True
# if len(ph) > 0 or len(pl) > 0:
if len(phl) > 0:
    # Remove old S/R levels due to new calculation
    sr_up_level.clear()
    sr_dn_level.clear()
    sr_strength.clear()
    
    # Find S/R zones
    for x in range(len(pivotvals)):
        hi, lo, strength = get_sr_vals(x)
        if check_sr(hi, lo, strength):
            loc = find_loc(strength)
            if loc <= maxnumsr and strength >= min_strength:
                sr_strength.insert(loc, strength)
                sr_up_level.insert(loc, hi)
                sr_dn_level.insert(loc, lo)
                if len(sr_strength) > maxnumsr:
                    sr_strength.pop(len(sr_strength)-1)
                    sr_up_level.pop(len(sr_up_level)-1)
                    sr_dn_level.pop(len(sr_dn_level)-1)
    # print(sr_up_level)
    # print(sr_dn_level)
    # print(sr_strength)            

    # Print support and resistance levels
    for x in range(len(sr_up_level)):
        mid = round_to_mintick((sr_up_level[x] + sr_dn_level[x]) / 2)
        rate = 100 * (mid - close[-1]) / close[-1]
        print(f"mid : {mid}, rate : {rate:.2f}%")
