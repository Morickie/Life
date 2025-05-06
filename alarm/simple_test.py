# 导入所需模块
import threading
from time import sleep
import pyttsx3
import random
import pygame
import tkinter as tk
from tkinter import font
import os

# 运动计时器主类
class ExerciseTimer:
    def __init__(self):
        # 初始化UI组件
        self.root = tk.Tk()
        self.root.title("Exercise Alarm")
        self.root.geometry("400x200")
        self.root.configure(bg="#ffdbdd")
        self.root.minsize(300, 150)
        self.root.resizable(True, True)
        
        # 初始化状态变量
        self.is_paused = False
        self.pause_event = threading.Event()
        
        # 定义动作组
        self.low_intensity = [
            "宽距深蹲", "平板支撑", "支撑开合跳", 
            '左右小步跑', '跳绳', '勾腿跳', 
            '左右跨步高踢腿', '左右小跳'
        ]
        
        self.high_intensity = [
            "波比跳", "高抬腿冲刺", "跳跃深蹲", 
            "登山跑", "弓箭步跳", "弓步单腿跳", 
            "侧滑步触地"
        ]
        
        # 初始化语音和音频
        self._init_audio()
        self._setup_ui()

    # 初始化音频系统
    def _init_audio(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("volume", 1.0)
            pygame.mixer.init()
            self.audio_path = os.path.join(os.path.dirname(__file__), 'music', 'ding.mp3')
        except Exception as e:
            print(f"[_init_audio] 初始化音频失败: {str(e)}")
            raise

    # 设置UI界面
    def _setup_ui(self):
        # 创建动作标签
        large_font = font.Font(family="Microsoft YaHei", size=30)
        self.action_label = tk.Label(
            self.root, text="", 
            font=large_font, bg="#ffdbdd", fg="#333333"
        )
        self.action_label.pack(expand=True, pady=(10, 5))
        
        # 创建倒计时标签
        small_font = font.Font(family="Microsoft YaHei", size=20)
        self.countdown_label = tk.Label(
            self.root, text="", 
            font=small_font, bg="#ffdbdd", fg="#555555"
        )
        self.countdown_label.pack(expand=True, pady=(0, 10))
        
        # 创建按钮框架
        self.button_frame = tk.Frame(self.root, bg="#ffdbdd", padx=10, pady=10)
        self.button_frame.pack()
        
        # 创建按钮
        self._create_buttons()

    # 创建控制按钮
    def _create_buttons(self):
        button_font = font.Font(family="Microsoft YaHei", size=14)
        
        # 暂停按钮
        self.pause_button = tk.Button(
            self.button_frame, text="暂停", 
            command=self.toggle_pause, width=10, height=2,
            bg="#ffadd5", fg="black", activebackground="#e69fc8",
            relief=tk.RAISED, font=button_font
        )
        self.pause_button.pack(side=tk.LEFT, padx=10)
        
        # 切换动作按钮
        self.switch_button = tk.Button(
            self.button_frame, text="切换动作", 
            command=self.toggle_action, width=10, height=2,
            bg="#ffadd5", fg="black", activebackground="#a3e8d0",
            relief=tk.RAISED, font=button_font
        )
        self.switch_button.pack(side=tk.LEFT, padx=10)

    # 播放提醒音
    def play_alarm(self):
        try:
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play(1)
            while pygame.mixer.music.get_busy():
                pass
        except Exception as e:
            print(f"[play_alarm] 播放音频失败: {str(e)}")

    # 更新动作标签
    def update_action_label(self, action):
        self.action_label.config(text=action)
        self.root.update()

    # 更新倒计时显示
    def update_countdown(self, seconds):
        self.countdown_label.config(text=f"剩余时间: {seconds}秒")
        self.root.update()

    # 倒计时函数
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            if self.pause_event.is_set():
                self.update_countdown("已暂停")
                while self.pause_event.is_set():
                    sleep(0.1)
                self.update_countdown(f"剩余时间: {i}秒")
            self.update_countdown(i)
            sleep(1)

    # 暂停/继续功能
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="继续")
            self.pause_event.set()
        else:
            self.pause_button.config(text="暂停")
            self.pause_event.clear()

    # 切换动作功能
    def toggle_action(self):
        try:
            current_text = self.action_label.cget("text")
            if current_text in self.high_intensity:
                new_action = random.choice(self.low_intensity)
            elif current_text in self.low_intensity:
                new_action = random.choice(self.high_intensity)
            else:
                new_action = random.choice(self.high_intensity + self.low_intensity)
            self.update_action_label(new_action)
            self.engine.say(new_action)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[toggle_action] 切换动作出错: {str(e)}")

    # 检查暂停状态
    def _check_pause_status(self):
        if self.pause_event.is_set():
            self.update_action_label("已暂停")
            while self.pause_event.is_set():
                sleep(0.1)
            self.update_action_label("继续运动")

    # 执行动作
    def _perform_action(self, action_list, duration):
        action = random.choice(action_list)
        self.update_action_label(action)
        self.engine.say(action)
        self.engine.runAndWait()
        self.countdown(duration)
        self.play_alarm()

    # 主运动逻辑
    def exercise_logic(self):
        try:
            for round in range(4):
                self._check_pause_status()
                self._perform_action(self.high_intensity, 60)
                
                self._check_pause_status()
                self._perform_action(self.low_intensity, 60)
                
                self._check_pause_status()
                self._perform_action(self.high_intensity, 30)
                
                self._check_pause_status()
                self.update_action_label('休息1分钟')
                self.engine.say('休息1分钟')
                self.countdown(60)
        except Exception as e:
            print(f"[exercise_logic] 运动逻辑出错: {str(e)}")

    # 启动计时器
    def start(self):
        exercise_thread = threading.Thread(target=self.exercise_logic)
        exercise_thread.daemon = True
        exercise_thread.start()
        self.root.mainloop()

# 程序入口
if __name__ == "__main__":
    timer = ExerciseTimer()
    timer.start()