import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

from konlpy.tag import Okt
from wordcloud import WordCloud
from collections import Counter

import matplotlib.pyplot as plt
import PIL

import requests
import platform
import time
import re

# (1) 크롤링을 위한 클래스 ------------------------------------------------------------

class Crawl:

    # 데이터 크롤링, 기사 마지막 n일 전 부분 삭제
    def get_content(start_num, end_num, key_word):

        news_list = []
        
        while start_num < end_num:

            url = 'https://www.google.com/search?q={}&start={}&lr=lang_ko&tbs=lr:lang_1ko&tbm=nws'.format(key_word, start_num)
            html = requests.get(url)

            time.sleep(1)

            soup = BeautifulSoup(html.text, 'html.parser')
            titles = soup.select('div.BNeawe.vvjwJb.AP7Wnd')
            contents = soup.select('div.BNeawe.s3v9rd.AP7Wnd')[::2]

            for i in range(len(titles)):
                content = contents[i].text
                mask = re.search('(\d{1,2})(시간|일|주|개월|년) (전)', content).group()
                content = content.replace(mask,'')
                news_list.append((titles[i].text, content))

            start_num += 10

        return news_list
    
     # 리스트를 데이터프레임 형식으로 변환
    def make_frame(data_list):
        return pd.DataFrame(data_list, columns=['기사제목','기사내용'])



# (2) 자연어 처리와 워드클라우드 생성을 위한 클래스 ------------------------------------------------------------

class MakeData:

    # 말뭉치 제작
    def make_text(data_frame):
        
        title = data_frame['기사제목'].to_list()
        content = data_frame['기사내용'].to_list()
 
        texts = ''
        
        for i in range(len(title)):
            texts = texts + title[i] + content[i]
        
        return texts
    
    # 형태소별 파싱 및 태그 부착한 딕셔너리 제작
    def text_parse(text):
        
        okt = Okt()
    
        data_tag = okt.pos(text, norm=True, stem=True)

        use_data_list = []

        # 특정 품사만 추출, 잘못 추출된 용어 삭제
        for word, tag in data_tag:
            if tag in ['Noun', 'Alpha', 'Adverb']: #'Adjective', 'Verb'
                if word not in ['의','를','등','것','수']: 
                    use_data_list.append(word)

        # 태그별 빈도 딕셔너리 생성
        counts = Counter(use_data_list)

        # 잘못 추출된 상위어 전처리
        cnt_big1 = counts['초']
        cnt_big2 = counts['거대']
        big_result = cnt_big1 if cnt_big1 >= cnt_big2 else cnt_big2
        counts['초거대'] = big_result

        cnt_make1 = counts['생']
        cnt_make2 = counts['성형']
        make_result = cnt_make1 if cnt_make1 >= cnt_make2 else cnt_make2
        counts['생성형'] = make_result

        counts.pop('초')
        counts.pop('거대')
        counts.pop('생')
        counts.pop('성형')

        return counts


    # 워드클라우드 제작
    def make_wordcloud(dic, mask_file):

        # 폰트 지정
        if platform.system() == 'Windows':
            path = r'c:\Windows\Fonts\HMFMMUEX.ttc'
        elif platform.system() == 'Darwin': # Mac OS
            path = r'/System/Library/Fonts/AppleGothic'
        else:
            path = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

        # 빈도순 상위어 추출
        big_text = dic.most_common(300)

        # 이미지 마스크 지정
        icon = PIL.Image.open(mask_file)
        img = PIL.Image.new('RGB', icon.size, (255,255,255))
        img.paste(icon, icon)
        img = np.array(img)

        wc = WordCloud(font_path=path, background_color="white", mask=img, min_font_size=15, max_font_size=300, colormap='cool') #
        img_wordcloud = wc.generate_from_frequencies(dict(big_text))

        plt.figure(figsize=(100, 80))
        plt.axis('off')
        plt.imshow(img_wordcloud)
        plt.show()
        
    # 빈도순 상위어 파이그래프     
    def draw_top_pi(dic, title):
        # 상위 노출어 5개 추출한 리스트 반환
        result = dic.most_common(5)

        # 단어 / 빈도 리스트로 각각 분리
        keys = []
        values = []

        for k,v in result:
            keys.append(k)
            values.append(v)

        # 전체 데이터(상위5개 수치 제외) 추가
        keys.append('all')
        all_val = len(dic) - sum(values)
        values.append(all_val)

        # 파이그래프 제작
        plt.title(title, size = 15)
        plt.pie(values, labels=keys, autopct='%1.1f', colors=plt.cm.Set3.colors, wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5})
        plt.show()
        
    # 연관어 파이그래프    
    def draw_connect_pi(dic, title, key_list, val_list):
        
        keys = key_list
        values = val_list
        
        # 전체 데이터(상위5개 수치 제외) 추가
        keys.append('all')
        all_val = len(dic) - sum(values)
        values.append(all_val)

        # 파이그래프 제작
        plt.title(title, size = 15)
        plt.pie(values, labels=keys, autopct='%1.1f', colors=plt.cm.Set3.colors, wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5})
        plt.show()
        
        
if __name__ == '__main__':
    
    # 크롤링 후 데이터프레임 생성, csv 저장
    data = Crawl.get_content(0, 100, 'chatgpt')
    print(data)
    df = Crawl.make_frame(data)
    df.to_csv('data_all.csv')
    
    # csv 가져와 형태소 단위로 파싱한 딕셔너리 생성
    df2 = pd.read_csv('./data/chatgpt_googld.csv', encoding='utf-8')
    texts = MakeData.make_text(df2)
    parsed_dict = MakeData.text_parse(texts)
    
    # 딕셔너리 활용하여 워드클라우드 생성
    MakeData.make_wordcloud(parsed_dict, './img/bing.png')
    
    # 딕셔너리 활용하여 상위노출어 파이그래프 생성
    MakeData.draw_top_pi(parsed_dict, 'ChatGPT - 구글/바드 검색 상위 노출어')
    
    # 리스트 직접 입력하여 연관어 파이그래프 생성
    keys = ['구글', '바드', 'Bard', '마이크로소프트', '빙']
    values = [410, 220, 174, 80, 60]
    MakeData.draw_connect_pi(parsed_dict, 'ChatGPT - 구글/바드 연관어', keys, values)