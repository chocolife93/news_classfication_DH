import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import*

# 데이터 불러오기
X_train, X_test, Y_train, Y_test = np.load('./models/news_data_max_20_wordsize_11911.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

# 모델생성
model = Sequential()
model.add(Embedding(11911, 300, input_length = 20)) # Embedding 레이어 : ; code) Embedding(데이터개수, , )
'''
    https://simpling.tistory.com/entry/Embedding-%EC%9D%B4%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0
    인간의 언어(자연어)는 수치화되어 있지 않은 데이터이기 때문에 머신러닝, 딥러닝 기법을 바로 사용할 수가 없다.
    (수치화되어있는 데이터의 예로는 Mnist나 꽃의 종류처럼 숫자로 분류가 가능한 것들을 말함.)
    그래서 자연어 처리에서 특징 추출을 통해 수치화를 해줘야 하는데 이때 사용하는 것이 "언어의 벡터화"이다.
    이런 벡터화의 과정을 Word Embedding이라고 한다. 그 중 하나가 one-hot encoding이다 ...
'''
    # 언어의 백터화 ; 의미공간 ; 차원의 저주 : 차원이 늘어나면 데이터는 희소해진다 ;
model.add(Conv1D(32, kernel_size=5, padding='same', activation = 'relu')) # conv1D : 1차원 cnn
model.add(MaxPool1D(pool_size=1))
model.add(GRU(128, activation = 'tanh', return_sequences=True)) #GRU layer : lstm의 성능은 유지하고 속도가 빨라진 레이어(rnn 레이어), 순서가 있는 데이터 ;; return_sequences :
model.add(Dropout(0.3))
model.add(GRU(64, activation='tanh',return_sequences=True))
model.add(Dropout(0.3))
model.add(GRU(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten()) # 여러겹의 데이터를 한줄로 reshape해주는 레이어()
model.add(Dense(128, activation = 'relu'))
model.add(Dense(6, activation='softmax')) # 분류할 클래스가 6개, 다중분류기이므로 활성화함수는 소프트맥스
model.summary()

'''
 cnn은 이미지(상하좌우 위치데이터가 있음), rnn은 1차원 데이터(앞뒤관계,시계열자료,단어 등 예측에 좋은 성능), Dense레이어는 점
 LSTM이 성능은 유지하면서 학습속도를 높인것이 GRU(국산 ; 성능이 더 좋은 것이 아님 acuraccy가 높아지지 않음, 단순히 속도가 빠름; 매개변수는 lstm과 똑같아서 사용법이 같음)
 RNN쓰려면 레이어를 SimpleRNN을 쓰면 됨
 트렌스포머는 자연어처리할 때 주로 쓰임
 cnn 이미지, lstm 시계열,
'''


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs = 10, validation_data=(X_test, Y_test))

# 모델 저장
model.save('./models/news_category_classfication_model_{}.h5'.format(np.round(fit_hist.history['val_accuracy'][-1],3)))

plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()


'''
질문
1. 모델 생성 : 첫번째 레이어로 GRU로 시작하지 않고 Conv1D레이어로 시작하는 이유
2.
'''

