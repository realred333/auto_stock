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
        if price_data is not None:
            start_price, high_price, low_price, close_price = price_data
            atr = calculate_atr(price_data)

            info_text = f"Start Price: {start_price.iloc[-1]}\n"
            info_text += f"High Price: {high_price.iloc[-1]}\n"
            info_text += f"Low Price: {low_price.iloc[-1]}\n"
            info_text += f"Close Price: {close_price.iloc[-1]}\n"
            info_text += f"ATR: {atr}"
            
            self.result_label.setText(info_text)

def get_price_data(code):
    # FinanceDataReader를 사용하여 주가 데이터 가져오기
    df = fdr.DataReader(code, '2023-02-01','2023-07-07')
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
