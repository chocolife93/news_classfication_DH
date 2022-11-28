import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # pip install scikit-learn
from konlpy.tag import Okt # konlpy : 한국어 정보처리를 위한 패키지 ; 형태소 단위로 잘라줌
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle
from keras.models import load_model

pd.set_option('display.unicode.east_asian_width',True) # 출력에서 어느정도 줄을 맞춰줌 -> 깊게공부 X
pd.set_option('display.max_columns',15) # 깊게공부 X

# 데이터 불러오기
df = pd.read_csv('./crawling_data/naver_headline_news_20221128.csv')
print(df.head())
df.info()

X=df['title']
Y=df['category']
# 라벨인코더 불러오기
with open('./models/label_encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
labeled_Y = encoder.transform(Y)
onehot_Y = to_categorical(labeled_Y)

#형태소 분리
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

# 토큰화
with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_X = token.texts_to_sequences(X)
#길이가 20개 넘는 애들은 20개 넘는 데이터들 잘라내기
for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 20:
        tokened_X[i] = tokened_X[i][:20]
X_pad = pad_sequences(tokened_X,20)

# 모델불러오기 & 예측하기
model = load_model('./models/news_category_classfication_model_0.993.h5')
preds = model.predict(X_pad)
label = encoder.classes_
category_preds=[]
for pred in preds :
    category_pred = label[np.argmax(pred)]
    category_preds.append(category_pred)
df['predict'] = category_preds

# 예측이 맞았는지 확인하기
df['OX'] = False
for i in range(len(df)):
    if df.loc[i,'category'] == df.loc[i,'predict']:
        df.loc[i,'OX'] = True
print(df.head(30))
print(df['OX'].value_counts())
print(df['OX'].mean()) # 정답률
print(df.loc[df['OX']==False])