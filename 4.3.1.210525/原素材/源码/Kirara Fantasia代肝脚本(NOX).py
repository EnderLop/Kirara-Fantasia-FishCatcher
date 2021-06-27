#Kirara Fantasia代肝脚本(NOX)Ver.4.3.1.210525
# -*- coding: utf-8 -*-
#@author:EnderLop
import time,win32ui,win32gui,win32api,win32con
import numpy as np
from os import getcwd
from PIL import Image


#全局变量声明
TOTAL_ROUND = 0
WINDOW_ID,MAINWINDOW_ID = 0,0
WIDTH,HEIGHT = 16000,9000


"""游戏预先处理单元"""
'''配置文件读入及应用'''
def config_reader():
    global WINDOW_ID
    file_road = getcwd() + "\\Config.txt"
    with open(file_road,"r",encoding = "utf-8") as config_file:
        window_name = config_file.readline().split(":")[-1]
        WINDOW_ID = win32gui.FindWindow(None,window_name)

'''模拟器子句柄枚举'''
def get_child_windows():
    global WINDOW_ID,MAINWINDOW_ID
    if not WINDOW_ID:
        return None
    child_list = []
    win32gui.EnumChildWindows(WINDOW_ID,lambda hwnd,param:param.append(hwnd),child_list)
    for _suspect_target in child_list:
        if win32gui.GetWindowText(_suspect_target) == "ScreenBoardClassWindow":
            MAINWINDOW_ID = _suspect_target
            break
    else:
        print("未找到游戏句柄")

'''游戏主窗口句柄应用'''
def state_change():
    global WIDTH,HEIGHT,MAINWINDOW_ID
    _four_state = win32gui.GetWindowRect(MAINWINDOW_ID)
    WIDTH,HEIGHT = _four_state[2] - _four_state[0],_four_state[3] - _four_state[1]

'''1080P→窗口化绝对位置调整'''
def state_transform(x_origin,y_origin):
    global WIDTH,HEIGHT
    x_new = x_origin / 1920 * WIDTH#X轴绝对位置变换
    y_new = y_origin / 1080 * HEIGHT#Y轴绝对位置变换
    return int(x_new),int(y_new)


"""游戏信息获取单元"""
'''截取当前屏幕色块信息'''
def detect_flash():
    global WIDTH,HEIGHT,MAINWINDOW_ID
    hWndDC = win32gui.GetWindowDC(MAINWINDOW_ID)
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC,WIDTH,HEIGHT)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0,0),(WIDTH,HEIGHT),mfcDC,(0,0),win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    image = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
    color_info = np.asarray(image,'int')#图像数字化
    color_info = color_info.swapaxes(0,1)#Shape转置
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(MAINWINDOW_ID,hWndDC)
    return color_info

'''判断当前位置颜色是否含有特殊信息'''
def color_compare(info,state_x,state_y,R,G,B):
    if info[state_transform(state_x,state_y)].tolist() == [R,G,B]:
        return True
    else:
        return False

'''鼠标操作'''
def mouse_click(state_x,state_y,n):
    global MAINWINDOW_ID
    tmp = win32api.MAKELONG(state_x,state_y)
    for i in range(n):
        win32gui.SendMessage(MAINWINDOW_ID,win32con.WM_ACTIVATE,win32con.WA_ACTIVE,0)
        time.sleep(0.1)
        win32api.PostMessage(MAINWINDOW_ID,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,tmp)
        time.sleep(0.1)
        win32api.PostMessage(MAINWINDOW_ID,win32con.WM_LBUTTONUP,0000,tmp)

'''判断珍藏技是否准备就绪'''
def star_shine(info):
    if color_compare(info,655,965,7,227,209) and color_compare(info,655,920,250,250,235):#检查珍藏第一颗星星为亮蓝 且 周遭界面亮
        return True
    elif color_compare(info,655,965,119,92,92) and color_compare(info,655,920,125,125,117):#检查珍藏第一颗星星为深粉 且 周遭界面暗
        return False

'''判断当前是否为AUTO模式'''
def auto_shine(info):
    if color_compare(info,1825,30,255,255,255) and color_compare(info,1820,55,255,255,255):#检查AUTO箭头头部为纯白
        return True
    elif color_compare(info,1825,30,110,65,53) and color_compare(info,1850,40,255,253,228):#检查AUTO箭头头部为深棕 且 周遭界面白
        return False

