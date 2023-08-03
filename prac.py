import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import FinanceDataReader as fdr
import numpy as np
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Information")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.code_input = QLineEdit(self)
        self.layout.addWidget(self.code_input)

        self.result_label = QLabel(self)
        self.layout.addWidget(self.result_label)

        self.button = QPushButton("Get Information", self)
        self.button.clicked.connect(self.get_stock_info)
        self.layout.addWidget(self.button)

    def get_stock_info(self):
        code = self.code_input.text()
        price_data = get_price_data(code)

        


        # print(f"종목코드 {stock_code}에 대한 정보:")
        # print(f"스쿼이즈 상태: {squeeze_status}")
        # print(f"히스토그램 상태: {histogram_status}")
        # print(f"오늘 종가는 {stock_data['Close'].iloc[-1]} 입니다.")



        if price_data is not None:
            start_price, high_price, low_price, close_price = price_data
            atr = calculate_atr(price_data)

            # Calculate Squeeze Momentum Indicator values
            momentum_vals, squeeze_on, squeeze_off, no_squeeze = squeeze_momentum_indicator(start_price, high_price, low_price, close_price)

            # squeeze_status = get_color(no_squeeze, squeeze_on)
            squeeze_status = get_color(no_squeeze.iloc[-1], squeeze_on.iloc[-1])
            
            
            histogram_status = 'Plus' if momentum_vals.iloc[-1] >= 0 else 'Minus'

        
            if squeeze_off[-2] == False and squeeze_off[-1] == True:
                if histogram_status == 'Plus':
                    long_cond = '야 얼른 사러 가라 신호 떴다.'
                else:
                    long_cond = '어 대기해라. 아직 아니다.'
            else:
                long_cond = '응 신호 없다. 다른거 찾아봐라'


            info_text = f"Start Price: {start_price.iloc[-1]:,}\n"
            info_text += f"High Price: {high_price.iloc[-1]:,}\n"
            info_text += f"Low Price: {low_price.iloc[-1]:,}\n"
            info_text += f"Close Price: {close_price.iloc[-1]:,}\n"
            info_text += f"ATR: {atr:,}\n"
            info_text += f"\n"
            info_text += f"Squeeze Status: {squeeze_status}\n"
            info_text += f"Histogram Status: {histogram_status}\n"
            info_text += f"매수 신호? {long_cond}\n"

            self.result_label.setText(info_text)

def get_price_data(code):
    # FinanceDataReader를 사용하여 주가 데이터 가져오기
    df = fdr.DataReader(code, '2023-01-01','2023-12-31')
    if len(df) < 20:
        print("데이터가 충분하지 않습니다.")
        return

    # 최근 20일간의 시가, 고가, 저가, 종가 가져오기
    start_price = df['Open']
    high_price = df['High']
    low_price = df['Low']
    close_price = df['Close']

    return start_price, high_price, low_price, close_price




def calculate_atr(price_data):
    # ATR 계산
    high_prices = np.array([data[1] for data in price_data])
    low_prices = np.array([data[2] for data in price_data])
    close_prices = np.array([data[3] for data in price_data])
    
    tr_list = np.maximum(high_prices - low_prices, np.abs(high_prices - np.roll(close_prices, 1)))
    tr_list = np.maximum(tr_list, np.abs(low_prices - np.roll(close_prices, 1)))
    atr = np.mean(tr_list[-20:])
    
    return atr




def squeeze_momentum_indicator(open, high, low, close):

    bb_length = 14
    bb_multfactor = 2
    kc_length = 16
    kc_multfactor = 1.5
    use_truerange = True
    
    # Calculate Bollinger Bands
    basis = close.rolling(window=bb_length).mean()
    dev = bb_multfactor * close.rolling(window=bb_length).std()
    upper_bb = basis + dev
    lower_bb = basis - dev

    # Calculate Keltner Channels
    ma = close.rolling(window=kc_length).mean()
    if use_truerange:
        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift()))
        tr3 = pd.DataFrame(abs(close.shift() - low))
        frame = pd.concat([tr1, tr2, tr3], axis=1)
        range_val = np.max(frame, axis=1)
    else:
        range_val = high - low
    
    rangema = range_val.rolling(window=kc_length).mean()
    upper_kc = ma + rangema * kc_multfactor
    lower_kc = ma - rangema * kc_multfactor

    # Determine squeeze criteria
    sqz_on = (lower_bb > lower_kc) & (upper_bb < upper_kc)
    sqz_off = (lower_bb < lower_kc) & (upper_bb > upper_kc)
    no_sqz = (~sqz_on) & (~sqz_off)

    # Calculate Squeeze Momentum value
    highest_high = high.rolling(window=kc_length).max()
    lowest_low = low.rolling(window=kc_length).min()
    sma_close = close.rolling(window=kc_length).mean()
    val = (close - ((highest_high + lowest_low) / 2 + sma_close) / 2).rolling(window=kc_length).apply(np.sum)


    return val, sqz_on, sqz_off, no_sqz



def get_color(noSqz, sqzOn):
    if noSqz:
        return '대기상태'
    elif sqzOn:
        return 'on'
    else:
        return 'off'
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
