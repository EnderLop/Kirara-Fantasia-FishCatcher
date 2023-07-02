# Kirara Fantasia代肝脚本Ver.4.3.1.211003
# -*- coding: utf-8 -*-
# @author:EnderLop
import numpy as np
import time, os, win32api, win32con, win32gui, win32ui
from ast import literal_eval
from operator import eq
from PIL import Image


"""全局变量声明"""
TOTAL_ROUND = 0
WIDTH, HEIGHT = 16000, 9000
FANGWEN_STARS = 0
HANDLE_CONFIG_FILE_ROAD = os.getcwd() + r'\Handle_Config.txt'
COLOR_DICTIONARY_FILE_ROAD = os.getcwd() + r'\Color_Dictionary.txt'
CLASS_DICTIONARY_FILE_ROAD = os.getcwd() + r'\Class_Dictionary.txt'
WINDOW_ID, CLICKABLE_WINDOW_ID, MONITOR_WINDOW_ID = 0, 0, 0
COLOR_INFO = []
CLASS_DICTIONARY, COLOR_DICTIONARY = {}, {}


"""游戏原始信息读入单元"""
'''句柄配置文件写入应用'''
def handle_config_file_writer():
    global WINDOW_ID, HANDLE_CONFIG_FILE_ROAD
    print("\a首次使用，将开始程序适配")
    time.sleep(2)
    print("\a请在五秒内将模拟窗口置顶")
    time.sleep(5)
    WINDOW_ID = win32gui.GetForegroundWindow()  # 获取最前端活动窗口句柄
    window_name = win32gui.GetWindowText(WINDOW_ID)  # 获取该窗口句柄对应标题
    with open(HANDLE_CONFIG_FILE_ROAD, 'w', encoding = 'utf-8') as handle_config_file:
        handle_config_file.write(window_name)  # 创建标题文件并写入标题信息
    print("\a配置成功！将运行代肝脚本")
    time.sleep(3)
    os.system("cls")

'''句柄配置文件读入应用'''
def handle_config_file_reader():
    global WINDOW_ID, HANDLE_CONFIG_FILE_ROAD
    with open(HANDLE_CONFIG_FILE_ROAD, 'r', encoding = 'utf-8') as handle_config_file:
        window_name = handle_config_file.read()
    WINDOW_ID = win32gui.FindWindow(None, window_name)

'''色彩字典文件读入应用'''
def color_dictionary_file_reader():
    global COLOR_DICTIONARY, COLOR_DICTIONARY_FILE_ROAD
    with open(COLOR_DICTIONARY_FILE_ROAD, 'r', encoding = 'utf-8') as color_dictionary_file:
        COLOR_DICTIONARY = literal_eval(color_dictionary_file.read())

'''窗口类型字典读入应用'''
def class_dictionary_file_reader():
    global CLASS_DICTIONARY, CLASS_DICTIONARY_FILE_ROAD
    with open(CLASS_DICTIONARY_FILE_ROAD, 'r', encoding = 'utf-8') as class_dictionary_file:
        CLASS_DICTIONARY = literal_eval(class_dictionary_file.read())


"""游戏窗口句柄应用单元"""
'''游戏子句柄穷举及应用'''
def children_windows_scanner():
    global WINDOW_ID, CLICKABLE_WINDOW_ID, MONITOR_WINDOW_ID
    if not WINDOW_ID:
        return None
    child_list = []
    win32gui.EnumChildWindows(WINDOW_ID, lambda hwnd, param: param.append(hwnd), child_list)  # 枚举各子窗口句柄
    for _suspect_target in child_list:
        if win32gui.GetWindowText(_suspect_target) in CLASS_DICTIONARY['MONITOR_WINDOW_CLASS']:
            MONITOR_WINDOW_ID = _suspect_target  # 查找监视窗口句柄
            if win32gui.GetWindowText(_suspect_target) == 'sub':
                CLICKABLE_WINDOW_ID = WINDOW_ID  # 最新版NOX模拟器监视窗口类型
        if win32gui.GetWindowText(_suspect_target) in CLASS_DICTIONARY['CLICKABLE_WINDOW_CLASS']:
            CLICKABLE_WINDOW_ID = _suspect_target  # 查找操作窗口句柄
        if MONITOR_WINDOW_ID * CLICKABLE_WINDOW_ID != 0:
            break
    else:
        input("未找到游戏句柄！")

'''游戏窗口边框信息读入'''
def window_edge_scanner():
    global WIDTH, HEIGHT, MONITOR_WINDOW_ID
    _four_state = win32gui.GetWindowRect(MONITOR_WINDOW_ID)
    WIDTH, HEIGHT = _four_state[2] - _four_state[0], _four_state[3] - _four_state[1]

'''监视窗口绝对坐标转换'''
def monitor_window_transformer(x_origin, y_origin):
    global WIDTH, HEIGHT
    x_new = x_origin / 1920 * WIDTH  # X轴绝对位置变换
    y_new = y_origin / 1080 * HEIGHT  # Y轴绝对位置变换
    return int(x_new), int(y_new)

