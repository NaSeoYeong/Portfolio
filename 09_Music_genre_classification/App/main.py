from flask import Flask, request, render_template
import os
import joblib
from konlpy.tag import Okt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


"""
# URL : http://127.0.0.1:8080/
"""


# 전역 변수 ------------------------------------------------------------------
# (1) 데이터 모델 형식에 맞게 변환하는 함수 구현 ----------------------------------
def trans_data(text):
    df = pd.read_csv(os.path.dirname(__file__) + "/make_model/data/data.csv")

    # 벡터화
    cv = CountVectorizer()
    dtm = cv.fit_transform(df["data"])

    okt = Okt()
    words = []

    for w, t in okt.pos(text):
        if t in ["Noun", "Verb", "Adjective", "Alpha"]:
            words.append(w)
        elif (t == "Punctuation") and ("*" in w):
            words.append(w)

    sent = pd.DataFrame([" ".join(words)])
    dtm = cv.transform(sent.iloc[0])
    data = pd.DataFrame(dtm.toarray(), columns=cv.get_feature_names_out())

    return data


# (2) 모델을 통한 장르, 긍정 분류 함수 ---------------------------------------
def genre_predict(text):
    result = genre_model.predict(trans_data(text))
    return result[0]


def pn_predict(text):
    result = pn_model.predict(trans_data(text))
    if result[0] == 0:
        return "부정"
    elif result[0] == 1:
        return "긍정"


# 모델 호출 ---------------------------------------------------------------
# (1) 장르 분류 모델 호출
genre_pklfile = os.path.dirname(__file__) + "/make_model/pycaret_model.pkl"
genre_model = joblib.load(genre_pklfile)

# (2) 감성 분류 모델 호출
pn_pklfile = os.path.dirname(__file__) + "/make_model/pn_model.pkl"
pn_model = joblib.load(pn_pklfile)


# App 구현 ---------------------------------------------------------------
# Flask 객체 생성
app = Flask(__name__)

# templates 폴더 경로 선언
template_dir = os.path.join(os.path.dirname(__file__), "templates")


# main 페이지 라우팅
@app.route("/")
def index():
    return render_template("main.html")


# 텍스트 데이터를 전처리하여 모델에 넘긴 후 결과에 따른 페이지 라우팅
@app.route("/upload_done", methods=["GET"])
def upload_done():
    _id = int(request.args.get("id"))
    _lyric = request.args.get("lyric")

    if _id == 0:
        result1 = genre_predict(_lyric)
        return (
            open(template_dir + "/result1.html", mode="r", encoding="UTF-8")
            .read()
            .replace("<result1>", result1)
        )

    elif _id == 1:
        result2 = pn_predict(_lyric)
        return (
            open(template_dir + "/result2.html", mode="r", encoding="UTF-8")
            .read()
            .replace("<result2>", result2)
        )


# App 실행부 ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
