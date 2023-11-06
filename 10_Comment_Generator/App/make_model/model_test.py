import pickle
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences



def model_predict(model, current_word): # 모델, 토크나이저, 현재 단어, 반복할 횟수
    
    with open('tokenizer.pkl', 'rb') as tokenizer_file:
        tokenizer = pickle.load(tokenizer_file)

    encoded = tokenizer.texts_to_sequences([current_word])[0]
    encoded = pad_sequences([encoded], maxlen=26, padding='pre')

    # 입력한 X(현재 단어)에 대해서 y를 예측하고 예측 결과와 확률 top3을 저장
    result = model.predict(encoded, verbose=0)

    top3_proba = np.sort(result, axis=1)[:, -3:][:, ::-1]
    flat_top3_proba = top3_proba.ravel().tolist()

    top3_indices = np.argsort(result, axis=1)[:, -3:][:, ::-1]
    flat_top3_indices = top3_indices.ravel().tolist()

    return tuple(zip(flat_top3_indices, flat_top3_proba))


# 모델 로드
with open('./models/best_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


# 토크나이저 로드
with open('./models/tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

# to_categorical() 결과 로드
with open('./models/categorical_data.pkl', 'rb') as one_hot_file:
    cate = pickle.load(one_hot_file)


if __name__ == '__main__':
    # 모델 예측 결과 확인
    print(model_predict(model, input('확인할 단어를 입력하세요: ')))



