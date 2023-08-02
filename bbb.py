from stock_indicator import Stock_indicator
import FinanceDataReader as fdr


stock_df = fdr.DataReader('005690', start = '2022-01-01' ,end = '2023-12-31')
SI = Stock_indicator(stock_df)


def get_color(noSqz, sqzOn):
    if noSqz:
        return '대기상태'
    elif sqzOn:
        return 'on'
    else:
        return 'off'
    

    
atr = SI.calculate_atr()


# Calculate Squeeze Momentum Indicator values
momentum_vals, squeeze_on, squeeze_off, no_squeeze = SI.squeeze_momentum()

# squeeze_status = get_color(no_squeeze, squeeze_on)
squeeze_status = get_color(no_squeeze.iloc[-1], squeeze_on.iloc[-1])


histogram_status = 'Plus' if momentum_vals.iloc[-1] >= 0 else 'Minus'



info_text = f"ATR: {atr[-1]}\n"
info_text += f"Squeeze Status: {squeeze_status}\n"
info_text += f"Histogram Status: {histogram_status}\n"



print(info_text)