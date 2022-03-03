import requests
import pandas as pd
from bs4 import BeautifulSoup

url='https://www.sitca.org.tw/ROC/Industry/IN2422.aspx?txtYEAR=2020&txtMONTH=12&txtGROUPID=EUCA000502'
headers={
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}
resp=requests.get(url,headers=headers)
soup=BeautifulSoup(resp.text,'html.parser')
table_content = soup.select('#ctl00_ContentPlaceHolder1_TableClassList')[0]
fund_df = pd.read_html(table_content.prettify(), encoding='utf-8')[1]
fund_df=fund_df.drop(index=[0])
fund_df.columns=fund_df.iloc[0]
fund_df=fund_df.drop(index=[1])
fund_df.reset_index(drop=True, inplace=True)
fund_df = fund_df.fillna(value=0)

fund_df['一個月']=fund_df['一個月'].astype(float)
fund_df['三個月']=fund_df['三個月'].astype(float)
fund_df['六個月']=fund_df['六個月'].astype(float)
fund_df['一年']=fund_df['一年'].astype(float)
fund_df['二年']=fund_df['二年'].astype(float)
fund_df['三年']=fund_df['三年'].astype(float)
fund_df['五年']=fund_df['五年'].astype(float)
fund_df['自今年以來'] = fund_df['自今年以來'].astype(float)
half_of_row_count=len(fund_df.index)//2

rule_3_df=fund_df.sort_values(by=['三年'],ascending=['True']).nlargest(half_of_row_count,'三年')
rule_1_df=fund_df.sort_values(by=['一年'],ascending=['True']).nlargest(half_of_row_count,'一年')
rule_6_df=fund_df.sort_values(by=['六個月'],ascending=['True']).nlargest(half_of_row_count,'六個月')

rule_31_df=pd.merge(rule_3_df,rule_1_df,how='inner')
rule_316_df=pd.merge(rule_31_df,rule_6_df,how='inner')
print('====316 法則====\n', rule_316_df)