from bs4 import BeautifulSoup
import requests # url주소를 가진 서버에 요청을 함
import re
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

category = ['Politics', 'Economic', 'social', 'Culture', 'World', 'IT']

# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100' # 정치
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101' # 경제
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102' # 사회
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103' # 생활/문화
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104' # 세계
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105' # IT



headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'} # 인터넷브라우저에서 F12 누르고 network에서 아무거나 하나 누른다음 header창 맨아래에 user-agent 부분 싹 긁어서 붙여넣기, 네이버가 이걸 안해주면 크롤링 못하게 막아버림
df_titles = pd.DataFrame()
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)
    # print(list(resp))
    soup = BeautifulSoup(resp.text, 'html.parser') # html문서형태로 보기좋게 바꿔줌
    # print(soup)
    title_tags = soup.select('.cluster_text_headline') # .을 붙이면 class =>> soup안에 cluster_text_headline이라는 클래스를 가진 텍스트를 뽑음
    titles = []
    for title_tag in title_tags :
        # print(title_tag.text) # 뉴스타이틀 모음
        titles.append(title_tag)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
print(df_titles)
print(df_titles.category.value_counts())
df_titles.to_csv('./crawlind_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)