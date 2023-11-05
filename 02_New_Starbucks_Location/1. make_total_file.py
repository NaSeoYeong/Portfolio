import pandas as pd
import geopy.distance

star_21_data = pd.read_csv('./susung_21.csv')
star_22_data = pd.read_csv('./susung_22.csv')
star_22_21_data = pd.read_csv('./Daegu_22.csv')
bus_data = pd.read_csv('./final_bus.csv')
sub_data = pd.read_csv('./final_subway.csv')
shop_21_data = pd.read_csv('./final_shop_21.csv')
shop_23_data = pd.read_csv('./final_shop_23.csv')
school_data = pd.read_csv('./school.csv', encoding='cp949')


# ---------------------------------------
# 스타벅스 주위 요소 개수 추출 함수

def count(data, directory, num, column):
    cnt_list = []
    person_move_list = []

    for i in range(len(data)):

        cnt = 0
        person_move_cnt = 0    
        star_idx = (data['위도'][i], data['경도'][i])

        for j in range(len(directory)):

            idx = (directory['위도'][j], directory['경도'][j])
            idx_distance = geopy.distance.distance(idx, star_idx)

            if idx_distance <= float(num):
                cnt += 1
                if '하루평균유동인구' in directory.columns:
                    person_move_cnt += directory['하루평균유동인구'][j]
        
        cnt_list.append(cnt)
        person_move_list.append(person_move_cnt)

    df = pd.DataFrame([data['매장명'][i], cnt_list[i], person_move_list[i]] for i in range(len(cnt_list)))
    df.columns = ['매장명', f'인접_{column}수', f'하루평균유동인구_{column}']
    
    
    return df

if __name__ == '__main__':

    # 데이터 통합을 위한 코드
    sr_sub = count(star_22_21_data, sub_data, 0.5, '지하철')
    sr_bus = count(star_22_21_data, bus_data, 0.3, '버스')
    sr_shop = count(star_22_21_data, shop_21_data, 0.3, '상가')
    sr_school = count(star_22_21_data, school_data, 1.0, '학교')
    sr_trans = sr_bus['하루평균유동인구_버스'] + sr_sub['하루평균유동인구_지하철']

    result = pd.concat([star_22_21_data, sr_shop, sr_school, sr_sub, sr_bus, sr_trans], axis=1)

    result.to_csv('analyze_Daegu_22_21.csv')

    # # 컬럼 이름 변경을 위한 코드
    # df = pd.read_csv('./analyze_Daegu_22_21.csv')
    # df.drop([df.columns[0], '매장명.1', '매장명.2', '매장명.3', '매장명.4', '하루평균유동인구_상가','하루평균유동인구_학교'], axis=1, inplace=True)
    # df.columns = ['매장명', '위도', '경도', '인접_상가수', '인접_학교수', '인접_지하철역수', '하루평균유동인구_지하철', '인접_버스정류장수', '하루평균유동인구_버스', '하루평균유동인구_대중교통']

    # df.to_csv('analyze_Daegu_22_21.csv')