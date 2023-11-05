from flask import Flask, request, redirect, render_template, url_for

import os
import cv2
import joblib


"""
# URL : http://127.0.0.1:8080/
"""


app = Flask(__name__)


# 기능 구현 -----------------------------------------------------

# 모델 로드
pklfile = os.path.dirname(__file__) + "/make_model/model.pkl"
print(pklfile)
clf = joblib.load(pklfile)

# 판정 힘수 구현
def recycle_predict(img):
    res = clf.predict(img)
    return str(res[0])

# 페이지 라우팅 --------------------------------------------------
# main 페이지
@app.route("/")
def index():
    return render_template("main.html")


# glass 페이지
@app.route("/glass")
def glass():
    return render_template("glass.html")


# can 페이지
@app.route("/can")
def can():
    return render_template("can.html")


# paper 페이지
@app.route("/paper")
def paper():
    return render_template("paper.html")


# plastic 페이지
@app.route("/plastic")
def plastic():
    return render_template("plastic.html")


# styrofoam 페이지
@app.route("/styrofoam")
def styrofoam():
    return render_template("styrofoam.html")


# 업로드 이미지 예측 후 관련 카테고리 분리수거 방법 페이지로 전환
@app.route("/upload_done", methods=["POST"])
def upload_done():
    try:
        uploaded_files = request.files["file"]
        uploaded_files.save("./static/img/{}.jpeg".format(1))
        filepath = "./static/img/1.jpeg"
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (150, 150))
        img = img.reshape(-1, (150 * 150))

        result = recycle_predict(img)
        print(result)

        if str(result) == "glass":
            return redirect(url_for("glass"))
        elif str(result) == "can":
            return redirect(url_for("can"))
        elif str(result) == "paper":
            return redirect(url_for("paper"))
        elif str(result) == "plastic":
            return redirect(url_for("plastic"))
        elif str(result) == "styrofoam":
            return redirect(url_for("styrofoam"))

    except:
        return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
