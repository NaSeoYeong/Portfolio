from flask import Flask, render_template

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# DB 연결을 위한 전역 변수 -------------------------------------------------------------------

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# mihtsyr 객체 생성
mygrate = Migrate()

# app 실행을 위한 flask 객체 생성 ----------------------------------------------------------------------
def create_app():
    import apps.model.view as model_view
    import apps.main.view as main_view

    # 플라스크 인스턴스 생성
    app = Flask(__name__)
    
    # 파일을 활용한 config 설정
    app.config.from_pyfile('config.py')
    
    # SQLAlchemy와 앱을 연계
    db.init_app(app)
    # Migrate와 앱을 연계
    mygrate.init_app(app, db)

    # 내부 기능의 view(라우팅 담당) blueprint 객체 임포트 
    app.register_blueprint(main_view.main)
    app.register_blueprint(model_view.model)

    # root 페이지 설정
    @app.route('/')
    @app.route('/main')
    def main_page():
        return render_template('main/about.html')

    return app
