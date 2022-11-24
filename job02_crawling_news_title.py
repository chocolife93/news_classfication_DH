#driver를 사용한 크롤링 방법 : 브라우저드라이버를 사용하여 컴퓨터가 직접 크롤링을 함

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'social', 'Culture', 'World', 'IT']
# pages = [167, 377, 505, 71, 94, 73] # 데이터의 불균형을 맞춰줘야한다 , 그렇지 않으면 데이터가 많은 쪽으로 치우져져 학습할 수 있다.
pages = [100, 100, 100, 70, 93, 72] # 마지막 페이지에는 뉴스가 꽉 채워져있지 않을 수도 있으므로 그 전 페이지까지만 취급

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options) # 인터넷에서 자신이 쓰는 크롬의 버전과 같은 버전으로 크롬드라이버.exe파일을 설치해야함
# x_path = '//*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a' # @@@@@ xpath가 뭔지 공부
# title = driver.find_element('xpath',x_path).text
# print(title)
df_title = pd.DataFrame()
for i in range(0, 6):  # section    #섹션 반복(섹션은 0부터 시작함)
    titles = []
    for j in range(1, 11):  #page # 페이지 반복(페이지는 1부터 시작함)
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i,j)
        driver.get(url)
        time.sleep(0.2) # driver가 0.2초동안

        for k in range(1,5):    # x_path
            for l in range(1,6):    # x_path
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k,l) # @@@@@ xpath가 뭔지 공부
                         #   에러가 난것들의 차이
                         # '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[1]/a'       이미지가 있는 뉴스의 이미지xpath
                         # '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'          이미지가 없는 뉴스의 xpath
                         #   에러가 난 이유를 찾고 에러난 데이터까지 필요한 경우 챙겨줘야한다 ==>> except에서 코딩으로 채워줌
                try:
                    title = driver.find_element('xpath',x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ',title)
                    titles.append(title)
                except NoSuchElementException as e:     # 이미지가 없는 뉴스도 크롤링할 수 있도록 코드작성
                    x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
                except:
                    print('error',i,j,k,l)
        if j % 10 ==0:  # 중간에 에러가 날 것을 대비하여 중간저장 ; 크롤링은 네트워크 통신 환경에 영향을 많이받음 -> 에러가 날 것을 가정으로 코딩해야한다
            df_section_title = pd.DataFrame(titles, columns=['title'])
            df_section_title['category'] = category[i]
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(category[i],j),index=False)
            titles=[]

