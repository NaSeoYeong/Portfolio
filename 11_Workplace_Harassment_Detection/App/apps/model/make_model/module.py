import mariadb as mdb
import json
import os

from konlpy.tag import Kkma


# 사용 함수 선언
# (1) 문장 파싱을 위한 함수 선언 -------------------------------------------------

kkma = Kkma()

def make_pos(data):
    
    all_result = []

    for sent in data:
        result = []
        text = kkma.pos(sent)
        for t, v in text:
            if v in ['NNG','NNP','NP', 'VV','VA', 'VCP','VCN', 'IC', 'MAG']:
                result.append(t)
        all_result.append(', '.join(result))
    
    return all_result


# (2) json 파일 로드 후 '회사/아르바이트' 데이터만 DB에 저장하는 함수 선언 -----------

def read_json(folder_name):

    # DB 연결 정보
    conn_params = {'host':"localhost",
                'port':3306,
                'user':'root',
                'password':'root'}

    conn = mdb.connect(**conn_params)

    # DB에 연결하기
    conn = mdb.connect(**conn_params)

    # DB에 접근할 커서 객체 생성
    cur = conn.cursor()

    # 가져올 파일 경로 설정
    path = f'./{folder_name}/'
    files = os.listdir(f'{folder_name}')

    # 커밋 횟수 설정
    com_cnt = 0
    # DB에 데이터 저장
    for file in files:
        try:
            com_cnt += 1
            with open(path+file, 'r') as f: 
                    data = json.load(f)
                    if data['info'][0]['annotations']['subject'] == '회사/아르바이트':
                        result = data['info'][0]['annotations']['text']
                        cur.execute("USE text_db")
                        cur.execute("INSERT INTO positive_data(filename, conversation) VALUES (?, ?)",[file, result])
            if com_cnt % 10 == 0:
                # 데이터 커밋하기     
                conn.commit()

        except:
            print(file)

    # 커서와 DB연결 종료
    cur.close()
    conn.close()


# (3) DB에서 데이터 가져오는 함수 선언 ---------------------------------------------

def get_data(col, table):
    conn_params = {'host':"localhost",
                'port':3306,
                'user':'root',
                'password':'root'}

    try:
        # DB에 연결하기
        conn = mdb.connect(**conn_params)

        # DB에 접근할 커서 객체 생성
        cur = conn.cursor()

        # 데이터 가져오기
        cur.execute("USE text_db;")
        cur.execute(f"SELECT {col} FROM {table}")

        data = cur.fetchall()

        # 커서와 DB연결 종료
        cur.close()
        conn.close()

    except mdb.Error as e:
        print(f'Error: {e}')
    
    return data