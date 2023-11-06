import os
import pickle
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences


# 모델 로드
with open(os.path.dirname(__file__)+'/models/best_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# 토크나이저 로드
with open(os.path.dirname(__file__)+'/models/tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

# 숫자->문자 변환을 위한 dict 선언
index_to_word = {index: word for word, index in tokenizer.word_index.items()}

def model_predict(model, tokenizer, current_word): # 모델, 토크나이저, 현재 단어, 반복할 횟수

    init_word = current_word
    sentence = ''

    encoded = tokenizer.texts_to_sequences([current_word])[0]
    encoded = pad_sequences([encoded], maxlen=26, padding='pre')

    # 입력한 X(현재 단어)에 대해서 y를 예측하고 예측 결과와 확률 top3을 저장
    result = model.predict(encoded, verbose=0)


    top3_proba = np.sort(result, axis=1)[:, -3:][:, ::-1]
    flat_top3_proba = top3_proba.ravel().tolist()

    top3_indices = np.argsort(result, axis=1)[:, -3:][:, ::-1]
    flat_top3_indices = top3_indices.ravel().tolist()
    flat_top3_indices = [index_to_word[index] for index in flat_top3_indices]

    return tuple(zip(flat_top3_indices, flat_top3_proba))

result = model_predict(model, tokenizer, '피부에 착')

print(result[2][0])

