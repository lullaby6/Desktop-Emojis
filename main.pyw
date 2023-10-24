import pygame as py
from win32api import GetMonitorInfo, MonitorFromPoint, RGB
from win32con import GWL_EXSTYLE, WS_EX_LAYERED, LWA_COLORKEY, WS_EX_TOOLWINDOW, SW_MAXIMIZE, HWND_TOPMOST, SWP_NOMOVE, SWP_NOSIZE
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes, ShowWindow, SetForegroundWindow, SetWindowPos
from os import environ
from random import choice
from datetime import datetime
from time import sleep
from sys import exit
from json import loads

config_file = open("config.json", "r")
config_json = config_file.read()
config = loads(config_json)
config_file.close()

title = 'Desktop Emojis'

font_size = config.get('font_size', 18)
screen_width, screen_height = config.get('screen_width', 75), config.get('screen_height', 50)

time_between_emojis = config.get('time_between_emojis', 60000)
sleep_time = config.get('sleep_time', 1000)

emojis = config.get('emojis', [
    '*-*',
    '^-^',
    'T-T',
    'O.O',
    'u.u',
    'UwU',
    'UoU',
    ';-;',
])

transparency = (128, 128, 128)

def emoji_text():
    # load font
    font = py.font.Font(None, font_size)
    if 'arial' in py.font.get_fonts():
        font = py.font.SysFont('arial', font_size)

    emoji = choice(emojis)
    text = font.render(emoji, True, (255, 255, 255, 0))
    text_rect = text.get_rect()
    text_x = (screen_width - text_rect.width) / 2
    text_y = (screen_height - text_rect.height) / 2

    return [text, text_x, text_y]

def init():
    device = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")
    device_width, device_height = device[2], device[3]

    screen_pos_x, screen_pos_y = device_width - screen_width, device_height - screen_height

    # set window position
    environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_pos_x, screen_pos_y)

    py.init()

    py.display.set_caption(title)

    screen = py.display.set_mode((screen_width, screen_height), py.NOFRAME)

    # get window from pygame
    hwnd = py.display.get_wm_info()["window"]

    # allow window transparency
    SetWindowLong(hwnd, GWL_EXSTYLE, GetWindowLong(
                            hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
    SetLayeredWindowAttributes(hwnd, RGB(*transparency), 0, LWA_COLORKEY)

    # hide window from taskbar
    SetWindowLong(hwnd, GWL_EXSTYLE, GetWindowLong(hwnd, GWL_EXSTYLE) | WS_EX_TOOLWINDOW)

    # set window position fixed
    SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

    # maximize window
    ShowWindow(hwnd, SW_MAXIMIZE)
    SetForegroundWindow(hwnd)

    return screen

def update(screen):
    text, text_x, text_y = emoji_text()

    current_time = datetime.now()

    running = True

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        time_difference = int((current_time - datetime.now()).total_seconds())*-1

        if time_difference > (time_between_emojis / 1000):
            current_time = datetime.now()

            text, text_x, text_y = emoji_text()

        screen.fill(transparency)

        screen.blit(text, (text_x, text_y))

        py.display.update()

        sleep(sleep_time / 1000)

def quit():
    py.quit()
    exit()

def main():
    screen = init()

    update(screen)

    quit()

if __name__ == "__main__":
	main()