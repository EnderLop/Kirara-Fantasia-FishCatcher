# Kirara Fantasia代肝脚本Ver.2.3.1.210123
# -*- coding: utf-8 -*-
# @author:EnderLop
import time, win32api, win32con
import numpy as np
from PIL import ImageGrab


# 全局变量声明
TOTAL_ROUND = 0
WIDTH, HEIGHT = 16000, 9000
POSITION, COLOR = [], []


"""游戏预先处理单元"""
'''游戏主窗口边界查找'''
def corner_finder():
    global WIDTH, HEIGHT, POSITION, COLOR
    print("请在2秒内将光标移至游戏界面左上角\a")
    time.sleep(2)
    POSITION.append(win32api.GetCursorPos()[0])
    POSITION.append(win32api.GetCursorPos()[1])
    print("请在2秒内将光标移至游戏界面右下角\a")
    time.sleep(2)
    POSITION.append(win32api.GetCursorPos()[0])
    POSITION.append(win32api.GetCursorPos()[1])
    print("请在2秒内将光标移至游戏界面边框上\a")
    time.sleep(2)
    info = detect_flash()
    COLOR = info[win32api.GetCursorPos()[0], win32api.GetCursorPos()[1]].tolist()

'''游戏主窗口边界细化'''
def corner_accurater():
    global WIDTH, HEIGHT, POSITION, COLOR
    info = detect_flash()
    for j in range(max(POSITION[1] - 10, 0), min(POSITION[1] + 10, len(info[0]) - 1)):
        for i in range(max(POSITION[0] - 10, 0), min(POSITION[0] + 10, len(info) - 1)):
            if not info[i, j].tolist() == COLOR:
                POSITION[0], POSITION[1] = i, j
    for j in range(min(POSITION[3] + 10, len(info[0]) - 1), max(POSITION[3] - 10, 0), -1):
        for i in range(min(POSITION[2] + 10, len(info) - 1), max(POSITION[2] - 10, 0), -1):
            if not info[i, j].tolist() == COLOR:
                POSITION[2], POSITION[3] = i, j
    WIDTH, HEIGHT = POSITION[2] - POSITION[0], POSITION[3] - POSITION[1]

'''1080P→窗口化绝对位置调整'''
def state_transform(x_origin, y_origin):
    global WIDTH, HEIGHT, POSITION
    x_new = POSITION[0] + x_origin / 1920 * WIDTH  # X轴绝对位置变换
    y_new = POSITION[1] + y_origin / 1080 * HEIGHT  # Y轴绝对位置变换
    return int(x_new), int(y_new)


"""游戏信息获取单元"""
'''截取当前屏幕色块信息'''
def detect_flash():
    pic = ImageGrab.grab()  # 截屏
    info = np.asarray(pic, 'int')  # 图像数字化
    info = info.swapaxes(0, 1)  # Shape转置
    return info

'''判断当前位置颜色是否含有特殊信息'''
def color_compare(info, state_x, state_y, R, G, B):
    if info[state_transform(state_x, state_y)].tolist() == [R, G, B]:
        return True
    else:
        return False

'''鼠标操作'''
def mouse_click(state_x, state_y, n):
    win32api.SetCursorPos((state_x, state_y))
    for i in range(n):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

'''判断珍藏技是否准备就绪'''
def star_shine(info):
    if color_compare(info, 655, 965, 7, 227, 209) and color_compare(info, 655, 920, 250, 250, 235):  # 检查珍藏第一颗星星为亮蓝 且 周遭界面亮
        return True
    elif color_compare(info, 655, 965, 119, 92, 92) and color_compare(info, 655, 920, 125, 125, 117):  # 检查珍藏第一颗星星为深粉 且 周遭界面暗
        return False

'''判断当前是否为AUTO模式'''
def auto_shine(info):
    if color_compare(info, 1825, 30, 255, 255, 255) and color_compare(info, 1820, 55, 255, 255, 255):  # 检查AUTO箭头头部为纯白
        return True
    elif color_compare(info, 1825, 30, 110, 65, 53) and color_compare(info, 1850, 40, 255, 253, 228):  # 检查AUTO箭头头部为深棕 且 周遭界面白
        return False

