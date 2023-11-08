import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


all_df = pd.read_csv('./pos.csv')

train, test = train_test_split(all_df, test_size=0.2, random_state=0, stratify=all_df['label'])

train_X = train['pos'].values
train_y = train['label'].values

test_X = test['pos'].values
test_y = test['label'].values

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_X)


threshold = 2
total_cnt = len(tokenizer.word_index)   # 단어의 수
rare_cnt = 0                            # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0                          # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0                           # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합


# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

vocab_size = total_cnt - rare_cnt + 2

tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
tokenizer.fit_on_texts(train_X)

with open('tokenizer.pkl', 'wb') as token_file:
    pickle.dump(tokenizer, token_file)

train_X = tokenizer.texts_to_sequences(train_X)
test_X = tokenizer.texts_to_sequences(test_X)

train_X = pad_sequences(train_X, maxlen=300)
test_X = pad_sequences(test_X, maxlen=300)


embedding_dim = 100
hidden_units = 128

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(LSTM(hidden_units))
model.add(Dense(1, activation='sigmoid'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('best_model.hdf5', verbose=1, save_best_only=True)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_X, train_y, epochs=100, callbacks=[mc, es], batch_size=512, validation_data=(test_X, test_y))

with open('final_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)