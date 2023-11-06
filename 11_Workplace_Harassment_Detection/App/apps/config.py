import os

SECRET_KEY="ALSKDJFQOAWIEA123541"

# DB와의 연결 설정--------------------------------------------------------------------
DB_MARIA_URI = 'mariadb+mariadbconnector://root:root@localhost:3306/sentence_db'

# 사용할 DB 설정----------------------------------------------------------------------
# 사용할 DB 지정
SQLALCHEMY_DATABASE_URI = DB_MARIA_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False
# SQL을 콘솔 로그에 출력
SQLALCHEMY_ECHO=True