'''判断当前是否已完成对战'''
def finish_shine(info):
    if color_compare(info, 1080, 225, 255, 154, 185) and color_compare(info, 1450, 655, 255, 255, 255):  # 检查表头为亮粉 且 两按钮间为纯白
        return True
    else:
        return False


"""战斗阶段响应单元"""
'''在珍藏技准备就绪的情况下释放芳文跳'''
def fangwen_jump(info):
    if star_shine(info):
        if auto_shine(info):  # 关闭AUTO
            for round in range(5):
                if auto_shine(detect_flash()):
                    mouse_click(state_transform(1825, 30)[0], state_transform(1825, 30)[1], 1)
                    time.sleep(0.25)
                elif not auto_shine(detect_flash()) and not (auto_shine(detect_flash()) is None):
                    break
            else:
                return None
        mouse_click(state_transform(655, 965)[0], state_transform(655, 965)[1], 1)
        time.sleep(0.5)
    elif color_compare(detect_flash(), 1350, 920, 3, 113, 104):
        mouse_click(state_transform(1690, 190)[0], state_transform(1690, 190)[1], 1)
        time.sleep(0.5)
        mouse_click(state_transform(1565, 965)[0], state_transform(1565, 965)[1], 1)
        time.sleep(0.5)
        for i in range(7):
            mouse_click(state_transform(960, 540)[0], state_transform(960, 540)[1], 1)
            time.sleep(1)
        print("{}：完成一次芳文跳释放".format(time.strftime("%Y/%m/%d %H:%M:%S")))

'''在珍藏技未就绪的情况下开启AUTO模式'''
def feel_fish(info):
    if not star_shine(info) and not auto_shine(info) and not (star_shine(info) is None) and not (auto_shine(info) is None):
        for round in range(5):
            if not auto_shine(detect_flash()) and not (auto_shine(detect_flash()) is None):
                mouse_click(state_transform(1825, 30)[0], state_transform(1825, 30)[1], 1)
                time.sleep(0.5)
                break
        else:
            return None

'''在对战结束后点击跳过结算界面'''
def finally_finsih(info):
    if finish_shine(info):
        time.sleep(1)
        for round in range(5):
            mouse_click(state_transform(960, 800)[0], state_transform(960, 800)[1], 1)
            time.sleep(1)
            if color_compare(detect_flash(), 630, 280, 255, 154, 185) and color_compare(detect_flash(), 630, 130, 127, 77, 92):
                time.sleep(1)
                mouse_click(state_transform(960, 680)[0], state_transform(960, 680)[1], 1)
        print("{}：完成一场大对战刷轮".format(time.strftime("%Y/%m/%d %H:%M:%S")))

'''在对战结束且仍有剩余体力的情况下自动再开一把对战'''
def restart_game(info):
    global TOTAL_ROUND
    if color_compare(info, 580, 85, 255, 154, 185) and color_compare(info, 695, 885, 200, 152, 110):
        mouse_click(state_transform(630, 990)[0], state_transform(630, 990)[1], 1)
        time.sleep(3)
        TOTAL_ROUND += 1
        print("{0}：已完成{1}场战斗,正在开始第{2}场战斗".format(time.strftime("%Y/%m/%d %H:%M:%S"), TOTAL_ROUND, TOTAL_ROUND+1))

'''主函数'''
def main():
    fangwen_jump(detect_flash())
    feel_fish(detect_flash())
    finally_finsih(detect_flash())
    restart_game(detect_flash())


'''运行函数'''
corner_finder()
corner_accurater()
mouse_position = (1, 1)
print("脚本启动中...")
time.sleep(5)
print("\a{}：代肝工作开始".format(time.strftime("%Y/%m/%d %H:%M:%S")))
timeStart = time.perf_counter()
while mouse_position != (0, 0):
    mouse_position = win32api.GetCursorPos()
    main()
dur = time.perf_counter() - timeStart
print("\a{}：代肝工作结束".format(time.strftime("%Y/%m/%d %H:%M:%S")))
print("共完成{3}场对战的刷轮，总耗时为:{2:.0f}h {1:.0f}min {0:.2f}s".format(dur % 60, (dur / 60) % 60, dur / 3600, TOTAL_ROUND))
input("\a输入任何字符以结束:\n")
