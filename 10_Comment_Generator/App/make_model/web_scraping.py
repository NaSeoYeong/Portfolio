import mariadb as mdb
import requests
import random 
import time
from tqdm import tqdm

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# (1) 올리브영 리뷰 데이터 크롤링 함수 구현 ----------------------------------------------------------

# 상품별 링크 크롤링 함수
def get_url(last_num):
    url_list = []

    for i in tqdm(range(1,last_num+1)):
        olive = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100020001&fltDispCatNo=&prdSort=01&pageIdx={i}&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100020001_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%A9%94%EC%9D%B4%ED%81%AC%EC%97%85&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd='

        url = requests.get(olive)
        html = BeautifulSoup(url.text)

        

        ul = html.find_all('ul', class_='cate_prd_list gtm_cate_list')

        for i in ul:
            b = i.find_all('a')
            for j in b:
                url_list.append(j['href'])
        
        time.sleep(random.random() + 1)
    
    return url_list


# 상품별 댓글 크롤링 함수
def get_review(data):

    driver = webdriver.Chrome('./chromedriver.exe')

    conn_params = {'host':"localhost",
               'port':3306,
               'user':'root',
               'password':'root'}
    
    try:
        # DB에 연결하기
        conn = mdb.connect(**conn_params)

        # DB에 접근할 커서 객체 생성
        cur = conn.cursor()

        # 사용할 DB 선택
        cur.execute("USE shrimp;")

        # 데이터 크롤링

        for idx, link in tqdm(data):
            driver.get(link)
            driver.implicitly_wait(10)
            time.sleep(0.5)

            # 후기열 클릭
            driver.find_element(By.ID, "reviewInfo").click()

            # num = 0
            nav = driver.find_element(By.CLASS_NAME, "pageing").find_elements(By.CSS_SELECTOR, '*')
            
            for i in range(10):
                nav[i].click()
                nav = driver.find_element(By.CLASS_NAME, "pageing").find_elements(By.CSS_SELECTOR, '*')
            
                time.sleep(random.random()+1)

                # num += 1

                text = driver.find_elements(By.CLASS_NAME, "txt_inner")

                for j in text:
                    review = j.text
                    
                    # 데이터 입력
                    cur.execute("INSERT INTO review(idx, review) VALUES (?, ?)", [idx, review])
        

            # 데이터 커밋
            conn.commit()

        # 커서와 DB연결 종료
        cur.close()
        conn.close()

    except mdb.Error as e:
            print(f'Error: {e}')


# (2) 실제 데이터 크롤링 후 DB와 연동 ----------------------------------------------------------

# (2-1) 저장할 링크 데이터 크롤링하기 ----------------------------------------------------------
url_list = []
url_list.append(get_url(12))

# 연결 정보 설정
conn_params = {'host':"localhost",
               'port':3306,
               'user':'root',
               'password':'root'}

try:
    # DB에 연결하기
    conn = mdb.connect(**conn_params)

    # DB에 접근할 커서 객체 생성
    cur = conn.cursor()

    # (2) DB에 데이터 입력
    for url in url_list[::2]:
        if url != None:
            cur.execute("USE shrimp;")
            cur.execute("INSERT INTO urls(link) VALUES (?)", [url])

    # 데이터 커밋하기
    conn.commit()

    # 커서와 DB연결 종료
    cur.close()
    conn.close()

except mdb.Error as e:
    print(f'Error: {e}')


# (2-2) DB에서 링크 가져와 리뷰 크롤링한 후 DB에 저장 ----------------------------------------------------------

try:
    # DB에 연결하기
    conn = mdb.connect(**conn_params)

    # DB에 접근할 커서 객체 생성
    cur = conn.cursor()

    # 데이터 가져오기
    cur.execute("USE shrimp;")
    cur.execute("SELECT * FROM urls")

    url = cur.fetchall()

    # 커서와 DB연결 종료
    cur.close()
    conn.close()

except mdb.Error as e:
    print(f'Error: {e}')

# 리뷰 데이터 크롤링 후 DB에 저장
get_review(url)