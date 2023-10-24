import pygame as py
from win32api import GetMonitorInfo, MonitorFromPoint, RGB
from win32con import GWL_EXSTYLE, WS_EX_LAYERED, LWA_COLORKEY, WS_EX_TOOLWINDOW, SW_MAXIMIZE
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes, ShowWindow, SetForegroundWindow
from os import environ
from random import choice
from datetime import datetime
from time import sleep

title = 'Destkop Kaomoji'
font_size = 20
screen_width, screen_height = 75, 50
device = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")
# device_width, device_height = .GetSystemMetrics(0), win32api.GetSystemMetrics(1)
device_width, device_height = device[2], device[3]

screen_pos_x, screen_pos_y = device_width - screen_width, device_height - screen_height

# set window position
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_pos_x, screen_pos_y)

py.init()

py.display.set_caption(title)

screen = py.display.set_mode((screen_width, screen_height), py.NOFRAME)

# get window from py
hwnd = py.display.get_wm_info()["window"]

# allow window transparency
color_to_alpha = 128
SetWindowLong(hwnd, GWL_EXSTYLE, GetWindowLong(
                        hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
SetLayeredWindowAttributes(hwnd, RGB(color_to_alpha, color_to_alpha, color_to_alpha), 0, LWA_COLORKEY)

# hide window from taskbar
SetWindowLong(hwnd, GWL_EXSTYLE, GetWindowLong(hwnd, GWL_EXSTYLE) | WS_EX_TOOLWINDOW)

# maximize window
ShowWindow(hwnd, SW_MAXIMIZE)
SetForegroundWindow(hwnd)

# print(py.font.get_fonts())
# font = py.font.Font(None, 25)
font = py.font.SysFont('arial', font_size)

kaomojis = [
    '*-*',
    '^-^',
    '^o^',
    '^u^',
    'T-T',
    'O.O',
    'o.O',
    'O.o',
    'U.U',
    'U.u',
    'u.U',
    'u.u',
]

kaomoji = choice(kaomojis)

text = font.render(kaomoji, True, (255, 255, 255, 0))
text_rect = text.get_rect()
text_x = (screen_width - text_rect.width) / 2
text_y = (screen_height - text_rect.height) / 2

current_time = datetime.now()
seconds = 60

clock = py.time.Clock()

while True:
    time_difference = int((current_time - datetime.now()).total_seconds())*-1

    if time_difference > seconds:
        current_time = datetime.now()
        kaomoji = choice(kaomojis)
        text = font.render(kaomoji, True, (255, 255, 255, 0))
        text_rect = text.get_rect()
        text_x = (screen_width - text_rect.width) / 2
        text_y = (screen_height - text_rect.height) / 2

    screen.fill((color_to_alpha, color_to_alpha, color_to_alpha))

    screen.blit(text, (text_x, text_y))

    py.display.update()
    clock.tick(1)
