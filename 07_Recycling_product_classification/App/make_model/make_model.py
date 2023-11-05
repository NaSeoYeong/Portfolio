import pandas as pd
import cv2
import joblib
import os

from sklearn.model_selection import train_test_split
from pycaret.classification import *

PATH = os.path.dirname(__file__)

# (1) 통합 데이터셋 구축 --------------------------------------------------


def make_data(num="all", save=True):
    global PATH

    if num > 4488:
        print("4488개 까지 생성 가능")

    else:
        # 제품군별 데이터 로딩
        bottle_df1 = pd.read_csv(PATH + "\\data\\bottle_1.csv")
        bottle_df2 = pd.read_csv(PATH + "\\data\\bottle_2.csv")
        bottle_df3 = pd.read_csv(PATH + "\\data\\bottle_3.csv")

        can_df = pd.read_csv(PATH + "\\data\\can.csv")
        styrofoam_df = pd.read_csv(PATH + "\\data\\styrofoam.csv")
        glass_df = pd.read_csv(PATH + "\\data\\glass.csv")
        paper_df = pd.read_csv(PATH + "\\data\\paper.csv")

        # 다운샘플링 적용하지 않은 전체 데이터셋 생성
        if num == "all":
            add_df = pd.concat(
                [
                    bottle_df1,
                    bottle_df2,
                    bottle_df3,
                    can_df,
                    styrofoam_df,
                    glass_df,
                    paper_df,
                ],
                axis=0,
            )

        # 다운샘플링 적용한 데이터셋 생성
        else:
            add_df = pd.concat(
                [
                    bottle_df1,
                    bottle_df2,
                    bottle_df3,
                    can_df[:num],
                    styrofoam_df[:num],
                    glass_df[:num],
                    paper_df[:num],
                ],
                axis=0,
            )

        # 데이터 형식 통일
        add_df = add_df.astype("uint8")
        add_df.replace("bottle", "plastic")
        add_df.drop("Unnamed: 0", axis=1, inplace=True)
        add_df.reset_index(drop=True, inplace=True)

        # 데이터 라벨 int로 변경
        add_df = add_df.replace("plastic", 1)
        add_df = add_df.replace("can", 2)
        add_df = add_df.replace("styrofoam", 3)
        add_df = add_df.replace("glass", 4)
        add_df = add_df.replace("paper", 5)

        # 가공한 데이터셋 저장
        if save == True:
            if num == "all":
                add_df.to_csv(PATH + "\\data\\final\\all_data.csv")
            else:
                add_df.to_csv(PATH + f"\\data\\final\\data_{num}.csv")

            print("데이터 저장 완료")

        return add_df


# (2) 모델 구현 함수 ------------------------------------------------------------


def make_model(df, save=True):
    # 훈련, 테스트 데이터 분리
    train, test = train_test_split(df, test_size=0.2, stratify=df["label"])

    # 모델 구현
    c = ClassificationExperiment()
    c.setup(train, target="label", train_size=0.8, fold=5)

    model = c.create_model("rf")
    tuned_model = c.tune_model(model, fold=10)
    final_model = c.finalize_model(tuned_model)

    # 모델 성능확인
    print(c.predict_model(final_model, data=train))
    print(c.predict_model(final_model, data=test))

    if save == True:
        # 모델 저장
        model_dir = "./"
        model_file = model_dir + "model.pkl"
        joblib.dump(final_model, model_file)

        print("모델 생성 완료")

    return


# (3) 모델 성능 평가 함수 구현 ------------------------------------------------------------
def check_model(img_path, model):
    # 모델 성능 확인
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (150, 150))
    img = img.reshape(-1, 1)

    img_df = pd.DataFrame(img).T
    print(model.predict(img_df))


if __name__ == "__main__":
    df = make_data()
    model = make_model(df, save=True)

    img = PATH + "make_model\\test\\test.jpg"
    check_model(img, model)