'''判断当前是否已完成对战'''
def finish_shine(info):
    if color_compare(info,1080,225,255,154,185) and color_compare(info,1450,655,255,255,255):#检查表头为亮粉 且 两按钮间为纯白
        return True
    else:
        return False


"""战斗阶段响应单元"""
'''在珍藏技准备就绪的情况下释放芳文跳'''
def fangwen_jump(info):
    if star_shine(info):
        if auto_shine(info):#关闭AUTO
            for round in range(5):
                if auto_shine(detect_flash()):
                    mouse_click(state_transform(1825,30)[0],state_transform(1825,30)[1],1)
                    time.sleep(0.25)
                elif not auto_shine(detect_flash()) and not (auto_shine(detect_flash()) is None):
                        break
            else:
                return None
        mouse_click(state_transform(655,965)[0],state_transform(655,965)[1],1)
        time.sleep(0.5)
    elif color_compare(detect_flash(),1350,920,3,113,104):
        mouse_click(state_transform(1690,190)[0],state_transform(1690,190)[1],1)
        time.sleep(0.5)
        mouse_click(state_transform(1565,965)[0],state_transform(1565,965)[1],1)
        time.sleep(0.5)
        for i in range(7):
            mouse_click(state_transform(960,540)[0],state_transform(960,540)[1],1)
            time.sleep(1)
        print("{}：完成一次芳文跳释放".format(time.strftime("%Y/%m/%d %H:%M:%S")))

'''在珍藏技未就绪的情况下开启AUTO模式'''
def feel_fish(info):
    if not star_shine(info) and not auto_shine(info) and not (star_shine(info) is None) and not (auto_shine(info) is None):
        for round in range(5):
            if not auto_shine(detect_flash()) and not (auto_shine(detect_flash()) is None):
                mouse_click(state_transform(1825,30)[0],state_transform(1825,30)[1],1)
                time.sleep(0.5)
                break
        else:
            return None

'''在对战结束后点击跳过结算界面'''
def finally_finsih(info):
    if finish_shine(info):
        time.sleep(1)
        for round in range(5):
            mouse_click(state_transform(960,800)[0],state_transform(960,800)[1],1)
            time.sleep(1)
            if color_compare(detect_flash(),630,280,255,154,185) and color_compare(detect_flash(),630,130,127,77,92):
                time.sleep(1)
                mouse_click(state_transform(960,680)[0],state_transform(960,680)[1],1)
        print("{}：完成一场大对战刷轮".format(time.strftime("%Y/%m/%d %H:%M:%S")))

'''在对战结束且仍有剩余体力的情况下自动再开一把对战'''
def restart_game(info):
    global TOTAL_ROUND
    if color_compare(info,580,85,255,154,185) and color_compare(info,695,885,200,152,110):
        mouse_click(state_transform(630,990)[0],state_transform(630,990)[1],1)
        time.sleep(3)
        TOTAL_ROUND += 1
        print("{0}：已完成{1}场战斗,正在开始第{2}场战斗".format(time.strftime("%Y/%m/%d %H:%M:%S"),TOTAL_ROUND,TOTAL_ROUND+1))

'''主函数'''
def main():
    fangwen_jump(detect_flash())
    feel_fish(detect_flash())
    finally_finsih(detect_flash())
    restart_game(detect_flash())


'''运行函数'''
config_reader()
get_child_windows()
mouse_position = (1,1)
print("脚本启动中...")
time.sleep(5)
print("\a{}：代肝工作开始".format(time.strftime("%Y/%m/%d %H:%M:%S")))
timeStart = time.perf_counter()
while mouse_position != (0,0):
    mouse_position = win32api.GetCursorPos()
    state_change()
    main()
dur = time.perf_counter() - timeStart
print("\a{}：代肝工作结束".format(time.strftime("%Y/%m/%d %H:%M:%S")))
print("共完成{3}场对战的刷轮，总耗时为:{2:.0f}h {1:.0f}min {0:.2f}s".format(dur % 60,(dur / 60) % 60,dur / 3600,TOTAL_ROUND))
input("\a输入任何字符以结束:\n")