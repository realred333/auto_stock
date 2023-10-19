import pandas as pd
import yfinance as yf
import numpy as np

# 입력 변수 설정
symbol = "AAPL"  # 종목 코드 (예: Apple Inc.)
start_date = "2021-01-01"
end_date = "2021-12-31"
perc = 1.0  # 퍼센트 스텝
num_levels = 5  # 레벨의 수

# yfinance 라이브러리를 사용하여 주가 데이터를 읽어옵니다.
ticker = yf.Ticker(symbol)
price_data = ticker.history(period="1d", start=start_date, end=end_date)

# 종가를 사용하여 DataFrame에 단계를 추가합니다.
price_data['Step'] = price_data['Close'] * (perc / 100)

# 기대 점수 및 레벨을 계산하는 함수
def calculate_score(price_data, num_levels):
    levels = (np.arange(1, num_levels + 1) * price_data['Step'].mean()).tolist()
    return levels

# 해당 레벨에 대한 기대 점수를 계산하는 함수
def calculate_expected_score(price_data, levels):
    results = []
    
    for level in levels:
        win_condition = price_data['Close'].shift(-1) >= (price_data['Close'] + level)
        loss_condition = price_data['Close'].shift(-1) < (price_data['Close'] - level)
        
        win_count = win_condition.sum()
        loss_count = loss_condition.sum()
        
        if win_count + loss_count != 0:
            win_ratio = win_count / (win_count + loss_count)
        else:
            win_ratio = 0.0
            
        results.append(win_ratio)
    
    return results

# 레벨과 기대 점수를 계산합니다.
levels = calculate_score(price_data, num_levels)
expected_scores = calculate_expected_score(price_data, levels)

# 결과 출력
print(f"{'Level':<10}{'Percentage':<15}{'Expected Score':<15}")
for i, (level, score) in enumerate(zip(levels, expected_scores), start=1):
    print(f"{i:<10}{level:<15.2f}{score:<15.2f}")
