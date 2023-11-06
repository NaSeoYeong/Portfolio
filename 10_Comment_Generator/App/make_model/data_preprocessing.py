import mariadb as mdb
import re

from konlpy.tag import Okt

# DB 연결 정보
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
    cur.execute("USE shrimp;")
    cur.execute("SELECT DISTINCT * FROM review")

    data = cur.fetchall()

    # 커서와 DB연결 종료
    cur.close()
    conn.close()

except mdb.Error as e:
    print(f'Error: {e}')


# (1) 데이터 정제
# 개행문자를 .으로 변경
r = [r.replace('\n', ' ') for _, r in data]

# 데이터 말뭉치화
text = ''
for i in r:
    text += i

# 해당 문자에 대하여 말뭉치에 개행문자 추가
characters_to_replace = ['.', '!', '?', 'ㅠㅠ','ㅜㅜ','ㅎㅎ',
                         '함 ', '음 ', '요 ', '당 ', '용 ', '욥 ']

for char in characters_to_replace:
    text = text.replace(char, char+'\n')

# 개행문자 기준으로 파싱, 길이 20~100인 데이터만 남김, 앞뒤 공백 제거
result = text.split('\n')
result = [i for i in result if len(i) > 20 and len(i) < 100]


# 정규 표현식에 맞지 않는 문자를 공백으로 대체하여 나머지를 제거
cleaned_text = []

for text in result:
    pattern = re.compile('[^ㄱ-ㅎ가-힣0-9a-zA-Z. ]')
    cleaned_text.append(re.sub(pattern, '', text))

# 데이터 정규화
okt = Okt()
cleaned_text = [okt.normalize(i).strip() for i in cleaned_text]

# 데이터 파일로 저장
with open('review.txt', 'wt', encoding='utf-8') as t:
    for text in cleaned_text:
        t.write(text)
        t.write('\n')