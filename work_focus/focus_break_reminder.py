# 间歇提醒程序，每5分钟随机在3-5分钟时响铃提醒
import time
import random
import subprocess
import sys
import pystray
from PIL import Image
import threading
import os
import traceback

# 全局变量控制计时状态
is_paused = False

def play_alarm():
    # 播放提醒铃声
    try:
        alarm_file = "e:\\BaiduSyncdisk\\python_promgram\\Life\\alarm\\music\\ding.mp3"
        subprocess.Popen(["start", "", alarm_file], shell=True)
    except Exception as e:
        print(f"播放铃声时出错: {str(e)}", file=sys.stderr)

def create_image(paused=False):
    # 创建托盘图标，暂停时为红色，否则为蓝色
    from PIL import Image, ImageDraw
    image = Image.new('RGB', (16, 16), 'white')
    dc = ImageDraw.Draw(image)
    color = 'red' if paused else 'blue'
    dc.rectangle((0, 0, 15, 15), fill=color)
    return image

def on_clicked(icon, item):
    # 托盘菜单点击事件
    global is_paused
    try:
        if str(item) == "暂停" or str(item) == "继续":
            is_paused = not is_paused
            # 重新创建菜单项来更新文本
            menu = pystray.Menu(
                pystray.MenuItem("继续" if is_paused else "暂停", on_clicked),
                pystray.MenuItem("退出", on_clicked)
            )
            icon.menu = menu
            # 更新图标颜色
            icon.icon = create_image(is_paused)
        elif str(item) == "退出":
            # 先停止图标，再退出
            icon.stop()
            # 使用os._exit而不是sys.exit
            os._exit(0)
    except Exception as e:
        print(f"菜单操作出错: {str(e)}", file=sys.stderr)
        traceback.print_exc()

def run_timer():
    # 主计时逻辑
    total_duration = 60 * 60  # 60分钟
    interval = 5 * 60  # 5分钟
    
    for i in range(0, total_duration, interval):
        # 随机选择3-5分钟之间的时间点
        wait_time = random.randint(3*60, 5*60)
        
        # 等待期间检查暂停状态
        for _ in range(wait_time):
            if not is_paused:
                time.sleep(1)
            else:
                time.sleep(0.1)
                continue
                
        if not is_paused:
            play_alarm()
        
        # 等待剩余时间
        remaining_time = interval - wait_time
        if remaining_time > 0:
            for _ in range(remaining_time):
                if not is_paused:
                    time.sleep(1)
                else:
                    time.sleep(0.1)
                    continue

def main():
    # 创建系统托盘
    menu = pystray.Menu(
        pystray.MenuItem("暂停", on_clicked),
        pystray.MenuItem("退出", on_clicked)
    )
    
    # 启动计时器线程
    timer_thread = threading.Thread(target=run_timer)
    timer_thread.daemon = True
    timer_thread.start()
    
    # 运行系统托盘，初始状态为蓝色
    icon = pystray.Icon("focus_break_reminder", create_image(), "专注休息提醒", menu)
    icon.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"程序运行时出错: {str(e)}", file=sys.stderr)