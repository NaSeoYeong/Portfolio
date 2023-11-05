import pandas as pd
import matplotlib.pyplot as plt
import platform
import os

PATH = os.path.dirname(__file__)

class Real_estate:
    
    def __init__(self, filename):
        self.filename = filename
        self.type = filename.split('_')[0].split('/')[-1]
        self.how = filename.split('_')[1]
        self.loc = filename.split('_')[-2]
        self.year = filename.split('_')[-1].split('.')[0]

        self.loc_list = ["중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군"]
        
    
    # 데이터 전처리 함수 : 매매(최성진) ------------------------------------------------------------------------


    def rent(self):
        file = self.filename
        data = pd.read_excel(file, header=16)

        data["계약년월"] = pd.to_datetime(data["계약년월"], format="%Y%m")
        monthly = data[data["전월세구분"] == "월세"]

        # 월세 : month_df 에 컬럼 추가 후 시군구 컬럼에서 동구만 추출
        month_df = monthly[["시군구", "전용면적(㎡)", "계약년월", "전월세구분", "월세(만원)", "건축년도"]]
        month_df["시군구"] = month_df["시군구"].apply(lambda v: v.split()[1])
        month_df = month_df[month_df["시군구"] != "군위군"]
        month_df = month_df.drop(columns="전월세구분", axis=1)

        # 전세 : annually_df 에 컬럼 추가 후 시군구 컬럼에서 동구만 추출
        annually = data[data["전월세구분"] == "전세"]
        annually_df = annually[["시군구", "전용면적(㎡)", "계약년월", "전월세구분", "보증금(만원)", "건축년도"]]
        annually_df["시군구"] = annually["시군구"].apply(lambda v: v.split()[1])
        annually_df["보증금(만원)"] = annually_df["보증금(만원)"].apply(
            lambda x: int(x.replace(",", ""))
        )
        annually_df = annually_df[annually_df["시군구"] != "군위군"]
        annually_df = annually_df.drop(columns="전월세구분", axis=1)

        return month_df, annually_df


    # 데이터 전처리 함수 : 전월세(최성진) ------------------------------------------------------------------------


    def trading(self):
        file = self.filename
        data = pd.read_excel(file, header=16)

        data["계약년월"] = pd.to_datetime(data["계약년월"], format="%Y%m")

        # 매매 :
        trading_df = data[["시군구", "전용면적(㎡)", "계약년월", "거래금액(만원)", "건축년도"]]
        trading_df["시군구"] = data["시군구"].apply(lambda v: v.split()[1])
        trading_df["거래금액(만원)"] = trading_df["거래금액(만원)"].apply(
            lambda x: int(x.replace(",", ""))
        )
        trading_df = trading_df[trading_df["시군구"] != "군위군"]

        return trading_df


    # 시군구/건축년도에 따른 데이터프레임 마스크 기능 구현 (나서영) ---------------------------------------------------------------

    @staticmethod
    def mask_gu_time(data, time, loc=None):
        if loc != None:
            data = data[data["시군구"] == loc]
        
        else:
            data = data

        if time == "순살":
            data = data[data["건축년도"].isin([2020, 2021, 2022, 2023])]

        elif time == "비순살":
            data = data[~data["건축년도"].isin([2020, 2021, 2022, 2023])]

        elif time == "모두":
            data = data

        return data


    # 데이터프레임에서 5,6,7월 데이터 추출, 딕셔너리 반환 함수 (나서영) ------------------------------------------------------------

    @staticmethod
    def quarter_contract_month_cnt(data):
        month_dic = {}

        may = data[data["계약년월"].dt.month == 5]
        month_dic["5월"] = may.shape[0]

        june = data[data["계약년월"].dt.month == 6]
        month_dic["6월"] = june.shape[0]

        july = data[data["계약년월"].dt.month == 7]
        month_dic["7월"] = july.shape[0]

        return month_dic



    # 2022년/2023년 5~7월 순살/비순살 지역별 그래프 시각화 함수 (나서영) ----------------------------------------------------------------------------


    def make_plot(self, label, data_dic1, data_dic2):
        global PATH

        # 글꼴 설정
        if platform.system() == "Windows":
            plt.rc("font", family="Malgun Gothic")
        else:
            plt.rc("font", family="AppleGothic")

        # 그래프 시각화
        s1 = pd.Series(data_dic1)
        s2 = pd.Series(data_dic2)
        df = pd.DataFrame({"순살": s1, "비순살": s2})

        category = ["5월", "6월", "7월"]
        fig = plt.figure(figsize=(20, 10), dpi=200)
        ax = fig.add_subplot(1, 1, 1)

        bar_width = 0.4
        ax.bar(
            [x - bar_width / 2 for x in range(len(category))],
            df["순살"],
            width=bar_width,
            label="순살",
            color="lightseagreen",
        )
        ax.bar(
            [x + bar_width / 2 for x in range(len(category))],
            df["비순살"],
            width=bar_width,
            label="비순살",
            color="slateblue",
        )

        ax.set_xticks(range(len(category)))
        ax.set_xticklabels(category)

        plt.title(f"{self.year}년 5~7월 {self.loc} {label}의 순살/비순살 {self.type} {self.how} 거래건수", fontsize=25, pad=15)
        ax.set_xlabel("월", loc="right")
        ax.set_ylabel("거래건수", loc="top")
        ax.legend(prop={"size": 15})

        # 그래프 저장
        file_name = f"{label}.png"
        plt.savefig(PATH + f"/graph/{self.year}/{self.year}_{self.type}{self.how}_plot/{self.year}_{file_name}")



    # 2022년/2023년 5~7월 순살/비순살 전체 지역 그래프 시각화 함수 (나서영) ----------------------------------------------------------------------------


    def make_all_loc_plot(self, data_dic1, data_dic2):
        global PATH

        if platform.system() == 'Windows':
            plt.rc('font', family='Malgun Gothic')
        else:
            plt.rc('font', family='AppleGothic')

        s1 = pd.Series(data_dic1)
        s2 = pd.Series(data_dic2)
        df = pd.DataFrame({'순살': s1, '비순살': s2})

        category = ['5월','6월','7월']
        fig = plt.figure(figsize=(20,10), dpi=200)
        ax = fig.add_subplot(1,1,1)
        
        bar_width = 0.4
        ax.bar([x - bar_width/2 for x in range(len(category))], df['순살'], width=bar_width, label='순살', color='lightseagreen')
        ax.bar([x + bar_width/2 for x in range(len(category))], df['비순살'], width=bar_width, label='비순살', color='slateblue')
        
        ax.set_xticks(range(len(category)))
        ax.set_xticklabels(category)

        plt.title(f'{self.year}년 5~7월 {self.loc} 순살/비순살 {self.type} {self.how} 거래건수', fontsize=25, pad=15)
        ax.set_xlabel('월', loc='right')
        ax.set_ylabel('거래건수', loc='top')
        ax.legend(prop={'size': 15})
    
        plt.savefig(PATH + f'/graph/all/{self.loc}_{self.year}.png')


    # 2022년/2023년 5~7월 지역별 비교 그래프 시각화 함수 (나서영) ----------------------------------------------------------------------------

    @staticmethod
    def make_two_plot(obj, label, data_dic1, data_dic2):
        global PATH
        
        if platform.system() == "Windows":
            plt.rc("font", family="Malgun Gothic")
        else:
            plt.rc("font", family="AppleGothic")

        s1 = pd.Series(data_dic1)
        s2 = pd.Series(data_dic2)
        df = pd.DataFrame({"2022년": s1, "2023년": s2})

        category = ["5월", "6월", "7월"]
        fig = plt.figure(figsize=(20, 10), dpi=200)
        ax = fig.add_subplot(1, 1, 1)

        bar_width = 0.4
        ax.bar(
            [x - bar_width / 2 for x in range(len(category))],
            df["2022년"],
            width=bar_width,
            label="2022년",
            color="lightseagreen",
        )
        ax.bar(
            [x + bar_width / 2 for x in range(len(category))],
            df["2023년"],
            width=bar_width,
            label="2023년",
            color="slateblue",
        )

        ax.set_xticks(range(len(category)))
        ax.set_xticklabels(category)

        plt.title(f"2022년/2023년 5~7월 {obj.loc} {label}의 {obj.type} {obj.how} 거래건수", fontsize=25, pad=15)
        ax.set_xlabel("월", loc="right")
        ax.set_ylabel("거래건수", loc="top")
        ax.legend(prop={"size": 15})

        file_name = f"{label}.png"

        plt.savefig(PATH + f"/graph/two/{obj.type}{obj.how}/{file_name}")


