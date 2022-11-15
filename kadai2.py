#!/usr/bin/python3
from abc import ABCMeta, abstractmethod
import cv2
import numpy as np

COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "black": (0, 0, 0)
}

# 背景を作る関数
def makeBlankImg(width, height, red, green, blue): 
    imageArray = np.zeros((height, width, 3), np.uint8)
    imageArray[0:height, 0:width] = [blue, green, red]
    return imageArray

# ボタン抽象クラス
class Button(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.weight = 2
        self.color = (0, 0, 0)
    def ret_y(self):
        return self.y
    def generate(self, background):
        pass

# 正方形のボタンクラス
class SquareButton(Button):
    def __init__(self, x, y, size):
        super().__init__(x, y)
        self.size = size
    def generate(self, background):
        size = self.size
        x1 = self.x
        x2 = x1 + size
        y1 = self.y
        y2 = y1 + size
        cv2.rectangle(
            background, 
            (x1, y1), 
            (x2, y2), 
            self.color,
            self.weight
        )
    def ret_y(self):
        return self.y + self.size

# SquareButtonを継承し、色に特化したクラス
class ColorButton(SquareButton):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size)
        self.weight = -1
        self.color = COLORS[color]
    def generate(self, background):
        return super().generate(background) 

# 円形のボタンクラス
class TextCircleButton(Button):
    def __init__(self, x, y, r, text):
        super().__init__(x, y)
        self.r = r
        self.text = text
    def generate(self, background):
        r = self.r
        x = self.x + r
        y = self.y + r
        cv2.circle(
            background, 
            (x, y), 
            r, 
            self.color, 
            self.weight
        )
        self.text_display(background)
    def text_display(self, background):
        fontType = cv2.FONT_HERSHEY_SIMPLEX
        fontSize = 1
        fontColor = (0, 0, 0)
        x = self.x + 13
        y = self.y + 33
        cv2.putText(background, 
            self.text,
            (x, y),
            fontType,
            fontSize,
            fontColor
            )
    def ret_y(self):
        return self.y + self.r * 2

# 色・太さを変更するボタンを管理するクラス
class Palette:
    def __init__(self):
        self.body = makeBlankImg(100, 600, 255, 255, 255)
        self.redbtn = ColorButton(30, 50, 50, "red")
        self.blackbtn = ColorButton(30, 110, 50, "black")
        self.greenbtn = ColorButton(30, 170, 50, "green")
        self.bluebtn = ColorButton(30, 230, 50, "blue")
        self.upbtn = TextCircleButton(30, 290, 25, "+")
        self.downbtn = TextCircleButton(30, 350, 25, "-")
    def generate(self):
        self.redbtn.generate(self.body)
        self.blackbtn.generate(self.body)
        self.greenbtn.generate(self.body)
        self.bluebtn.generate(self.body)
        self.upbtn.generate(self.body)
        self.downbtn.generate(self.body)
    def render(self):
        return self.body
    def y_selector(self, y):
        if (y < self.redbtn.ret_y()):
            return "red"
        elif (y < self.blackbtn.ret_y()):
            return "black"
        elif (y < self.greenbtn.ret_y()):
            return "green"
        elif (y < self.bluebtn.ret_y()):
            return "blue"
        elif (y < self.upbtn.ret_y()):
            return "up"
        elif (y < self.downbtn.ret_y()):
            return "down"

# 描画する線を管理するクラス
class Canvas:
    def __init__(self):
        self.background = makeBlankImg(700, 600, 255, 255, 255)
        self.__pxy = (-1, -1)
        self.lineColor = (0, 0, 0) #線分の色
        self.lineWidth = 2 #線分の太さ
    @property
    def pxy(self):
        return self.__pxy
    @pxy.setter
    def pxy(self, value):
        if type(value) is tuple:
            self.__pxy = value
        else:
            raise ValueError("argument is not tuple")
    def render(self):
        return self.background
    def draw(self, x, y):
        cv2.line(
            self.background, 
            self.__pxy,
            (x, y),
            self.lineColor,
            self.lineWidth
            )
        self.__pxy = (x, y) #次回の線分描画の始点座標
    def line_up(self):
        self.lineWidth += 1
    def line_down(self):
        self.lineWidth -= 1
    def clear(self):
        self.background = makeBlankImg(700, 600, 255, 255, 255)

# マウスイベントを管理、集約したクラスのメソッドを実行するクラス
class Paint:
    def __init__(self):
        self.canvas = Canvas()
        self.palette = Palette()
        self.palette.generate()
        self.drawing = False
    def mouse_event(self, event, x, y, flags, param):
        canvas = self.canvas
        if event == cv2.EVENT_MOUSEMOVE: #マウスを動かした時
            if self.drawing: #フラグが True の場合のみ線分が描かれる
                canvas.draw(x, y)
        elif event == cv2.EVENT_LBUTTONDOWN: #左ボタンをクリックした時
            self.drawing = True
            if (730 < x):
                res = self.palette.y_selector(y)
                if res == "up":
                    canvas.line_up()
                elif res == "down":
                    canvas.line_down()
                else:
                    canvas.lineColor = COLORS[res]
            else:
                canvas.pxy = (x, y) #次回の線分描画の始点座標
        elif event == cv2.EVENT_LBUTTONUP: #左ボタンを放した時
            self.drawing = False #マウスが動いても線分を描画しないように
        elif event == cv2.EVENT_LBUTTONDBLCLK: #左ボタンをダブルクリック
            canvas.clear() # クリア
    def render(self):
        canvas = self.canvas.render()
        palette = self.palette.render()
        return np.hstack((canvas, palette))

# main loop
paint = Paint()
cv2.namedWindow("event")
cv2.setMouseCallback("event", paint.mouse_event)
while (True):
    cv2.imshow("event", paint.render())
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break 
cv2.destroyAllWindows()