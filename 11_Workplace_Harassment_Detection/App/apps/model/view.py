from flask import Blueprint, render_template, redirect, url_for, request

model = Blueprint('model', __name__, template_folder='templates', static_folder='static', url_prefix='/model')


# 데이터 저장을 위한 전역 변수
history = []
predict_history = []

# 모델 페이지 라우팅
@model.route('/workplace', methods=['GET','POST'])
def workplace_index():
    from apps.model.models import model, predict
    global history

    if request.method == 'POST':

        # post 방식일 때 데이터 처리 - 저장 혹은 초기화
        if 'submit_button' in request.form:
            sent_ = request.form['sent']
            history.append(sent_)

        if 'clear_button' in request.form:
            history.clear()
            predict_history.clear()

        # 모델 결과 확인
        if len(history) >= 2:
            result_ = predict(model, history[-2], history[-1])
            predict_history.append(result_)

        return redirect(url_for('model.workplace_index'))
    
    return render_template('/model/workplace.html', hist=history, result=predict_history)


@model.route('/school', methods=['GET','POST'])
def school_index():

    if request.method == 'POST':
        if 'home_button' in request.form:
            return redirect(url_for('main.about_index'))
        
    return render_template('/model/school.html')