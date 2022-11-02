#!/usr/bin/python3
import cv2
import numpy as np

drawing = False
px = -1
py = -1

def makeBlankImg(width, height, red, green, blue): 
    imageArray = np.zeros((height, width, 3), np.uint8)
    imageArray[0:height, 0:width] = [blue, green, red]
    return imageArray

class Button:
    state = False
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def generate(self):
        print("adc")
    def get_state(self):
        return self.state
    def toggle_button(self):
        self.state = not self.state
    def ret_y(self):
        return self.y

class SquareButton(Button):
    def __init__(self, x, y, size):
        super().__init__(x, y)
        self.size = size
    def generate(self):
        size = self.size
        x1 = self.x
        x2 = x1 + size
        y1 = self.y
        y2 = y1 + size
        cv2.rectangle(
            background, (x1, y1), (x2, y2), (0, 0, 0), 2)
    def ret_y(self):
        return self.y + self.size


class CircleButton(Button):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r
    def generate(self):
        r = self.r
        x = self.x + r
        y = self.y + r
        cv2.circle(
            background, (x, y), r, (0,0,0), 2)
    def ret_y(self):
        return self.y + self.r * 2

def y_selector(y):
    if (y < redbutton.ret_y()):
        print("red")
    elif (y < blackbutton.ret_y()):
        print("black")
    elif (y < upbutton.ret_y()):
        print("up")
    elif (y < downbutton.ret_y()):
        print("down")

def mouse_event(event, x, y, flags, param):
    global px, py, drawing 
    lineColor = (0, 0, 0) #線分の色(B,G,R)
    lineWidth = 2 #線分の太さ
    if event == cv2.EVENT_MOUSEMOVE: #マウスを動かした時
        if drawing: #フラグが True の場合のみ線分が描かれる
            cv2.line(background, (px, py), (x, y), lineColor, lineWidth)
            px = x #次回の線分描画の始点 x 座標
            py = y #次回の線分描画の始点ｙ座標
    elif event == cv2.EVENT_LBUTTONDOWN: #左ボタンをクリックした時
        drawing = True
        if (750 < x):
            y_selector(y)
        else:
            px = x #次回の線分描画の始点 x 座標
            py = y #次回の線分描画の始点ｙ座標
    elif event == cv2.EVENT_LBUTTONUP: #左ボタンを放した時
        drawing = False #マウスが動いても線分を描画しないように
    

background = makeBlankImg(800, 600, 255, 255, 255)
cv2.namedWindow("event")
cv2.setMouseCallback("event", mouse_event)

redbutton = SquareButton(750, 50, 30)
blackbutton = SquareButton(750, 100, 30)
upbutton = CircleButton(750, 150, 15)
downbutton = CircleButton(750, 200, 15)
redbutton.generate()
blackbutton.generate()
upbutton.generate()
downbutton.generate()

while (True):
    cv2.imshow("event", background)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break 
cv2.destroyAllWindows()