'''操作窗口绝对坐标转换'''
def clickable_window_transformer(x_origin, y_origin):
    global WIDTH, HEIGHT, MONITOR_WINDOW_ID, CLICKABLE_WINDOW_ID
    _monitor_window_edge = win32gui.GetWindowRect(MONITOR_WINDOW_ID)
    _clickable_window_edge = win32gui.GetWindowRect(CLICKABLE_WINDOW_ID)
    x_new = _monitor_window_edge[0] - _clickable_window_edge[0] + x_origin / 1920 * WIDTH  # X轴绝对位置变换
    y_new = _monitor_window_edge[1] - _clickable_window_edge[1] + y_origin / 1080 * HEIGHT  # Y轴绝对位置变换
    return int(x_new), int(y_new)


"""游戏信息获取处理单元"""
'''截取当前屏幕色块信息'''
def monitor_window_scanner():
    global WIDTH, HEIGHT, MONITOR_WINDOW_ID, COLOR_INFO
    hWndDC = win32gui.GetWindowDC(MONITOR_WINDOW_ID)
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, WIDTH, HEIGHT)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (WIDTH, HEIGHT), mfcDC, (0, 0), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    COLOR_INFO = np.asarray(image, 'int').swapaxes(0, 1)  # 图像数字化
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(MONITOR_WINDOW_ID, hWndDC)  # 释放内存

'''游戏特殊位置颜色比对'''
def color_comparator(annotation):
    global COLOR_INFO, COLOR_DICTIONARY
    _content = COLOR_DICTIONARY[annotation]
    _screen_color = tuple(COLOR_INFO[monitor_window_transformer(_content[0][0], _content[0][1])])
    if eq(_screen_color, _content[1]):
        return True
    else:
        return False

'''后台句柄模拟鼠标操作'''
def mouse_click_simulator(state_x, state_y, n = 1, pause_time = 0.5, waiting_time = 0):
    global CLICKABLE_WINDOW_ID
    _x_new, _y_new = clickable_window_transformer(state_x, state_y)
    _coordinate = win32api.MAKELONG(_x_new, _y_new)
    for i in range(n):
        win32gui.SendMessage(CLICKABLE_WINDOW_ID, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)  # 激活窗口
        time.sleep(0.25)
        win32api.PostMessage(CLICKABLE_WINDOW_ID, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, _coordinate)  # 模拟按下鼠标左键
        time.sleep(0.25)
        win32api.PostMessage(CLICKABLE_WINDOW_ID, win32con.WM_LBUTTONUP, 0000, _coordinate)  # 模拟松开鼠标左键
        time.sleep(pause_time)
    time.sleep(waiting_time)


"""战斗进程信息处理单元"""
'''判断珍藏技是否已就绪'''
def star_key_shine():
    monitor_window_scanner()
    if color_comparator('珍藏技能板块整体呈亮') and color_comparator('珍藏第一颗星星为亮蓝'):
        return True
    elif color_comparator('珍藏技能板块整体呈暗') and color_comparator('珍藏第一颗星星为深粉'):
        return False

'''判断当前是否为AUTO模式'''
def auto_key_shine():
    monitor_window_scanner()
    if color_comparator('自动箭头上箭头呈纯白') and color_comparator('自动箭头下箭头呈纯白'):
        return True
    elif color_comparator('自动战斗板块整体呈亮') and color_comparator('自动箭头上箭头呈深棕') and color_comparator('自动箭头下箭头呈深棕'):
        return False

'''判断当前是否已完成对战'''
def finish_key_shine():
    monitor_window_scanner()
    if color_comparator('结束界面标题上界上白') and color_comparator('结束界面标题上界下粉') and color_comparator('结束界面标题左界左白') and color_comparator('结束界面标题左界右粉'):
        return True
    else:
        return False


"""战斗进程分析响应单元"""
'''准备就绪时释放芳文跳'''
def fangwen_jump():
    global FANGWEN_STARS
    monitor_window_scanner()
    if star_key_shine():
        for _round in range(5):
            if auto_key_shine():
                mouse_click_simulator(1825, 30, waiting_time = 0.25)
            elif auto_key_shine() is False:
                break
        else:
            return None
        mouse_click_simulator(655, 965)
    elif color_comparator('进入芳文跳序选择界面'):
        FANGWEN_STARS = 1
        if color_comparator('珍藏第二颗星星为亮黄'):
            FANGWEN_STARS += 1
            if color_comparator('珍藏第三颗星星为亮粉'):
                FANGWEN_STARS += 1
        for i in range(FANGWEN_STARS):
            mouse_click_simulator(1535, 210 + i * 270)
    elif color_comparator('芳文跳顺序已选择完毕'):
        mouse_click_simulator(1350, 920, 3, 0.5, 1.5)
        for j in range(FANGWEN_STARS):
            mouse_click_simulator(960, 540, waiting_time = 3)
        print("{}：完成一次芳文跳释放".format(time.strftime("%Y/%m/%d %H:%M:%S")))

