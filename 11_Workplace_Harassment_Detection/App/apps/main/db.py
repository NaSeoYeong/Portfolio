from apps.app import db

# db.Model을 상속한 user 클래스 작성
class Ask(db.Model):
    
    # 테이블명 지정
    __tablename__ = 'ask'

    # 컬럼 정의
    idx = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True)
    password = db.Column(db.String(100))
    sentence = db.Column(db.String(10000))