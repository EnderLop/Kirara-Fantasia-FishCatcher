#拾色器
# -*- coding: utf-8 -*-
#@author:EnderLop


import win32api
import numpy as np
from PIL import ImageGrab
from time import sleep


'''截屏色彩分析函数'''
def detectFlash():
    pic = ImageGrab.grab()##截屏
    info = np.asarray(pic,'int')##图像数字化
    info = info.swapaxes(0,1)##Shape转置
    return info

'''检验函数'''
def result(info):
    print(MOUSE_POSITION,info[MOUSE_POSITION],"\n")


MOUSE_POSITION = (1,1)
while MOUSE_POSITION != (0,0):
    MOUSE_POSITION = win32api.GetCursorPos()
    result(detectFlash())
    sleep(1)
input("\a检验结束\n输入任意字符以退出：\n")