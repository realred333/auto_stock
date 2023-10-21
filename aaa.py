import FinanceDataReader as fdr
import os

df = fdr.StockListing('KOSPI')
kospi_codes = df['Code']
df = fdr.StockListing('KOSDAQ')
# 'Dept' 열에서 'SPAC(소속부없음)'을 제외한 행만 선택
filtered_df = df[~df['Dept'].str.contains('소속부없음')]
kosdaq_codes = filtered_df['Code']

# 코스닥 종목 코드를 파일에 저장
with open('kosdaq.txt', 'w') as file:
    for code in kosdaq_codes:
        file.write(code + '\n')

# 코스피 종목 코드를 파일에 저장
with open('kospi.txt', 'w') as file:
    for code in kospi_codes:
        file.write(code + '\n')
        
