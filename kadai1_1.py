#!/usr/bin/python3
import cv2

img = cv2.imread("./apple.jpg")
# 状態管理変数stateで切り替える
state = True

# マウスクリックによって img と state を切り替える
def mouse_event(event, x, y, flags, param):
    global img, state
    if event == cv2.EVENT_LBUTTONDOWN:
        if state:
            img = cv2.imread("./baboon.jpg")
            state = False
        else:
            img = cv2.imread("./apple.jpg")
            state = True
    else:
        pass

cv2.namedWindow("event") # イベントウインドウの生成
cv2.setMouseCallback("event", mouse_event) # イベントウインドウはmouse_event関数を呼ぶ
while (True):
    cv2.imshow("event", img) # イベントウインドウにimg を描画
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break 
cv2.destroyAllWindows()