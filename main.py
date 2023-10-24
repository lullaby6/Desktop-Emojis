import pygame, win32api, win32con, win32gui
from os import environ
from random import choice
from time import sleep
from datetime import datetime
from sys import exit

title = 'Destkop Kaomoji'
font_size = 20
screen_width, screen_height = 75, 50
device = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0))).get("Work")
# device_width, device_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
device_width, device_height = device[2], device[3]

screen_pos_x, screen_pos_y = device_width - screen_width, device_height - screen_height

environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_pos_x, screen_pos_y)

pygame.init()

pygame.display.set_caption(title)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

# get window from pygame
hwnd = pygame.display.get_wm_info()["window"]

# allow window transparency
color_to_alpha = 128
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                        hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(color_to_alpha, color_to_alpha, color_to_alpha), 0, win32con.LWA_COLORKEY)

# hide window from taskbar
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOOLWINDOW)

# maximize window
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
win32gui.SetForegroundWindow(hwnd)

# print(pygame.font.get_fonts())
# font = pygame.font.Font(None, 25)
font = pygame.font.SysFont('arial', font_size)

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

current_time = datetime.now()
seconds = 60

running = True
while running:
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    try: win32gui.SetForegroundWindow(hwnd)
    except Exception as e: pass

    time_difference = int((current_time - datetime.now()).total_seconds())*-1

    if time_difference > seconds:
        current_time = datetime.now()
        kaomoji = choice(kaomojis)

    screen.fill((color_to_alpha, color_to_alpha, color_to_alpha))

    text = font.render(kaomoji, True, (255, 255, 255, 0))
    text_rect = text.get_rect()
    text_x = (screen_width - text_rect.width) / 2
    text_y = (screen_height - text_rect.height) / 2

    screen.blit(text, (text_x, text_y))

    pygame.display.flip()

    sleep(1)

pygame.quit()
exit()
