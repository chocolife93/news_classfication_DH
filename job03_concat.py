import pandas as pd
import glob                 # glob 패키지 공부
import datetime             # datetime 패키지와 time 패키지의 다른점 공부

data_path = glob.glob('./crawling_data/*.csv')
print(data_path)
df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp], ignore_index=True)
df.dropna(inplace=True)
df.reset_index(inplace=True, drop = True)
print(df.head())
df.info()
df.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')),index=False)
