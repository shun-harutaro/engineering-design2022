#!/usr/bin/python3
import cv2
import numpy as np
#フォーマット・解像度・FPS の設定
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("Y", "U","Y", "V"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
while (True):
    ret, img = cap.read() #カメラ画像取得
    if not ret:
        continue
    cv2.imshow("capture",img) #画像 img を表示する 処理速度は落ちる
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break #「q」キーが入力されたら while ループを抜ける

cv2.imwrite("captureImage.jpg",img) #画像 img を JPEG ファイルとして保存する
cv2.destroyAllWindows() #ウィンドウを閉じる