'''在珍藏技未就绪的情况下开启AUTO模式'''
def feel_fish():
    if star_key_shine() is False:
        for _round in range(5):
            if auto_key_shine() is False:
                mouse_click_simulator(1825, 30, waiting_time = 0.25)
            elif auto_key_shine():
                break

'''在对战结束后点击跳过结算界面'''
def finally_finsih():
    if finish_key_shine():
        time.sleep(1)
        mouse_click_simulator(960, 795, 3, 1, 1)
        monitor_window_scanner()
        for i in range(5):
            if color_comparator('二级好感界面上界上白') and color_comparator('二级好感界面上界下粉') and color_comparator('二级好感界面左界左白') and color_comparator('二级好感界面左界右粉'):
                mouse_click_simulator(960, 910, 2, 1, 1)
                print("{}：队员好感度升至二级".format(time.strftime("%Y/%m/%d %H:%M:%S")))
            elif color_comparator('三级好感界面上界上白') and color_comparator('三级好感界面上界下粉') and color_comparator('三级好感界面左界左白') and color_comparator('三级好感界面左界右粉'):
                mouse_click_simulator(960, 935, 2, 1, 1)
                print("{}：队员好感度升至三级".format(time.strftime("%Y/%m/%d %H:%M:%S")))
            elif color_comparator('四级好感界面上界上白') and color_comparator('四级好感界面上界下粉') and color_comparator('四级好感界面左界左白') and color_comparator('四级好感界面左界右粉'):
                mouse_click_simulator(960, 910, 2, 1, 1)
                print("{}：队员好感度升至四级".format(time.strftime("%Y/%m/%d %H:%M:%S")))
            elif color_comparator('五级好感界面上界上白') and color_comparator('五级好感界面上界下粉') and color_comparator('五级好感界面左界左白') and color_comparator('五级好感界面左界右粉'):
                mouse_click_simulator(960, 815, 2, 1, 1)
                print("{}：队员好感度升至五级".format(time.strftime("%Y/%m/%d %H:%M:%S")))
            monitor_window_scanner()
        if color_comparator('作品升级界面上界上白') and color_comparator('作品升级界面上界下粉') and color_comparator('作品升级界面左界左白') and color_comparator('作品升级界面左界右粉'):
            mouse_click_simulator(960, 795, 2, 1, 1)
        mouse_click_simulator(960, 795, waiting_time = 1)

'''在对战结束且仍有剩余体力的情况下自动再开一把对战'''
def restart_game():
    global TOTAL_ROUND
    if color_comparator('重开界面标题上界上白') and color_comparator('重开界面标题上界下粉') and color_comparator('重开界面标题左界左白') and color_comparator('重开界面标题左界右粉'):
        mouse_click_simulator(630, 990, waiting_time = 3)
        TOTAL_ROUND += 1
        print("{0}：已经完成第{1}场战斗, 正在开始第{2}场战斗".format(time.strftime("%Y/%m/%d %H:%M:%S"), TOTAL_ROUND, TOTAL_ROUND+1))

def network_error_solvers():
    monitor_window_scanner()
    if color_comparator('停摆界面标题上界上白') and color_comparator('停摆界面标题上界下粉') and color_comparator('停摆界面标题左界左白') and color_comparator('停摆界面标题左界右粉'):
        mouse_click_simulator(960, 660, waiting_time = 1)
        print("{}：加速器出现连接异常".format(time.strftime("%Y/%m/%d %H:%M:%S")))

'''主函数'''
def main():
    network_error_solvers()
    fangwen_jump()
    feel_fish()
    finally_finsih()
    restart_game()

'''运行函数'''
class_dictionary_file_reader()
color_dictionary_file_reader()
if os.path.exists(HANDLE_CONFIG_FILE_ROAD):
    handle_config_file_reader()
else:
    handle_config_file_writer()
children_windows_scanner()
mouse_position = (1, 1)
print("请稍事等待，脚本正在启动中...")
time.sleep(3)
print("\a{}：代肝脚本已正常启动".format(time.strftime("%Y/%m/%d %H:%M:%S")))
timeStart = time.perf_counter()
while mouse_position != (0, 0):
    window_edge_scanner()
    main()
    mouse_position = win32api.GetCursorPos()
dur = int(time.perf_counter() - timeStart)
print("\a{}：代肝工作已顺利结束".format(time.strftime("%Y/%m/%d %H:%M:%S")))
print("共自动完成{3}场战斗，总耗时为:{2:.0f}h {1:.0f}min {0:.0f}s".format(dur % 60, (dur / 60) % 60, dur / 3600, TOTAL_ROUND))
print("\a程序将在10秒内自动关闭！")
time.sleep(10)
