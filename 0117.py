import pymysql
import pandas as pd
# 顯示所有列
pd.set_option('display.max_columns', None)
# 顯示所有行
pd.set_option('display.max_rows', None)
# 設定value的顯示長度為100，預設為50
pd.set_option('max_colwidth', 1000)

connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='0000',
    database='test',)
sql = 'select * from 1211_test '
df = pd.read_sql(sql, connection)
df1 = pd.DataFrame(df)  # 讀取資料庫轉為資料表
a = df1[['核心數', '特技1', '特技1']
        ] = df1.name.str.split('硬', expand=True)
print(a.fillna("找不到"))

