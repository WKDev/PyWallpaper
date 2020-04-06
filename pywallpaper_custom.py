import os, sys, random, ctypes
import time
from PIL import Image

import os


def get_wallpaper_label():
    os.path.abspath(os.getcwd())
    wallpaper_list = os.listdir('./wallpaper/Catalina')
    return wallpaper_list

# https://512pixels.net/projects/default-mac-wallpapers-in-5k/

def change_wallpaper(wallpaper_list):
    # print(wallpaper_list[1])
    # print(t.tm_hour % 3)
    # print('{}:{}'.format(t.tm_hour, t.tm_min))

    'C:/Users/chanh/PyCharmProjects/PyWallpaper/wallpaper/Mojave/10-14-Mojave-15.jpg'
    if (t.tm_sec == 58) and (t.tm_min == 0) and (t.tm_hour % 3 == 0):
        print("정각이므로 시간을 바꿉니다.")
        wallpaper_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(t.tm_hour // 3)-1]
        # wallpaper_path.replace('\\', '/')
        # print(wallpaper_path, t.tm_hour // 3)
        ctypes.windll.user32.SystemParametersInfoW(0x14, 0, wallpaper_path, 0x3)  # SystemParametersInfoA
    else:
        print('현재 시간 {}:{}'.format(t.tm_hour, t.tm_min))


if __name__ == '__main__':
    list = get_wallpaper_label()

    # image = Image.open("image.gif")
    # icon = pystray.Icon(name="SPAM!", icon=image, title="MOBASuite", menu=None)

    while True:
        # icon.run()
        t = time.localtime()
        
        change_wallpaper(list)
