#!/usr/bin/python3
import cv2
import numpy as np

linebold = False
drawing = False
px = -1
py = -1
lineColor = (0, 0, 0)
lineWidth = 2

def makeBlankImg(width, height, red, green, blue): # 背景を描画する関数
    imageArray = np.zeros((height, width, 3), np.uint8)
    imageArray[0:height, 0:width] = [blue, green, red]
    return imageArray

def mouse_event(event, x, y, flags, param):
    global background, px, py, drawing, lineColor, lineWidth, linebold 
    if event == cv2.EVENT_MOUSEMOVE: #マウスを動かした時
        if drawing: #フラグが True の場合のみ線分が描かれる
            cv2.line(background, (px, py), (x, y), lineColor, lineWidth)
            px = x #次回の線分描画の始点 x 座標
            py = y #次回の線分描画の始点ｙ座標
    elif event == cv2.EVENT_LBUTTONDOWN: #左ボタンをクリックした時
        lineColor = (0, 0, 0) #線分の色(B,G,R)
        drawing = True
        px = x #次回の線分描画の始点 x 座標
        py = y #次回の線分描画の始点ｙ座標
    elif event == cv2.EVENT_LBUTTONUP: #左ボタンを放した時
        drawing = False #マウスが動いても線分を描画しないように
    elif event == cv2.EVENT_RBUTTONDOWN: # 右ボタンを押して赤い線を引くことができる
        drawing = True
        lineColor = (0, 0, 255)
        px = x
        py = y
        print("red")
    elif event == cv2.EVENT_RBUTTONUP:
        drawing = False
    elif event == cv2.EVENT_LBUTTONDBLCLK: # 左ダブルクリックするたびに太さを変える
        if linebold:
            print(linebold)
            lineWidth = 2
            linebold = False
        else: 
            print(linebold)
            lineWidth = 20
            linebold = True
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        background = makeBlankImg(800, 600, 255, 255, 255) # 右ダブルクリックで初期化

background = makeBlankImg(800, 600, 255, 255, 255) # 背景を初期化
cv2.namedWindow("event")
cv2.setMouseCallback("event", mouse_event)
while (True):
    cv2.imshow("event", background)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break 
cv2.destroyAllWindows()