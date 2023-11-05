import pandas as pd
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

PATH = os.path.dirname(__file__)


# 이미지 데이터 이름 일괄 변경 함수
def name_changer(path):
    cnt = 1

    for file in os.listdir(path):
        new_name = "styrofoam_" + str(cnt) + ".jpg"
        old_path = os.path.join(path, file)
        new_path = os.path.join(path, new_name)

        # 파일 이름 변경
        os.rename(old_path, new_path)
        cnt += 1


# 이미지 회전 함수
def rotate_img(img_arr, degree=90):
    img = img_arr.reshape(150, 150, 1)
    center_idx = len(img) // 2 - 1

    matrix = cv2.getRotationMatrix2D((center_idx, center_idx), degree, 1)
    ro_img = cv2.warpAffine(img, matrix, dsize=(0, 0))

    ro_img = ro_img.reshape(-1)

    return ro_img


# 이미지 블러링 함수
def blur_img(img_arr):
    img = img_arr.reshape(150, 150, 1)
    bl_img = cv2.GaussianBlur(img, (3, 3), 5).reshape(-1)

    return bl_img


# 이미지 샤프닝 함수
def sharp_img(img_arr):
    img = img_arr.reshape(150, 150, 1)
    mask = np.asarray([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=np.float32)

    sharp_img = cv2.filter2D(img, -1, mask).reshape(-1)

    return sharp_img


if __name__ == "__main__":
    folder_path = PATH + "data\\imgs"
    img_path = os.listdir(folder_path)

    first_img = []

    for img_name in img_path:
        org = cv2.imread(folder_path + img_name, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(org, (150, 150))
        first_img.append(img.reshape(-1))

    all_imgs = []
    ro_imgs = []

    for img_arr in first_img:
        for i in range(90, 361, 90):
            ro_imgs.append(rotate_img(img, i))

    all_imgs.extend(first_img)
    all_imgs.extend(ro_imgs)

    blur_imgs = []

    for img_arr in all_imgs:
        blur_imgs.append(blur_img(img_arr))

    sharp_imgs = []
    for img_arr in all_imgs:
        sharp_imgs.append(sharp_img(img_arr))

    all_imgs.extend(blur_imgs)
    all_imgs.extend(sharp_imgs)

    result = pd.DataFrame(all_imgs)
    result["label"] = "styrofoam"

    result.to_csv("styrofoam.csv", index=False)
