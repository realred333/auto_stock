import FinanceDataReader as fdr

def save_codes_with_fs_month(filename):
    krx_list = fdr.StockListing("KRX")
    
    # 결산월(column: '결산월')이 결측치가 아닌 종목만 선택
    filtered_list = krx_list[krx_list['SettleMonth'].notna()]
    
    codes = filtered_list['Symbol']

    with open(filename, "w") as f:
        for code in codes:
            f.write(f"{code}\n")

filename = "code.txt"
save_codes_with_fs_month(filename)
