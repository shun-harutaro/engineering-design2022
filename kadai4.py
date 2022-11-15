#!/usr/bin/python3
import cv2
import numpy as np

COLOR = {
    "yello": (0, 255, 255),
    "white": (255, 255, 255),
    }

def color_pick(img, y, x):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = img_hsv[y, x, 0] #色相(0~179)
    s = img_hsv[y, x, 1] #彩度(0~255)
    v = img_hsv[y, x, 2] #明度(0~255)
    return h, s, v

def color_mask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = img_hsv[:, :, 0] #色相(0~179)
    s = img_hsv[:, :, 1] #彩度(0~255)
    v = img_hsv[:, :, 2] #明度(0~255)
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h>90) & (h<120)) & (s>128)] = 255
    return mask

def get_contour(mask): # 領域の輪郭を抽出
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
        )
    return contours

def get_max_contour(contours): # 最大領域の抽出
    max_contour = contours[0]
    max_area = 0.0
    for contour in contours:
        area = cv2.contourArea(contour)
        if (area > max_area):
            max_area = area
            max_contour = contour
    return max_contour

def get_line_coordinates(max_contour,img): # 直線の座標を取得
    vx, vy, x0, y0 = cv2.fitLine(
        max_contour,
        cv2.DIST_L2,
        0,
        0.01,
        0.01
        )
    if vx < 0.1: #ゼロ除算の防止
        pass
    slope = vy / vx
    x1 = 0 # 画像の左端
    x2 = 640 # 画像の右端
    y1 = int(slope * (x1 - x0) + y0)
    y2 = int(slope * (x2 - x0) + y0)
    start = (x1, y1)
    end = (x2, y2)
    return start, end

def apply_contour(img):# 輪郭を表示させる
    line_width = 2
    mask = color_mask(img)
    contours = get_contour(mask)
    cv2.drawContours(img, contours, -1, COLOR["yello"], line_width)
    if contours:
        max_contour = get_max_contour(contours)
        start, end = get_line_coordinates(max_contour, img)
        cv2.line(img, start, end, COLOR["white"], line_width)

def mouse_event(event, x, y, flags, param):
    # マウスクリックでhsvの色情報を表示
    if event == cv2.EVENT_LBUTTONDOWN:
        h, s, v = color_pick(img_merge, y, x)
        print('({}, {}, {})'.format(h, s, v))

#フォーマット・解像度・FPS の設定
cap = cv2.VideoCapture(0) # インスタンス
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("Y", "U","Y", "V"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 横および縦の解像度
cap.set(cv2.CAP_PROP_FPS, 30) # フレームレート

cv2.namedWindow("capture")
cv2.setMouseCallback("capture", mouse_event)
while (True):
    ret, img = cap.read() #カメラ画像取得
    contour_img = img.copy()
    apply_contour(contour_img)
    img_merge = np.hstack((img, contour_img)) #画像配列を横に結合
    if not ret:
        continue
    cv2.imshow("capture", img_merge) #画像 img を表示する 処理速度は落ちる
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break #「q」キーが入力されたら while ループを抜ける
cv2.imwrite("captureImage.jpg",img) #画像 img を JPEG ファイルとして保存する
cv2.destroyAllWindows() #ウィンドウを閉じる