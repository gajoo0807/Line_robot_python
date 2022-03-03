import requests
import pandas as pd
from bs4 import BeautifulSoup


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}

# 網路爬蟲抓取資料
resp = requests.get('https://www.sitca.org.tw/ROC/Industry/IN2422.aspx?txtYEAR=2020&txtMONTH=02&txtGROUPID=EUCA000671&txtFUNDKIND=&txtFUNDKEYWORD=&txt', headers=headers)

soup = BeautifulSoup(resp.text, 'html.parser')

# 觀察發現透過 id ctl00_ContentPlaceHolder1_TableClassList 可以取出 Morningstar table 資料。取出第一筆
table_content = soup.select('#ctl00_ContentPlaceHolder1_TableClassList')[0]

# 將 BeautifulSoup 解析的物件美化後交給 pandas 讀取 table，注意編碼為 UTF-8。取出第二筆
fund_df = pd.read_html(table_content.prettify(), encoding='utf-8')[1]

# 資料前處理，將不必要的列移除
fund_df = fund_df.drop([0])

# 設置第一列為標頭
fund_df.columns = fund_df.iloc[0]

# 去除不必要列
fund_df = fund_df.drop([1])

# 整理完後新設定 index
fund_df.reset_index(drop=True, inplace=True)

# NaN -> 0
fund_df = fund_df.fillna(value=0)

print(fund_df.dtypes)

fund_df['一個月']=fund_df['一個月'].astype(float)
fund_df['三個月']=fund_df['三個月'].astype(float)
fund_df['六個月']=fund_df['六個月'].astype(float)
fund_df['一年']=fund_df['一年'].astype(float)
fund_df['二年']=fund_df['二年'].astype(float)
fund_df['三年']=fund_df['三年'].astype(float)
fund_df['五年']=fund_df['五年'].astype(float)
fund_df['自今年以來'] = fund_df['自今年以來'].astype(float)
print(fund_df.dtypes)

half_of_row_count=len(fund_df.index)//2
rule_3_df=fund_df.sort_values(by=['三年'],ascending=['True']).nlargest(half_of_row_count,'三年')
rule_1_df=fund_df.sort_values(by=['一年'],ascending=['True']).nlargest(half_of_row_count,'一年')
rule_6_df=fund_df.sort_values(by=['六個月'],ascending=['True']).nlargest(half_of_row_count,'六個月')

rule_31_df=pd.merge(rule_3_df,rule_1_df,how='inner')
rule_316_df=pd.merge(rule_31_df,rule_6_df,how='inner')
print('三年前 1/2')
for index, row in rule_3_df.iterrows():
    print(index, row['基金名稱'], row['三年'], row['一年'], row['六個月'])


print('一年前 1/2')
for index, row in rule_1_df.iterrows():
    print(index, row['基金名稱'], row['三年'], row['一年'], row['六個月'])


print('六個月 1/2')
for index, row in rule_6_df.iterrows():
    print(index, row['基金名稱'], row['三年'], row['一年'], row['六個月'])

print('====316 法則====\n', rule_316_df)