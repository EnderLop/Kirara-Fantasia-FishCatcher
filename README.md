# Kirara-Fantasia-FishCatcher

# 脚本仅供群友活动末期赶成就或刷作品珠、专武、精神强化果实之用，请勿恶意、依赖使用或商用！
# 脚本仅供群友活动末期赶成就或刷作品珠、专武、精神强化果实之用，请勿恶意、依赖使用或商用！
# 脚本仅供群友活动末期赶成就或刷作品珠、专武、精神强化果实之用，请勿恶意、依赖使用或商用！

## 写了个智障Python脚本拯救电脑玩家的游戏体验和肝！
### 1. 使用Win32api库按句柄扫色、分析色块获取游戏进程信息并给出回应
* 实现战斗结束自动点击再来一关（体力够的话）
* 珍藏珠就绪芳文跳，跳完上AUTO
* 支持全屏幕和窗口化游戏
* 后台点击，不影响电脑正常使用
###	2. 后期更新方向
* 自动续表、设置最大游戏次数等功能
* 可能会兼容其他系统
* *【Kirara Fantasia于2023年2月28日终止运营】*


## 2021.1月初更新补充：
* 理论上只要模拟器能将游戏画面开到全屏就可以使用全屏模式
* 如果模拟器四面都有边框且颜色一致，理论上可使用窗口模式，但推荐用NOX模拟器（贴吧有教程）
## 2021.1月末更新补充：
* 210125的更新中提供了读取模拟器句柄进行分析的新版本，目前还不确定兼容性
* 目前我搜索到的后台鼠标点击教程都存在一定问题，用Spy++发现在MAKE_LONG加WA_ACTIVE方法中，模拟松开鼠标左键的PostMessage()指令存在参数错误，空下来写一篇CSDN帮帮后来人罢
* *【现实中烦的一比，README中写写抱怨的了，反正没人看得见：大二下真滴好忙，想写一篇百元外设体验VR露营的黑盒教程也没时间，还有这该死的GitHub，文件都传一半给我404，淦！】*
* *【其实已经可以实现后台操纵，但是这一方面仍在考虑中，挂后台刷游戏似乎让游戏失去了乐趣】*
* 开放后台句柄点击功能（KRF这个精神强化属实恶心到我了）
## 2021.5月末更新补充：
* 5月份游戏大更新直接枪毙了NOX模拟器，一方面仍在等待NOX官方回应，另一方面开始着手BlueStacks模拟器脚本的开发
* 210525的更新中提供了适应BlueStacks模拟器的脚本

## 使用方法【具体可参考“示例”文件夹中视频】：
### 1. 第一次启动：
* 运行“Config文件适配程序”，三秒内将模拟器置于屏幕最上层（活动窗口）
* 若成功会在源文件夹中出现一个新的“Config”文件
### 2. 启动：
* 使用模拟器开启KRF，进入将要刷次数的对战，点开脚本（成功跳忙音）
* *注意：为避免读不到窗口句柄的问题，请在打开脚本后多点几次模拟器窗口以激活*
* *注意：由于BlueStacks模拟器自身特性，在窗口缩小到一定比例后会自动模糊画质影响扫色，使用时请确保该窗口不要过小*
### 3. 停止：
* 将光标移至显示器左上角，一段时间后程序自动停止运行（成功跳忙音）
* *注意：若出现错误，请重启脚本【如遇死循环，请打开任务管理器关闭脚本】*
