#!/usr/bin/python3
import cv2
import numpy as np
def saltpepper(img):
    r = np.random.rand(480, 640) # カメラの画像と解像度をそろえる
    # 乱数配列の各要素と比較してノイズの色を変える
    img[(r<0.01)] = [255, 255, 255] # 白
    img[(r<0.005)] = [0, 255, 0] # 緑
#フォーマット・解像度・FPS の設定
cap = cv2.VideoCapture(0) # インスタンス
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("Y", "U","Y", "V"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 横および縦の解像度
cap.set(cv2.CAP_PROP_FPS, 30) # フレームレート
while (True):
    ret, img = cap.read() #カメラ画像取得
    img_noise = img.copy() # 参照渡しになるため値をコピー
    saltpepper(img_noise, count)
    img_med = cv2.medianBlur(img_noise, 3)
    img_merge = np.hstack((img, img_noise, img_med)) #画像配列を横に結合
    if not ret:
        continue
    cv2.imshow("capture", img_merge) #画像 img を表示する 処理速度は落ちる
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break #「q」キーが入力されたら while ループを抜ける
cv2.imwrite("captureImage.jpg",img) #画像 img を JPEG ファイルとして保存する
cv2.destroyAllWindows() #ウィンドウを閉じる
