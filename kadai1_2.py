#!/usr/bin/python3
import cv2
import numpy as np

img = cv2.imread("./apple.jpg")

def makeBlankImg(width, height, red, green, blue): 
    # NumPy のzeros メソッドで0埋め配列を生成
    imageArray = np.zeros((height, width, 3), np.uint8)
    # 引数でとったRGBの値を代入
    imageArray[0:height, 0:width] = [blue, green, red]
    return imageArray

width = 512
height = 512 # サイズは"apple.jpg"と統一
imgR = 0
imgG = 0
imgB = 0
# 黒一色の画像配列を予め用意しておく
background = makeBlankImg(width, height, imgR, imgG, imgB)

def mouse_event(event, x, y, flags, param):
    global background
    if event == cv2.EVENT_LBUTTONDOWN:
        # 画像を切り取る前に一面黒画面にして初期化
        background = makeBlankImg(width, height, imgR, imgG, imgB)
        # 左上からクリックした座標までの部分を同じ座標で切り取った部分で書き換える
        background[0:y,0:x] = img[0:y,0:x]

cv2.namedWindow("event")
cv2.setMouseCallback("event", mouse_event)
while (True):
    cv2.imshow("event", background)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break 
cv2.destroyAllWindows()