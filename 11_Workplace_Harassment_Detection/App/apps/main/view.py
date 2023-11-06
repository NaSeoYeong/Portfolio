from flask import Blueprint, render_template, redirect, url_for, request, flash
from apps.app import db
from apps.main.db import Ask

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', url_prefix='/main')

# db index 생성을 위한 전역변수 생성 --------------------------------------------------------------------------
IDX = 0


# 모델 페이지 라우팅 ------------------------------------------------------------------------------------------
@main.route('/')
@main.route('/about')
def about_index():
    return render_template('/main/about.html')

@main.route('/howto')
def howto_index():
    return render_template('/main/howto.html')

@main.route('/ask', methods=['GET','POST'])
def ask_index():
    if request.method == 'POST':

        is_vaild = True
        
        if 'submit_button' in request.form:
            if not request.form['email']:
                flash('이메일을 입력해 주세요')
                is_vaild = False
            
            if not request.form['pw']:
                flash('비밀번호를 입력해 주세요')
                is_vaild = False
                
            if not request.form['sentence']:
                flash('요청 내용을 입력해 주세요')
                is_vaild = False
            
        if not is_vaild:
            return redirect(url_for('main.ask_index'))
            
            
        email_ = request.form['email']
        pw_ = request.form['pw']
        sentence_ = request.form['sentence']
        
        # Ask 인스턴스 생성, 데이터 할당    
        ask = Ask(email=email_, password=pw_, sentence=sentence_)
        
        # 해당 정보를 DB에 저장
        db.session.add(ask)
        db.session.commit()

        flash('요청이 처리되었습니다. 고맙습니다.')
    
        return redirect(url_for('main.ask_index'))

    return render_template('/main/ask.html')