import pandas as pd
import numpy as np
import FinanceDataReader as fdr

codeNumber = str(input("종목 코드를 입력하세요"))
# 가격 데이터 가져오기 (주식 코드: '삼성전자' 예시)
df = fdr.DataReader(codeNumber, '2020-06-24', '2023-07-07')  # 시작일과 종료일을 원하는 기간으로 설정해야 합니다.

# 필요한 컬럼 추출
high = df['High']
low = df['Low']
close = df['Close']

# ATR 계산을 위한 TR 계산
tr = np.maximum(
    np.maximum(high - low, np.abs(high - close.shift(1))),
    np.abs(low - close.shift(1))
)

# ATR 계산 (20일 기간 평균)
atr = tr.rolling(window=20).mean()

# 최근 1년 데이터 선택
one_year_data = df[-224:]  # 252는 약 1년 동안의 거래일 수입니다.

# 20일 기준의 ATR 값을 가져옵니다.
last_20_days_atr = atr.iloc[-20:]

# 터틀트레이딩 방식에 따라 자산 배분 계산을 수행합니다.
total_assets = 5000000  # 총 자산 (예시: 500만원)
risk_per_trade = 0.02  # 개별 거래 위험 비율 (2%)
unit_per_trade = (risk_per_trade * total_assets) / last_20_days_atr.iloc[-1]
print("*******************************************************")
print("**                                                   **")
print("**                 주식 얼마에 살래?                 **")
print("**                                                   **")
print("*******************************************************")


print(f"1ATR은 {last_20_days_atr[-1]}입니다. ")
print(f"현재 주가는 {close[-1]}이고 손절 주가는{close[-1] - last_20_days_atr[-1]}입니다.")
print(f"한 거래당 투자해야 할 단위:{int(unit_per_trade)}")
print(f"그래서 총 매수금액은 {int(unit_per_trade * close[-1])}원 이오.")






# import FinanceDataReader as fdr

# # 가격 데이터 가져오기 (주식 코드: '005930' 삼성전자 예시)
# df = fdr.DataReader('093640', '2020-06-24', '2023-06-24')  # 시작일과 종료일을 원하는 기간으로 설정해야 합니다.

# # 터틀트레이딩 파라미터 설정
# entry_period = 20  # 매수 진입 기간 (예시: 20일)
# exit_period = 10  # 매도 청산 기간 (예시: 10일)
# risk_per_trade = 0.02  # 개별 거래 위험 비율 (2%)

# # 매수/매도 신호 계산
# df['high_entry'] = df['Close'].rolling(window=entry_period).max()
# df['low_entry'] = df['Close'].rolling(window=entry_period).min()
# df['high_exit'] = df['Close'].rolling(window=exit_period).max()
# df['low_exit'] = df['Close'].rolling(window=exit_period).min()

# df['buy_signal'] = df['Close'] > df['high_entry']
# df['sell_signal'] = df['Close'] < df['low_exit']

# # 투자 금액 계산
# total_assets = 100000000  # 총 자산 (예시: 100,000 달러)
# unit_per_trade = risk_per_trade * total_assets

# # 매매 시그널에 따라 매수/매도 수행
# position = 0  # 0: 현금 보유, 1: 주식 보유
# for i in range(len(df)):
#     if df['buy_signal'].iloc[i] and position == 0:
#         shares_to_buy = unit_per_trade / df['Close'].iloc[i]
#         position = 1
#         print(f"{df.index[i].date()}: 매수, 보유 주식 수: {shares_to_buy:.2f}")

#     elif df['sell_signal'].iloc[i] and position == 1:
#         shares_to_sell = unit_per_trade / df['Close'].iloc[i]
#         position = 0
#         print(f"{df.index[i].date()}: 매도, 보유 주식 수: {shares_to_sell:.2f}")

# # 마지막에 주식을 보유한 상태라면, 모두 매도
# if position == 1:
#     shares_to_sell = unit_per_trade / df['Close'].iloc[-1]
#     print(f"마지막 날짜: 매도, 보유 주식 수: {shares_to_sell:.2f}")