class Draw():

    # 년도별-지역별 매매/월세/전세 그래프 추출 함수 (나서영) ----------------------------------------------------------------------------

    def draw_graph(file, how_):
        file_ = Real_estate(file)
        
        # 데이터 로딩           
        if how_ == '매매':
            df = file_.trading()
    
        elif how_ == '월세':
            df = file_.rent()[0]
            
        elif how_ == '전세':
            df = file_.rent()[1]
            
        # 시각화
        for i in file_.loc_list:
            data1 = file_.quarter_contract_month_cnt(file_.mask_gu_time(df, "순살", i))
            data2 = file_.quarter_contract_month_cnt(file_.mask_gu_time(df, "비순살", i))
            file_.make_plot(i, data1, data2)
    
    
    # 년도별-지역별 매매/월세/전세 비교 그래프 추출 함수 (나서영) ----------------------------------------------------------------------------
    # 수정 필요!
    def draw_compare_graph(file1, file2, how_):
        file1_ = Real_estate(file1)
        file2_ = Real_estate(file2)
        
        # 데이터 로딩           
        if how_ == '매매':
            df1 = file1_.trading()
            df2 = file2_.trading()
    
        elif how_ == '월세':
            pass
            df1 = file1_.rent()[0]
            df2 = file2_.rent()[0]
            
        elif how_ == '전세':
            df1 = file1_.rent()[1]
            df2 = file2_.rent()[1]
            
            
        for i in file1_.loc_list:
            data1 = file1_.quarter_contract_month_cnt(file1_.mask_gu_time(df1, '모두', i))
            data2= file2_.quarter_contract_month_cnt(file2_.mask_gu_time(df2, '모두', i))
            file1_.make_two_plot(file1_, i, data1, data2)
        
        
                        
                
    # 년도별 매매/월세/전세 비교 그래프 추출 함수 (나서영) ----------------------------------------------------------------------------
    
    def draw_all_loc_graph(file, how_):
        file_ = Real_estate(file)
        # 데이터 로딩           
        if how_ == '매매':
            df = file_.trading()
    
        elif how_ == '월세':
            df = file_.rent()[0]
            
        elif how_ == '전세':
            df = file_.rent()[1]
            
        # 시각화

        data1 = file_.quarter_contract_month_cnt(file_.mask_gu_time(df, "순살"))
        data2 = file_.quarter_contract_month_cnt(file_.mask_gu_time(df, "비순살"))
        file_.make_all_loc_plot(data1, data2)



if __name__ == "__main__":
    file1 = PATH + '/data/아파트_매매_실거래가_daegu_2022.xlsx'
    file2 = PATH + '/data/아파트_매매_실거래가_daegu_2023.xlsx'
    Draw.draw_compare_graph(file1, file2, '매매')