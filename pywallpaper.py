import ctypes
import time
import cv2
import os

import sys
from PyQt5.QtWidgets import QApplication, QWidget

# https://512pixels.net/projects/default-mac-wallpapers-in-5k/

def get_wallpaper_label():
    os.path.abspath(os.getcwd())
    wallpaper_list = os.listdir('./wallpaper/Catalina')
    return wallpaper_list

def smooth_change(wallpaper_list):
    # image_amount = 8, wallpapers are changed every 3 hours(180min)
    # when resolution is 10, image_amount = 8, wallpapers are changed every 18min

    hour = time.localtime().tm_hour
    min = time.localtime().tm_min
    sec = time.localtime().tm_sec

    elasped = min + hour * 60
    if hour % 3 == 0 and min == 0 and sec < 20:
        cur_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(hour // 3) ]
        prev_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(hour // 3)-1]
        cur_pic = cv2.imread(cur_pic_path)
        prev_pic = cv2.imread(prev_pic_path)

    if (elasped % 18 == 0) and sec <10:
        mix = (elasped - (hour // 3) * 180) * 10 / 18
        print(elasped, mix)
        print('배경화면을 변경합니다. time {}:{},  elasped :{}   cur : {} {}%, prev :{} {}%'
              .format(hour, min, elasped,wallpaper_list[(hour // 3)][:-4],mix, wallpaper_list[(hour // 3) -1][:-4], (100 - mix)))

        try:
            weighted_img = cv2.addWeighted(cur_pic, float(mix) / 100, prev_pic, float(100 - mix) / 100, 0)
        except:
            print('배경화면이 불러와져 있지않아 불러온 후 이미지를 처리합니다.')
            cur_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(hour // 3)]
            prev_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(hour // 3)-1]
            cur_pic = cv2.imread(cur_pic_path)
            prev_pic = cv2.imread(prev_pic_path)
            weighted_img = cv2.addWeighted(cur_pic, float(mix) / 100, prev_pic, float(100 - mix) / 100, 0)

        t1 = time.time()
        cv2.imwrite('wallpaper.jpg', weighted_img)
        t2 = time.time()
        print('배경화면 생성 완료, {}초 소요'.format(t2 - t1))
        apply_wallpaper()

def apply_wallpaper():
    hour = time.localtime().tm_hour
    min = time.localtime().tm_min
    sec = time.localtime().tm_sec

    curr_min = min + hour * 60
    while not curr_min % 18 == 0:
        curr_min += 1
    wallpaper_path = os.getcwd() + r'\wallpaper.jpg'
    print('경로 :' + wallpaper_path)
    print('에서 배경화면 적용 완료. 다음 적용 시간은 {}:{}입니다.'.format(curr_min // 60, curr_min - hour * 60))
    ctypes.windll.user32.SystemParametersInfoW(0x14, 0, wallpaper_path, 0x3)  # SystemParametersInfoA

class Gui(QWidget):
    def __init__(self):
        super.__init__()
        self.initUI(self)

    def initUI(self):
        self.setWindowTitle('PyWallpaper')
        self.move(600,600)
        self.resize(1920,1080)
        self.show()

if __name__ == '__main__':
    hour = time.localtime().tm_hour
    min = time.localtime().tm_min
    sec = time.localtime().tm_sec
    curr_min = min + hour * 60

    while not curr_min % 18 == 0:
        curr_min += 1

    print('welcome to pyWallpaper.')
    list = get_wallpaper_label()

    while True:
        hour = time.localtime().tm_hour
        min = time.localtime().tm_min
        sec = time.localtime().tm_sec
        print('Current Time - {} :{}:{}  |  Wallpapers will be updated at - {} : {}'
              .format(hour, min, sec, curr_min // 60, curr_min - hour * 60))
        smooth_change(list)
        time.sleep(1)
