from flask import Flask, request, render_template, jsonify
import os
import cv2
from keras.models import load_model
import numpy as np


# 모델 로딩
model_path = os.path.join(os.path.dirname(__file__),'model')

# model_age = load_model(model_path + '/cnn_fashion_model_AGE.hdf5')
# model_income = load_model(model_path + '/cnn_fashion_model_INCOME.hdf5')
# model_job = load_model(model_path + '/cnn_fashion_model_JOB.h5')
# model_style = load_model(model_path + '/cnn_fashion_model_STYLE.hdf5')
# model_year = load_model(model_path + '/fashion_year.HDF5')

model_age = load_model(model_path + '/cnn_fashion_model_AGE.hdf5', compile=False)
model_income = load_model(model_path + '/cnn_fashion_model_INCOME.hdf5', compile=False)
model_job = load_model(model_path + '/cnn_fashion_model_JOB.h5', compile=False)
model_style = load_model(model_path + '/cnn_fashion_model_STYLE.hdf5', compile=False)
model_year = load_model(model_path + '/fashion_year.HDF5', compile=False)

model_age.compile()
model_income.compile()
model_job.compile()
model_style.compile()
model_year.compile()

# 모델 결과에 따른 라벨 정보
income = {0:'250만 원 미만', 1:'250~350만 원 미만', 2:'350~450만 원 미만', 3:'450~550만 원 미만', 4:'550~650만 원 미만', 5:'650만 원 이상'}
style = {0: 'athleisure', 
        1:'bodyconscious',
        2:'cityglam' , 
        3:'classic',
        4:'disco', 
        5:'ecology', 
        6:'feminine', 
        7:'genderless', 
        8:'grunge', 
        9:'hiphop', 
        10:'hippie', 
        11:'kitsch', 
        12:'lingerie', 
        13:'lounge',
        14:'military', 
        15:'minimal', 
        16:'normcore', 
        17:'oriental', 
        18:'popart', 
        19:'powersuit', 
        20:'punk', 
        21:'space', 
        22:'sportivecasual'}

age = {0:'40~49세', 1:'30~39세', 2:'20~29세', 3:'50~60세'}
year = {0:'1950',1:'1960',2:'1970',3:'1980',4:'1990',5:'2000',6:'2010',7:'2020'}
job = {0:'전업주부', 1:'기술/전문직', 2:'판매/서비스직', 3:'사무/관리직', 4:'학생', 5:'기타'}


# 웹 구현 

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('index.html', result_message="아직 없음",internal_script="")

@app.route('/upload', methods=['POST','GET'])


def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '파일이 없습니다.'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': '파일을 선택하지 않았습니다.'})

    if file:
        filename = os.path.dirname(__file__) + '/static/upload/uploaded_image.png'
        file.save(filename)

        # 모델에 따른 이미지 처리
        # (1) 이미지 크기 400*300 처리
        img_arr_400 = np.fromfile(filename, np.uint8)
        img_data_400 = cv2.imdecode(img_arr_400, cv2.IMREAD_COLOR)
        img_data_400 = cv2.resize(img_data_400,(300,400)).reshape(1,400,300,3)/255.0
        
        # (2) 이미지 크기 100*75 처리
        img_arr_100 = np.fromfile(filename, np.uint8)
        img_data_100 = cv2.imdecode(img_arr_100, cv2.IMREAD_COLOR)
        img_data_100 = cv2.resize(img_data_100,(75,100)).reshape(1,100,75,3)/255.0
        
        # 모델을 통한 예측
        pred_result_year = year[np.argmax(model_year.predict(img_data_400))]
        pred_result_style = style[np.argmax(model_style.predict(img_data_100))]
        pred_result_job = job[np.argmax(model_job.predict(img_data_100))]
        
        arr1 = np.array([[10**6.9999,10,10**6.9992,10]])
        pred_result_age = age[np.argmax(model_age.predict(img_data_100)*arr1)]
        
        arr2 = np.array([[1.5,1,2,2.5,3,3]])
        pred_result_income = income[np.argmax(model_income.predict(img_data_100)* arr2)]

        # 'uploaded_image' 변수를 템플릿에 전달
        return render_template('index.html',  result_message=f"{pred_result_year}",
                                            result_message1=f"{pred_result_style}",
                                            result_message2=f"{pred_result_age}",
                                            result_message3=f"{pred_result_job}",
                                            result_message4=f"{pred_result_income}",
                                            internal_script="showResult();")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)