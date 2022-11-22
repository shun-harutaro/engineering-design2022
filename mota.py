#!/usr/bin/python3
#import cv2
#import numpy as np
from gpiozero import Robot #ツインモータ搭載ロボット制御のため
from time import sleep #sleep()関数のため
robot = Robot(left=(17, 18), right=(19, 20)) #GPIO17～20 を用いる 変更可
duty_r = 0.5 #右旋回の角度設定（０～１）
duty_l = 0.75 #左旋回の角度設定（０～１）
duty_f = 0.75 #後退の速度設定（０～１）
robot.forward() #前進
sleep(3) #３秒待つ
robot.forward(speed=1, curve_right=duty_r) #前進しながら右旋回
sleep(3)
robot.left(speed=duty_l) #その場で左回転
sleep(3)
robot.backward(speed=duty_f) #後退
sleep(3)
robot.stop() #停止
