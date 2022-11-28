# 네이버뉴스 타이를 제목과 카테고리만 가진 데이터로 학습을 시켜 새로운 뉴스 타이틀제목을 입력했을 때 카테고리를 분류해주는 다중분류기를 만들기

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # pip install scikit-learn
from konlpy.tag import Okt # konlpy : 한국어 정보처리를 위한 패키지 ; 형태소 단위로 잘라줌
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle
# pip install tensorflow==2.9.2
# 패키지버전은 코랩에서 찾아보는게 가장 안정적이다. 코랩에서 !pip list 입력

pd.set_option('display.unicode.east_asian_width', True)
df=pd.read_csv('./crawling_data/naver_news_titles_20221124.csv')
# print(df.head())
# print(df.category.value_counts())
# df.info()

X = df['title']     # x를 넣어서
Y = df['category']  # y를 예측함

encoder = LabelEncoder() # encoder는 아무것도 없음
Labeled_Y = encoder.fit_transform(Y) # fit_transform을 하게되면  encoder에 정보가 들어감
# print(Labeled_Y[:5])
# print(encoder.classes_) # 몇번으로 라벨링 되어있는지 저장되어 있음; 라벨인코더는 오름차순으로 정렬함
with open('./models/label_encoder.pickle','wb') as f: # encoder저장
    pickle.dump(encoder, f)
onehot_Y = to_categorical(Labeled_Y)
# print(onehot_Y[:5])

okt = Okt()
for i in range(len(X)):
    X[i] = okt_morph_X = okt.morphs(X[i], stem=True)  # 의미를 가지는 최소단위인 형태소로 문장을 자름 # .morphs() 공부 ; stem=True : 용언의 기본형으로 바꿔줌
    if i % 100 == 0:
        print('.',end='')
    if i % 10000 == 0:
        print()

stopwords = pd.read_csv('./stopwords.csv', index_col=0) # 불용어(조사, 감탄사 등) 모음 (한글 자연어학습하는데 도움이 안됨)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in stopwords['stopword']:
                words.append(X[j][i])
    X[j] = ' '.join(words) # 각각의 문자열들을 ' '를 기준으로 하나의 문자열로 만들어 줌

token = Tokenizer() #각각의 형태소마다 숫자를 부여해 분류
token.fit_on_texts(X) # x안의 값을 모두 끄집어내 유니크한 값들을 모아 => back of words (=bow)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1 ## 63-line)  작업 중 문장에 패딩을 하게되면 0이라는 형태소가 추가되기 때문에 wordsize에 +1을 해줌
# print(tokened_X)
# print(wordsize) # 문장마다 문장의 길이(형태소의 개수)가 다르다.

#token저장
with open('./models/news_token.pickle','wb')as f:
    pickle.dump(token, f)

# 딥러닝 모델에 입력변수로 넣으려면 길이를 맞춰주어야 한다. 가장 긴 문장의 형태소 갯수에 맞춰 나머지 문장들의 형태소 개수를 맞춰줘야함
max_len = 0
for i in range(len(tokened_X)):
    if max_len < len(tokened_X[i]):
        max_len = len(tokened_X[i])
print(max_len)

X_pad = pad_sequences(tokened_X, max_len) # pad : padding ; code) 가장 긴 문장의 길이에 맞게 tokended_X의 문장앞에 0을 채워줌
# print(X_pad)`

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size = 0.1)
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)
xy = X_train, X_test, Y_train, Y_test
np.save('./models/news_data_max_{}_wordsize_{}.npy'.format(max_len,wordsize),xy)


