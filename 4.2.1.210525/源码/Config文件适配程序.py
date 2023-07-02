# Config文件适配程序
# -*- coding: utf-8 -*-
# @author:EnderLop
import win32gui
from os import getcwd, system
from time import sleep


'''构建写入文本'''
def construction():
    config_text = "Window Name:"
    health_window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(health_window)
    config_text += title
    return config_text


print("下面开始进行程序适配")
sleep(2)
print("\a请在三秒内将模拟器作为活动窗口")
sleep(3)
file_road = getcwd() + "\\Config.txt"
with open(file_road, "w", encoding = "utf-8") as config_file:
    config_file.write(construction())
system("cls")
input("\a配置完成,输入任何字符以结束：\n")
