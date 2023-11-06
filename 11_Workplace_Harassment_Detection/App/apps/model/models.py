from konlpy.tag import Kkma
import pandas as pd
import pickle
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


# (1) 모델 로드
model_path = os.path.dirname(__file__) + '/make_model/'
model = load_model(model_path+ 'best_model.hdf5')

# (2) 대화를 모델 사용 가능한 형식으로 변환 함수
def make_test(text):
    kkma = Kkma()

    with open(model_path+'tokenizer.pkl', 'rb') as tokenizer_model:
        tokenizer = pickle.load(tokenizer_model)

    result = []
    one = kkma.pos(text)

    for t, v in one:
        if v in ['NNG','NNP','NP', 'VV','VA', 'VCP','VCN', 'IC', 'MAG']:
            result.append(t)

    pre_data = pd.Series(', '.join(result))
    pre_data = pre_data.values

    pre = tokenizer.texts_to_sequences(pre_data)
    pre = pad_sequences(pre, maxlen=300)

    return pre

# (3) 결과 예측 함수
def predict(model, fst, sec):
    data = fst + ' ' + sec

    pre_data = make_test(data)
    
    result = model.predict(pre_data)[0][0]

    if result >= 0.1:
        return ("정상 대화입니다", result)
    else:
        return ("직장 내 괴롭힘 대화입니다.", result)