# 导入所需模块
import threading
from time import sleep
import pyttsx3
import random
import pygame
import tkinter as tk
from tkinter import font
import os

# 初始化Tkinter窗口
root = tk.Tk()
root.title("Exercise Alarm")
root.geometry("400x200")

# 创建大字体标签
large_font = font.Font(size=30)
action_label = tk.Label(root, text="", font=large_font)
action_label.pack(expand=True)

# 初始化语音引擎
engine = pyttsx3.init()
engine.setProperty("volume", 1.0)

# 定义动作组
low_intensity = [
    "宽距深蹲",
    "平板支撑",
    "支撑开合跳",
    '左右小步跑',
    '跳绳',
    '勾腿跳',
    '左右跨步高踢腿',
    '左右小跳',
]

high_intensity = [
    "波比跳",
    "高抬腿冲刺",
    "跳跃深蹲",
    "登山跑",
    "弓箭步跳",
    "弓步单腿跳",
    "侧滑步触地",
]

# 获取音频文件的绝对路径
audio_path = os.path.join(os.path.dirname(__file__), 'music', 'ding.mp3')

# 添加暂停状态变量
is_paused = False
pause_event = threading.Event()

# 播放提醒音
def play_alarm():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(1)
        while pygame.mixer.music.get_busy():
            pass
    except Exception as e:
        print(f"播放音频失败: {e}")

# 更新动作标签
def update_action_label(action):
    action_label.config(text=action)
    root.update()

# 暂停/继续功能
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="继续")
        pause_event.set()
    else:
        pause_button.config(text="暂停")
        pause_event.clear()

# 创建暂停按钮
# 增大按钮的宽度和高度，同时设置突出的背景颜色
pause_button = tk.Button(root, text="暂停", command=toggle_pause, width=10, height=2)
pause_button.pack()

# 运动逻辑
def exercise_logic():
    try:
        for round in range(4):
            if pause_event.is_set():
                update_action_label("已暂停")
                while pause_event.is_set():
                    sleep(0.1)
                update_action_label("继续运动")
            
            action = random.choice(high_intensity)
            update_action_label(action)
            engine.say(action)
            engine.runAndWait()
            sleep(2)
            play_alarm()
            
            if pause_event.is_set():
                update_action_label("已暂停")
                while pause_event.is_set():
                    sleep(0.1)
                update_action_label("继续运动")
            
            action = random.choice(low_intensity)
            update_action_label(action)
            engine.say(action)
            engine.runAndWait()
            sleep(2)
            play_alarm()
            
            if pause_event.is_set():
                update_action_label("已暂停")
                while pause_event.is_set():
                    sleep(0.1)
                update_action_label("继续运动")
            
            action = random.choice(high_intensity)
            update_action_label(action)
            engine.say(action)
            engine.runAndWait()
            sleep(2)
            play_alarm()
            
            if pause_event.is_set():
                update_action_label("已暂停")
                while pause_event.is_set():
                    sleep(0.1)
                update_action_label("继续运动")
            
            update_action_label('休息1分钟')
            engine.say('休息1分钟')
            sleep(2)
    except Exception as e:
        print(f"运动逻辑出错: {e}")

# 启动运动逻辑线程
exercise_thread = threading.Thread(target=exercise_logic)
exercise_thread.daemon = True
exercise_thread.start()

# 启动主循环
root.mainloop()