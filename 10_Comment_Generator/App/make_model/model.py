import numpy as np
import pickle

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, LSTM

from keras.callbacks import ModelCheckpoint


# 데이터 로딩, 개행문자 제거
with open('review.txt', 'rt', encoding='utf-8') as t:
    review = t.readlines()

review = [r.replace('\n','') for r in review][:5000]

# 띄어쓰기 기준으로 토크나이징
tokenizer = Tokenizer()
tokenizer.fit_on_texts(review)
vocab_size = len(tokenizer.word_index) + 1

# 학습에 사용할 샘플 생성
sequences = []
for line in review:
    encoded = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(encoded)):
        sequence = encoded[:i+1]
        sequences.append(sequence)

# 가장 긴 샘플의 길이
max_len = max(len(l) for l in sequences) 

# 패딩 처리
sequences = pad_sequences(sequences, maxlen=max_len, padding='pre')

# train, test 데이터 분리
sequences = np.array(sequences)
X = sequences[:,:-1]
y = sequences[:,-1]

# test 데이터 원핫인코딩
y = to_categorical(y, num_classes=vocab_size)

with open('tokenizer.pkl', 'wb') as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)

with open('categorical_data.pkl', 'wb') as categorical_file:
    pickle.dump(y, categorical_file)


embedding_dim = 10
hidden_units = 128

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(LSTM(hidden_units))
model.add(Dense(vocab_size, activation='softmax'))

checkpoint = ModelCheckpoint('best.hdf5', monitor='loss', verbose=True, save_best_only=True)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=1000, batch_size=1024, callbacks=[checkpoint])


with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

