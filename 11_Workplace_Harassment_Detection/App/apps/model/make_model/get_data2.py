import mariadb as mdb
import pandas as pd

from module import get_data

# DB 연결 정보
conn_params = {'host':"localhost",
            'port':3306,
            'user':'root',
            'password':'root'}


# (1) 대화 분리 후 DB에 저장 -------------------------------------------------------------

# DB에 연결하기
conn = mdb.connect(**conn_params)

# DB에 접근할 커서 객체 생성
cur = conn.cursor()

# (1-1) 긍정 대화 분리 후 DB 저장
# 데이터 가져오기
cur.execute("USE text_db;")
cur.execute("SELECT idx, conversation FROM positive_data")

positive_data = cur.fetchall()

# 데이터 입력하기
for idx, con in positive_data:
    texts = con.split('\n')
    for i in texts:
        if ':' in i:
            i = i.split(':')[1]
        cur.execute("USE text_db;")
        cur.execute("INSERT INTO positive_one(idx, conversation) VALUES (?,?)", [idx, i])
    
    conn.commit()

# (1-2) 부정 대화 분리 후 DB 저장
# 데이터 가져오기
negative_df = pd.read_csv('./train.csv')
negative_df = negative_df[negative_df['class']=='직장 내 괴롭힘 대화'].copy()
negative_df.reset_index(inplace=True, drop=True)

# 데이터 입력하기
for idx, con in zip(negative_df['idx'], negative_df['conversation']):
    texts = con.split('\n')
    for i in texts:
        cur.execute("USE text_db;")
        cur.execute("INSERT INTO negative_one(idx, conversation) VALUES (?,?)", [idx, i])

# 커서와 DB연결 종료
cur.close()
conn.close()


# (2) Q&A 분리 데이터 가져와 CSV로 저장 ----------------------------------------------------
# DB에 연결하기
conn = mdb.connect(**conn_params)

# DB에 접근할 커서 객체 생성
cur = conn.cursor()

cur.execute("USE text_db;")
cur.execute("SELECT Q,A FROM negative_Q")

# 부정 데이터 저장
ne_data = cur.fetchall()

ne_df = pd.DataFrame(ne_data, columns=['Q','A'])
ne_df.to_csv('negative_QA.csv', index=False)

cur.execute("USE text_db;")
cur.execute("SELECT Q,A FROM positive_Q")

# 긍정 데이터 저장
po_data = cur.fetchall()

po_df = pd.DataFrame(po_data, columns=['Q','A'])
po_df.to_csv('positive_QA.csv', index=False)

# 커서와 DB연결 종료
cur.close()
conn.close()
