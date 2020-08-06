import argparse
import ctypes
import shutil
import time
import cv2
import os
import sys
from configparser import ConfigParser, ExtendedInterpolation

import requests
from PyQt5.QtWidgets import QApplication, QWidget, QAction, qApp, QHBoxLayout, \
    QVBoxLayout, QPushButton, QLabel, QCheckBox, QSystemTrayIcon, QMenu, QStyle, QComboBox, QDesktopWidget, QMessageBox, \
    QDialog, QProgressBar, QListView
from PyQt5.QtCore import QThread, Qt, QSize, pyqtSignal, QObject, pyqtSlot, QVariant
from PyQt5.QtGui import QPixmap, QColor, QPalette, QStandardItemModel, QStandardItem

# https://512pixels.net/projects/default-mac-wallpapers-in-5k/

# cd C:\Users\chanh\PycharmProjects\PyWallpaper

END_SIGNAL = 1

CHEETAH_PUMA = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-0_10.1.png'
JAGUAR = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-2.png'
PANTHER = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-3.png'
TIGER = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-4.png'
LEOPARD = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-5.png'
SNOW_LEOPARD = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-6.png'
LION = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-7.png'
MOUNTAIN_LION = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-8.jpg'
MAVERICKS = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-9.jpg'
YOSEMITE = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-10.jpg'
EL_CAPTAIN = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-11.jpg'
SIERRA = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-12.jpg'
HIGH_SIERRA = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-13.jpg'
MOJAVE = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-14-Mojave-'  # 16.jpg' , 1-16
CATALINA_1 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-1-Dawn.jpg'
CATALINA_2 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-2-Morning.jpg'
CATALINA_3 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-3-Day-Sunny.jpg'
CATALINA_4 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-4-Day-Overcast.jpg'
CATALINA_5 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-5-Afternoon.jpg'
CATALINA_6 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-6-Evening.jpg'
CATALINA_7 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-7-Dusk.jpg'
CATALINA_8 = 'https://ismh.s3.amazonaws.com/macos-wallpapers/10-15-8-Night.jpg'


class ConfigManager:
    def __init__(self, path):
        self.abs_path = path
        self.config = ConfigParser(interpolation=ExtendedInterpolation())

    def is_initial_execution(self):  # 처음 시작하는 경우 True를 반환
        global_path = os.path.expandvars(r'%appdata%\WKDev')
        if not os.path.exists(global_path):
            os.mkdir(global_path)

        os.chdir(global_path)

        if os.path.exists('config.ini'):
            initial_state = False
            print('최초 실행이 아님')
        else:
            print('최초 실행임')
            initial_state = True

        os.chdir(self.abs_path)
        return initial_state

    def create_ini(self):
        global_path = os.path.expandvars(r'%appdata%\WKDev')
        if not os.path.exists(global_path):
            os.mkdir(global_path)
        os.chdir(global_path)

        with open('config.ini', 'w') as c:
            print('created_config')
            config_context = '[PYWALLPAPER]\nisInitialStart = False\nCurrentWallpaperType = Catalina\n[AUTOSTART]\nisAutostart = False'
            c.write(config_context)

    def get_current_wallpaper_type(self):
        global_path = os.path.expandvars(r'%appdata%\WKDev')

        if os.path.exists(global_path):
            os.chdir(global_path)
        else:
            os.mkdir(global_path)
            os.chdir(global_path)

        if os.path.exists('config.ini'):
            self.config.read('config.ini')
            wall_type = self.config.get('PYWALLPAPER', 'CurrentWallpaperType')
        else:
            print('config dosen\'t exist')
            wall_type = None

        os.chdir(self.abs_path)
        return wall_type

    def set_current_wallpaper_type(self, wall_type):
        global_path = os.path.expandvars(r'%appdata%\WKDev')

        if os.path.exists(global_path):
            os.chdir(global_path)
        else:
            os.mkdir(global_path)
            os.chdir(global_path)

        if os.path.exists('config.ini'):
            self.config.read('config.ini')
            self.config.set('PYWALLPAPER', 'CurrentWallpaperType', wall_type)
            with open('config.ini', 'w') as c:
                self.config.write(c)
        else:
            print('config dosen\'t exist')
            wall_type = None

        os.chdir(self.abs_path)
        return wall_type

    def get_installed_wallpaper(self):
        global_path = os.path.expandvars(r'%appdata%\WKDev')
        version_list = ['10.15 Catalina', '10.14 Mojave', '10.13 High Sierra',
                        '10.12 Sierra', '10.11 El Captain', '10.10 Yosemite', '10.9  Mavericks',
                        '10.8  Mountain Lion', '10.7  Lion', '10.6  Snow Leopard', '10.5  Leopard',
                        '10.4  Tiger', '10.3  Panther', '10.2  Jaguar', '10.0  Cheetah & 10.1 Puma']

        if not os.path.exists(global_path):
            os.mkdir(global_path)

        os.chdir(global_path)

        if os.path.exists('config.ini'):
            self.config.read('config.ini')

            if not self.config.has_section('INSTALLED_WALLPAPER'):
                self.config.add_section('INSTALLED_WALLPAPER')
            options_list = self.config.options('INSTALLED_WALLPAPER')

            res = []
            for i in options_list:
                res.append(i[:].title())

            return res
            #
            # with open('config.ini', 'w') as c:
            #     self.config.write(c)
        else:
            print('config dosen\'t exist')

        os.chdir(self.abs_path)

    def set_installed_wallpaper(self, wallpaper_list):
        global_path = os.path.expandvars(r'%appdata%\WKDev')
        version_list = ['10.15 Catalina', '10.14 Mojave', '10.13 High Sierra',
                        '10.12 Sierra', '10.11 El Captain', '10.10 Yosemite', '10.9  Mavericks',
                        '10.8  Mountain Lion', '10.7  Lion', '10.6  Snow Leopard', '10.5  Leopard',
                        '10.4  Tiger', '10.3  Panther', '10.2  Jaguar', '10.0  Cheetah & 10.1 Puma']

        if not os.path.exists(global_path):
            os.mkdir(global_path)

        os.chdir(global_path)

        if os.path.exists('config.ini'):
            self.config.read('config.ini')

            if not self.config.has_section('INSTALLED_WALLPAPER'):
                self.config.add_section('INSTALLED_WALLPAPER')

            for wallpaper in wallpaper_list:
                self.config.set('INSTALLED_WALLPAPER', str(wallpaper[2]), 'True')

            with open('config.ini', 'w') as c:
                self.config.write(c)
        else:
            print('config dosen\'t exist')

        os.chdir(self.abs_path)

    def getAutostart(self):
        global_path = os.path.expandvars(r'%appdata%\WKDev')
        #
        # if not os.path.exists(global_path):
        #     os.mkdir(global_path)
        os.chdir(global_path)

        if os.path.exists('config.ini'):
            if self.config.has_section('AUTOSTART'):
                self.config.read('config.ini')
                state = self.config.get('AUTOSTART', 'isAutostart')
                print('state is ' + state)
                return state
            else:
                # self.config.add_section('AUTOSTART')
                # self.config.set('AUTOSTART', 'isAutostart', 'False')
                # with open('config.ini', 'w') as c:
                #     self.config.write(c)
                print('in autostart, couldnt find config file')
                return 'False'

        os.chdir(self.abs_path)

    def setAutostart(self, state):
        location = r'%appdata%\Microsoft\Windows\Start Menu\Programs\Startup'
        launcher_location = os.path.expandvars(location) + r'\launcher.bat'
        global_path = os.path.expandvars(r'%appdata%\WKDev')

        # if not os.path.exists(global_path):
        #     os.mkdir(global_path)
        os.chdir(global_path)

        if os.path.exists('config.ini'):
            if state:
                str_state = 'True'
            else:
                str_state = 'False'

            if self.config.has_section('AUTOSTART'):
                self.config.set('AUTOSTART', 'isautostart', str_state)
                with open('config.ini', 'w') as c:
                    self.config.write(c)

        if state == Qt.Checked or state == 'True':
            os.chdir(self.abs_path)
            with open('launcher.bat', 'w') as f:
                f.write('cd ' + os.getcwd() + '\n')
                f.write('start pythonw pywallpaper.py')
            shutil.move('launcher.bat', launcher_location)

        else:
            if os.path.isfile(launcher_location):
                os.remove(launcher_location)
                print('startup_file removed')

        os.chdir(self.abs_path)


class Main:
    def __init__(self, abs_path):
        super().__init__()
        self.abs_path = abs_path
        self.wallpaper_list = []
        self.current_picture = ''
        self.previous_picture = ''
        self.image_location = []
        self.wallpaper_path = ''
        self.mix = 0
        self.config = []

        self.last_update_hour = None
        self.last_update_min = None

    # 파일이 존재하는 위치에서 배경화면 파일 리스트 불러오기
    def get_wallpaper_label(self, wallpaper_version):
        os.chdir(self.abs_path)
        # print(self.os_abs_path)
        if wallpaper_version == 'Catalina': self.wallpaper_list = os.listdir(self.abs_path + '\\wallpaper\\Catalina')
        if wallpaper_version == 'Mojave':
            self.wallpaper_list.clear()
            ls = os.listdir(self.abs_path + '\\wallpaper\\Mojave')
            for i in range(1, 17):
                # print('fetching Mojave wallpapers from directory')
                self.wallpaper_list.append('10-14-Mojave-' + str(i) + '.jpg')

    # 다음에 변경될 시간 제공하는 함수
    def get_next_change_time(self, wall_type):
        if self.last_update_hour == None or self.last_update_min == None:
            t = time.localtime()
            curr_min = t.tm_hour + 60 + t.tm_min

            if wall_type == 'Catalina':
                while not curr_min % 18 == 0:
                    curr_min += 1

            if wall_type == 'Mojave':
                while not curr_min % 18 == 0:
                    curr_min += 1

            next_hour = t.tm_hour
            next_min = curr_min - t.tm_hour * 60

            return next_hour, next_min

        if wall_type == 'Catalina':
            next_hour = self.last_update_hour
            next_min = self.last_update_min + 18

        elif wall_type == 'Mojave':
            next_hour = self.last_update_hour
            next_min = self.last_update_min + 9

        else:
            next_hour = 0
            next_min = 0

        if next_min >= 60:
            next_hour += 1
            next_min -= 60

        if next_hour == 24:
            next_hour = 0

        return next_hour, next_min

    # 현재 배경화면과 비율 제공하는 함수
    def get_wallpaper_info(self):
        return self.current_picture, self.previous_picture, self.mix

    def wallpaper_selector(self, wallpaper_type, initial_apply=False):
        if wallpaper_type is not None:
            version_list = {'10.15 Catalina': 'Catalina', '10.14 Mojave': 'Mojave', '10.13 High Sierra': '10-13.jpg',
                            '10.12 Sierra': '10-12.jpg', '10.11 El Captain': '10-11.jpg', '10.10 Yosemite': '10-10.jpg',
                            '10.9  Mavericks': '10-9.jpg',
                            '10.8  Mountain Lion': '10-8.jpg', '10.7  Lion': '10-7.png',
                            '10.6  Snow Leopard': '10-6.png',
                            '10.5  Leopard': '10-5.png',
                            '10.4  Tiger': '10-4.png', '10.3  Panther': '10-3.png', '10.2  Jaguar': '10-2.png',
                            '10.0  Cheetah & 10.1 Puma': '10-0_10.1.png'}

            if wallpaper_type == 'Catalina':
                self.change_background_catalina(initial_apply)
            elif wallpaper_type == 'Mojave':
                self.change_background_mojave(initial_apply)
            else:
                self.apply_wallpaper(wallpaper_type, version_list[wallpaper_type])

    # 사진 불러오고 합성하는 핵심 기능 담겨있음
    def change_background_catalina(self, initial_apply=False):

        self.get_wallpaper_label('Catalina')

        hour = time.localtime().tm_hour
        min = time.localtime().tm_min
        sec = time.localtime().tm_sec
        elasped = min + hour * 60

        if initial_apply:
            os.chdir(self.abs_path)  # 다 다운로드 받지 못했을 때도 고려해야함
            self.mix = round((elasped - (hour // 3) * 180) * 10 / 18, 2)
            self.current_picture = self.wallpaper_list[(hour // 3)][:-4]
            self.previous_picture = self.wallpaper_list[(hour // 3) - 1][:-4]
            print(
                '즉시 변경 : time {}:{},  elasped :{}   cur : {} {}%, prev :{} {}%'
                    .format(hour, min, elasped, self.current_picture, self.mix, self.previous_picture,
                            (100 - self.mix)))

            cur_pic_path = self.abs_path + '\\wallpaper\\Catalina\\' + self.current_picture + '.jpg'
            prev_pic_path = self.abs_path + '\\wallpaper\\Catalina\\' + self.previous_picture + '.jpg'
            cur_pic = cv2.imread(cur_pic_path)
            prev_pic = cv2.imread(prev_pic_path)
            weighted_img = cv2.addWeighted(cur_pic, float(self.mix) / 100, prev_pic, float(100 - self.mix) / 100, 0)

            # 이미지를 저장합니다.
            os.chdir(self.abs_path)
            os.chdir('./wallpaper')
            cv2.imwrite('catalina_processed.jpg', weighted_img)
            self.apply_wallpaper('Catalina', r'\catalina_processed.jpg')
            os.chdir('../')
            initial_apply = False

        # image_amount = 8, wallpapers are changed every 3 hours(180min)
        # when resolution is 10, image_amount = 8, wallpapers are changed every 18min

        os.chdir(self.abs_path)
        # pc 자원 소모를 최소화하기 위해 실제로 이미지들이 쓰이는 cur_pic과 prev_pic을 3시간 단위로 불러옵니다.
        if hour % 3 == 0 and min == 0 and sec < 20:
            self.current_picture = self.wallpaper_list[(hour // 3)][:-4]
            self.previous_picture = self.wallpaper_list[(hour // 3) - 1][:-4]
            cur_pic_path = self.abs_path + '\\wallpaper\\Catalina\\' + self.current_picture + '.jpg'
            prev_pic_path = self.abs_path + '\\wallpaper\\Catalina\\' + self.previous_picture + '.jpg'
            cur_pic = cv2.imread(cur_pic_path)
            prev_pic = cv2.imread(prev_pic_path)

        # 매 18분 마다 이미지의 비율을 확인하고 변경합니다.
        if (elasped % 18 == 0) and sec < 5:
            self.last_update_hour = hour
            self.last_update_min = min
            self.mix = (elasped - (hour // 3) * 180) * 10 / 18
            # print(elasped, mix)
            print('배경화면을 변경합니다. time {}:{},  elasped :{}   cur : {} {}%, prev :{} {}%'
                  .format(hour, min, elasped, self.current_picture, int(self.mix), self.previous_picture,
                          int(100 - self.mix)))

            # 시간 경과에 따라 이미지 합성을 수행합니다. 이전에 이미지를 불러온 적이 없다면 이미지를 불러온 후 합성을 수행합니다.
            try:
                weighted_img = cv2.addWeighted(cur_pic, float(self.mix) / 100, prev_pic, float(100 - self.mix) / 100, 0)
            except:
                print('배경화면이 불러와져 있지않아 불러온 후 이미지를 처리합니다.')
                self.current_picture = self.wallpaper_list[(hour // 3)][:-4]
                self.previous_picture = self.wallpaper_list[(hour // 3) - 1][:-4]
                cur_pic_path = self.abs_path + '\\wallpaper\\Catalina\\' + self.current_picture + '.jpg'
                prev_pic_path = self.abs_path + '\\wallpaper\\Catalina\\' + self.previous_picture + '.jpg'
                cur_pic = cv2.imread(cur_pic_path)
                prev_pic = cv2.imread(prev_pic_path)
                weighted_img = cv2.addWeighted(cur_pic, float(self.mix) / 100, prev_pic, float(100 - self.mix) / 100, 0)

            # 이미지를 저장합니다.
            os.chdir('./wallpaper')
            t1 = time.time()
            cv2.imwrite('catalina_processed.jpg', weighted_img)
            t2 = time.time()
            self.apply_wallpaper('Catalina', r'\catalina_processed.jpg')
            os.chdir('../')

    def change_background_mojave(self, initial_apply=False):
        os.chdir(self.abs_path)
        self.get_wallpaper_label('Mojave')

        hour = time.localtime().tm_hour
        min = time.localtime().tm_min
        sec = time.localtime().tm_sec
        elasped = min + hour * 60

        image_amount = 16
        change_term = 24 / image_amount  # images are changed every 'change_term'

        # print(self.wallpaper_list)

        if initial_apply:
            self.mix = round((elasped - (hour / 1.5) * 90) * (10 / 9), 2)

            self.current_picture = self.wallpaper_list[int(hour // change_term) - 1][:-4]
            self.previous_picture = self.wallpaper_list[int(hour // change_term) - 2][:-4]
            print(
                '즉시 변경 : time {}:{},  elasped :{}   cur : {} {}%, prev :{} {}%'
                    .format(hour, min, elasped, self.current_picture, self.mix, self.previous_picture,
                            (100 - self.mix)))

            # print(self.os_abs_path)
            cur_pic_path = self.abs_path + '\\wallpaper\\Mojave\\' + self.current_picture + '.jpg'
            prev_pic_path = self.abs_path + '\\wallpaper\\Mojave\\' + self.previous_picture + '.jpg'
            cur_pic = cv2.imread(cur_pic_path)
            prev_pic = cv2.imread(prev_pic_path)

            weighted_img = cv2.addWeighted(cur_pic, float(self.mix) / 100, prev_pic, float(100 - self.mix) / 100, 0)

            os.chdir(self.abs_path)
            os.chdir('./wallpaper')
            t1 = time.time()
            cv2.imwrite('mojave_processed.jpg', weighted_img)
            t2 = time.time()
            self.apply_wallpaper('Mojave', r'\mojave_processed.jpg')

            # 이미지를 저장합니다.

            initial_apply = False

        # image_amount = 16, wallpapers are changed every 90min
        # when resolution is 9, image_amount = 16, wallpapers are changed every 9min

        # pc 자원 소모를 최소화하기 위해 실제로 이미지들이 쓰이는 cur_pic과 prev_pic을 1시간 단위로 불러옵니다.
        if min == 0 and sec < 10:
            os.chdir(self.abs_path)
            self.current_picture = self.wallpaper_list[int(hour // change_term)]
            self.previous_picture = self.wallpaper_list[int(hour // change_term)]
            cur_pic_path = os.getcwd() + '\\wallpaper\\Mojave\\' + self.current_picture + '.jpg'
            prev_pic_path = os.getcwd() + '\\wallpaper\\Mojave\\' + self.previous_picture + '.jpg'
            cur_pic = cv2.imread(cur_pic_path)
            prev_pic = cv2.imread(prev_pic_path)

        # 매 9분 마다 이미지의 비율을 확인하고 변경합니다.
        if (elasped % 9 == 0) and sec < 5:
            self.last_update_hour = hour
            self.last_update_min = min
            os.chdir(self.abs_path)
            self.mix = round((elasped - (hour / 1.5) * 90) * (10 / 9), 2)
            # print(elasped, mix)
            print('지정 시간 도래에 따른 변경: time {}:{},  elasped :{}   cur : {} {}%, prev :{} {}%'
                  .format(hour, min, elasped, self.current_picture, int(self.mix), self.previous_picture,
                          int(100 - self.mix)))

            # 시간 경과에 따라 이미지 합성을 수행합니다. 이전에 이미지를 불러온 적이 없다면 이미지를 불러온 후 합성을 수행합니다.

            self.current_picture = self.wallpaper_list[int(hour // change_term) - 1][:-4]
            self.previous_picture = self.wallpaper_list[int(hour // change_term) - 2][:-4]
            cur_pic_path = self.abs_path + '\\wallpaper\\Mojave\\' + self.current_picture + '.jpg'
            prev_pic_path = self.abs_path + '\\wallpaper\\Mojave\\' + self.previous_picture + '.jpg'
            cur_pic = cv2.imread(cur_pic_path)
            prev_pic = cv2.imread(prev_pic_path)
            weighted_img = cv2.addWeighted(cur_pic, float(self.mix) / 100, prev_pic, float(100 - self.mix) / 100, 0)

            os.chdir(self.abs_path)
            os.chdir('./wallpaper')
            t1 = time.time()
            cv2.imwrite('mojave_processed.jpg', weighted_img)
            t2 = time.time()
            self.apply_wallpaper('Mojave', r'\mojave_processed.jpg')

    # 합성한 이미지를 배경화면으로 설정합니다.
    def apply_wallpaper(self, wall_type, title):
        os.chdir(self.abs_path)
        os.chdir('./wallpaper')

        if wall_type == 'Catalina' or wall_type == 'Mojave':
            self.wallpaper_path = os.getcwd() + title
            ctypes.windll.user32.SystemParametersInfoW(0x14, 0, self.wallpaper_path, 0x3)  # SystemParametersInfoA

        else:
            print('apply_wallpaper : ' + title)
            self.wallpaper_path = os.getcwd() + '\\' + title
            self.init_wallpaper = False
            ctypes.windll.user32.SystemParametersInfoW(0x14, 0, self.wallpaper_path, 0x3)  # SystemParametersInfoA


class ImgDownloadGui(QWidget):
    def __init__(self, path):
        super().__init__()
        self.abs_path = path
        self.config = ConfigManager(self.abs_path)
        self.img_list = []
        self.init_list()
        self.init_ui()
        self.img_thread = None

    def init_list(self):

        # self.name = name
        # self.icon = icon
        self.model = QStandardItemModel()
        self.listView = QListView()

        version_list = ['10.15 Catalina', '10.14 Mojave', '10.13 High Sierra',
                        '10.12 Sierra', '10.11 El Captain', '10.10 Yosemite', '10.9  Mavericks',
                        '10.8  Mountain Lion', '10.7  Lion', '10.6  Snow Leopard', '10.5  Leopard',
                        '10.4  Tiger', '10.3  Panther', '10.2  Jaguar', '10.0  Cheetah & 10.1 Puma']

        installed_list = self.config.get_installed_wallpaper()

        # s = set(installed_list)
        # avaliable_list = [x for x in version_list if x not in s]

        checked = False
        if version_list is not None:
            for i in range(len(version_list)):
                item = QStandardItem(version_list[i])
                item.setCheckable(True)
                # if version_list[i] in installed_list:
                #     item.setCheckState(True)

                check = Qt.Checked if checked else Qt.Unchecked
                item.setCheckState(check)
                self.model.appendRow(item)

        self.listView.setModel(self.model)

        self.installed_model = QStandardItemModel()
        self.installed_listView = QListView()

        if installed_list is not None:
            for i in range(len(installed_list)):
                item = QStandardItem(installed_list[i])
                item.setCheckable(False)
                check = Qt.Checked if checked else Qt.Unchecked
                item.setCheckState(check)
                self.installed_model.appendRow(item)
        self.installed_listView.setModel(self.installed_model)

    def init_ui(self):
        # text
        info_text = QLabel(
            'Thank you for using PyWallpaper. \n before using Application,\n you need to download wallpaper.')
        info_text.setAlignment(Qt.AlignCenter)

        family_font = self.font()
        family_font.setPointSize(12)
        family_font.setFamily('AppleSDGothicNeoUL00')
        self.setFont(family_font)

        # info_font = info_text.font()
        # info_font.setPointSize(14)
        # info_text.setFont(info_font)

        # pushbutton
        btn_download_all = QPushButton('Select All')
        self.btn_download = QPushButton('Download')
        btn_cancel = QPushButton('Cancel')
        btn_download_all.clicked.connect(self.on_download_all_click)
        self.btn_download.clicked.connect(self.on_download_click)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_download)
        hbox.addWidget(btn_cancel)

        vbox = QVBoxLayout()
        vbox.addWidget(info_text)
        vbox.addWidget(self.listView)
        # vbox.addWidget(self.installed_listView)
        vbox.addWidget(btn_download_all)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setMinimumSize(QSize(400, 500))  # 사이즈 설정
        self.setMaximumSize(QSize(400, 800))  # 사이즈 설정
        self.setWindowTitle('PyWallpaper - DownloadImage')  # 타이틀 설정

    # 필요한 이미지의 리스트를 생성해 스레드에 전달
    def on_download_click(self):
        # while self.model.item(i):
        # if self.model.item(i).checkState():
        #     self.img_list.append(self.model.item(i).text())
        if self.model.item(0).checkState():
            self.img_list.append([CATALINA_1, '10-15-1-Dawn.jpg', self.model.item(0).text()])
            self.img_list.append([CATALINA_2, '10-15-2-Morning.jpg', self.model.item(0).text()])
            self.img_list.append([CATALINA_3, '10-15-3-Day-Sunny.jpg', self.model.item(0).text()])
            self.img_list.append([CATALINA_4, '10-15-4-Day-Overcast.jpg', self.model.item(0).text()])
            self.img_list.append([CATALINA_5, '10-15-5-Afternoon.jpg', self.model.item(0).text()])
            self.img_list.append([CATALINA_6, '10-15-6-Evening.jpg', self.model.item(0).text()])
            self.img_list.append([CATALINA_7, '10-15-7-Dusk.jpg', self.model.item(0).text()])
            self.img_list.append([CATALINA_8, '10-15-8-Night.jpg', self.model.item(0).text()])
            print('append 8 ')
        if self.model.item(1).checkState():
            self.img_list.append([MOJAVE + str(1) + '.jpg', '10-14-11-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(2) + '.jpg', '10-14-1-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(3) + '.jpg', '10-14-2-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(4) + '.jpg', '10-14-3-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(5) + '.jpg', '10-14-4-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(6) + '.jpg', '10-14-5-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(7) + '.jpg', '10-14-6-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(8) + '.jpg', '10-14-7-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(9) + '.jpg', '10-14-8-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(10) + '.jpg', '10-14-9-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(11) + '.jpg', '10-14-10-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(12) + '.jpg', '10-14-12-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(13) + '.jpg', '10-14-13-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(14) + '.jpg', '10-14-14-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(15) + '.jpg', '10-14-15-Mojave.jpg', self.model.item(1).text()])
            self.img_list.append([MOJAVE + str(16) + '.jpg', '10-14-16-Mojave.jpg', self.model.item(1).text()])

        if self.model.item(2).checkState():
            self.img_list.append([HIGH_SIERRA, '10-13.jpg', self.model.item(2).text()])
        if self.model.item(3).checkState():
            self.img_list.append([SIERRA, '10-12.jpg', self.model.item(3).text()])
        if self.model.item(4).checkState():
            self.img_list.append([EL_CAPTAIN, '10-11.jpg', self.model.item(4).text()])
        if self.model.item(5).checkState():
            self.img_list.append([YOSEMITE, '10-10.jpg', self.model.item(5).text()])
        if self.model.item(6).checkState():
            self.img_list.append([MAVERICKS, '10-9.jpg', self.model.item(6).text()])
        if self.model.item(7).checkState():
            self.img_list.append([MOUNTAIN_LION, '10-8.jpg', self.model.item(7).text()])
        if self.model.item(8).checkState():
            self.img_list.append([LION, '10-7.png', self.model.item(8).text()])
        if self.model.item(9).checkState():
            self.img_list.append([SNOW_LEOPARD, '10-6.png', self.model.item(9).text()])
        if self.model.item(10).checkState():
            self.img_list.append([LEOPARD, '10-5.png', self.model.item(10).text()])
        if self.model.item(11).checkState():
            self.img_list.append([TIGER, '10-4.png', self.model.item(11).text()])
        if self.model.item(12).checkState():
            self.img_list.append([PANTHER, '10-3.png', self.model.item(12).text()])
        if self.model.item(13).checkState():
            self.img_list.append([JAGUAR, '10-2.png', self.model.item(13).text()])
        if self.model.item(14).checkState():
            self.img_list.append([CHEETAH_PUMA, '10-1.png', self.model.item(14).text()])
        #
        # i = 0
        # while self.model.item(i):
        #     if self.model.item(i).text() == '10.15 Catalina':
        #         self.img_list.append([CATALINA_1, '10-15-1-Dawn.jpg',self.model.item(0).text()])
        #         self.img_list.append([CATALINA_2, '10-15-2-Morning.jpg',self.model.item(0).text()])
        #         self.img_list.append([CATALINA_3, '10-15-3-Day-Sunny.jpg',self.model.item(0).text()])
        #         self.img_list.append([CATALINA_4, '10-15-4-Day-Overcast.jpg',self.model.item(0).text()])
        #         self.img_list.append([CATALINA_5, '10-15-5-Afternoon.jpg',self.model.item(0).text()])
        #         self.img_list.append([CATALINA_6, '10-15-6-Evening.jpg',self.model.item(0).text()])
        #         self.img_list.append([CATALINA_7, '10-15-7-Dusk.jpg',self.model.item(0).text()])
        #         self.img_list.append([CATALINA_8, '10-15-8-Night.jpg',self.model.item(0).text()])
        #     if self.model.item(i).text() == '10.14 Mojave':
        #         self.img_list.append([MOJAVE + str(1) + '.jpg', '10-14-11-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(2) + '.jpg', '10-14-1-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(3) + '.jpg', '10-14-2-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(4) + '.jpg', '10-14-3-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(5) + '.jpg', '10-14-4-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(6) + '.jpg', '10-14-5-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(7) + '.jpg', '10-14-6-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(8) + '.jpg', '10-14-7-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(9) + '.jpg', '10-14-8-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(10) + '.jpg', '10-14-9-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(11) + '.jpg', '10-14-10-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(12) + '.jpg', '10-14-12-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(13) + '.jpg', '10-14-13-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(14) + '.jpg', '10-14-14-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(15) + '.jpg', '10-14-15-Mojave.jpg',self.model.item(1).text()])
        #         self.img_list.append([MOJAVE + str(16) + '.jpg', '10-14-16-Mojave.jpg',self.model.item(1).text()])
        #
        #     if self.model.item(i).text() == '10.13 High Sierra':
        #         self.img_list.append([HIGH_SIERRA, '10-13.jpg',self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.12 Sierra':
        #         self.img_list.append([SIERRA, '10-12.jpg', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.11 El Captain':
        #         self.img_list.append([EL_CAPTAIN, '10-11.jpg', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.10 Yosemite':
        #         self.img_list.append([YOSEMITE, '10-10.jpg', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.9  Mavericks':
        #         self.img_list.append([MAVERICKS, '10-9.jpg', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.8  Mountain Lion':
        #         self.img_list.append([MOUNTAIN_LION, '10-8.jpg', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.7  Lion':
        #         self.img_list.append([LION, '10-7.png', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.6  Snow Leopard':
        #         self.img_list.append([SNOW_LEOPARD, '10-6.png', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.5  Leopard':
        #         self.img_list.append([LEOPARD, '10-5.png', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.4  Tiger':
        #         self.img_list.append([TIGER, '10-4.png', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.3  Panther':
        #         self.img_list.append([PANTHER, '10-3.png', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.2  Jaguar':
        #         self.img_list.append([JAGUAR, '10-2.png', self.model.item(i).text()])
        #     if self.model.item(i).text() == '10.0  Cheetah & 10.1 Puma':
        #         self.img_list.append([CHEETAH_PUMA, '10-1.png', self.model.item(i).text()])

        self.config.set_installed_wallpaper(self.img_list)
        print(self.img_list)

    def on_download_all_click(self):
        i = 0
        while self.model.item(i):
            item = self.model.item(i)
            if not item.checkState():
                item.setCheckState(Qt.Checked)
            i += 1

    def closeEvent(self, event):
        self.hide()


class DownloadProgressGui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.selected_img_amount = None

    def init_ui(self):
        # text
        info_text = QLabel(
            'Downloading Wallpaper...')
        info_text.setAlignment(Qt.AlignCenter)

        family_font = self.font()
        family_font.setPointSize(12)
        family_font.setFamily('AppleSDGothicNeoUL00')
        self.setFont(family_font)

        # text
        self.curr_file_text = QLabel('Waiting for Server Response...')
        self.curr_file_text.setAlignment(Qt.AlignRight)
        self.total_file_text = QLabel('0 / 0 Downloaded')
        self.total_file_text.setAlignment(Qt.AlignRight)

        # progressBar : for separate item
        self.progress_bar = QProgressBar()
        # progressBar : display whole progress
        self.total_progress_bar = QProgressBar()

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(info_text)
        vbox.addStretch(1)
        vbox.addWidget(self.curr_file_text)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.total_file_text)
        vbox.addWidget(self.total_progress_bar)
        self.setLayout(vbox)

        self.setMinimumSize(QSize(600, 250))  # 사이즈 설정
        self.setMaximumSize(QSize(600, 250))  # 사이즈 설정
        self.setWindowTitle('PyWallpaper - Download in Progress')  # 타이틀 설정

    def closeEvent(self, event):
        sys.exit(0)

    def set_total_image_amount(self, list_size):
        self.selected_img_amount = list_size

    @pyqtSlot(int)  # 스레드에서 시그널 받아 프로그레스바에 표현
    def set_curr_file_percentage(self, status):
        self.progress_bar.setValue(status)

    def set_total_file_count(self, status):
        self.total_file_text.setText('{} / {} Downloaded'.format(status, self.selected_img_amount))
        self.total_progress_bar.setValue((status / self.selected_img_amount) * 100)

    @pyqtSlot(str)
    def set_file_label(self, status):
        self.curr_file_text.setText(status)


# 이미지를 다운로드 받는 스레드
class ImgDownloadThread(QObject):
    # custom_signal 생성
    end_signal = pyqtSignal(int)
    curr_percentage = pyqtSignal(int)
    img_count = pyqtSignal(int)
    img_title_signal = pyqtSignal(str)

    def __init__(self, path, download_list, parent=None):
        super(self.__class__, self).__init__(parent)
        self.abs_path = path
        self.download_list = download_list

    @pyqtSlot()  # 버튼 클릭시 시그널을 받아들이는 슬롯 제작
    def run(self):
        i = 0
        # wallpaper 폴더가 없으면 생성
        print(os.getcwd())
        os.chdir(self.abs_path)
        if not os.path.exists('./wallpaper'):
            os.mkdir('wallpaper')
        os.chdir('./wallpaper')

        inv_version = {'10-13.jpg': '10.13 High Sierra', '10-3.png': '10.3  Panther', '10-11.jpg': '10.11 El Captain',
                       '10-7.png': '10.7  Lion', '10-0_10.1.png': '10.0  Cheetah & 10.1 Puma',
                       '10-10.jpg': '10.10 Yosemite',
                       '10-6.png': '10.6  Snow Leopard', '10-8.jpg': '10.8  Mountain Lion', '10-2.png': '10.2  Jaguar',
                       '10-9.jpg': '10.9  Mavericks', '10-12.jpg': '10.12 Sierra', 'Catalina': '10.15 Catalina',
                       'Mojave': '10.14 Mojave', '10-5.png': '10.5  Leopard', '10-4.png': '10.4  Tiger'}

        for img_attribute in self.download_list:
            self.img_count.emit(i)
            self.img_title_signal.emit(img_attribute[1])
            if img_attribute[1].startswith('10-15'):
                print('found Catalina item')
                if not os.path.exists('./Catalina'):
                    print('Catalina 경로가 없어 새로 생성합니다.')
                    os.mkdir('Catalina')
                os.chdir('./Catalina')
                self.download_img_from_url(img_attribute[0], img_attribute[1])
                os.chdir('../')

            elif img_attribute[1].startswith('10-14'):
                print('found Mojave item')
                if not os.path.exists('./Mojave'):
                    print('Mojave 경로가 없어 새로 생성합니다.')
                    os.mkdir('Mojave')
                os.chdir('./Mojave')
                self.download_img_from_url(img_attribute[0], img_attribute[1])
                os.chdir('../')

            else:
                print('downloading   ' + img_attribute[1] + ' from ' + img_attribute[0])
                self.download_img_from_url(img_attribute[0], img_attribute[1])
            i += 1
        print('download_finished')
        self.img_count.emit(i)
        self.end_signal.emit(END_SIGNAL)

    def download_img_from_url(self, url, filename):
        with open(filename, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                chunk_size = max(int(total / 1500), 1024)
                # print('total : {} chunk size : {}'.format(total, chunk_size))
                for data in response.iter_content(chunk_size=chunk_size):
                    downloaded += len(data)
                    f.write(data)
                    curr_file_percentage = int(100 * downloaded / total)
                    self.curr_percentage.emit(curr_file_percentage)
                    # print('\r{} %  downloaded'.format(done))


class MainQLogic(QObject):
    def __init__(self, parent=None, location=None, is_called_from_main=False):
        super(self.__class__, self).__init__(parent)
        self.abs_path = location
        self.config = ConfigManager(self.abs_path)

        is_initial_start = self.config.is_initial_execution()

        parser = argparse.ArgumentParser(description='Pywallpaper')
        parser.add_argument('-m', '--start_minimized', default=False, help='it determines application to show gui when startup.')
        args = parser.parse_args()

        # gui 설정
        self.download_gui = ImgDownloadGui(self.abs_path)
        self.progress_gui = DownloadProgressGui()
        self.main_gui = MainGui(self.abs_path)

        img_list = self.download_gui.img_list
        self.img_worker = ImgDownloadThread(self.abs_path, img_list)  # 백그라운드에서 돌아갈 인스턴스 소환
        self.img_worker_thread = QThread()  # 따로 돌아갈 스레드를 하나 생성
        self.img_worker.moveToThread(self.img_worker_thread)  # img_worker를 만들어둔 스레드에 넣어줌
        self.img_worker_thread.start()

        self.main_worker = MainThread(self.abs_path)
        self.main_worker_thread = QThread()
        self.main_worker.moveToThread(self.main_worker_thread)
        self.main_worker_thread.start()

        self._connectSignals()  # 시그널을 연결하기 위한 함수 호출

        if is_initial_start or not is_called_from_main:
            self.config.create_ini()
            os.chdir(self.abs_path)
            self.download_gui.show()
        else:
            self.main_worker.start()
            print(args.start_minimized)
            if not args.start_minimized:
                self.main_gui.show()

    # 시그널을 연결하기 위한 함수
    def _connectSignals(self):
        # gui 버튼 클릭 시 연결 설정
        self.download_gui.btn_download.clicked.connect(self.img_worker.run)
        self.download_gui.btn_download.clicked.connect(self.download_gui.hide)
        self.download_gui.btn_download.clicked.connect(self.progress_gui.show)
        self.download_gui.btn_download.clicked.connect(self.parse_download_state_to_gui)

        # 메인스레드에 요청할 작업 수행
        self.main_gui.get_wallpaper_signal.connect(self.inflate_download_gui)
        self.main_gui.btn_manage_wallpaper.clicked.connect(self.terminate_img_down_thread)

        # img_worker에서 발생한 end_signal의 연결 설정
        self.img_worker.end_signal.connect(self.on_finished_download)
        self.img_worker.curr_percentage.connect(self.progress_gui.set_curr_file_percentage)
        self.img_worker.img_count.connect(self.progress_gui.set_total_file_count)
        self.img_worker.img_title_signal.connect(self.progress_gui.set_file_label)

        # gui - thread 시그널 연결하기
        self.main_worker.time_signal.connect(self.main_gui.setCurrTime)
        self.main_worker.next_time_signal.connect(self.main_gui.setNextTime)
        self.main_worker.wallpaper_info_sig.connect(self.main_gui.setWallpaperInfo)
        self.main_worker.apply_gui_signal.connect(self.main_gui.init_image)

        # cancel버튼 연결 설정
        # self.gui.button_cancel.clicked.connect(self.forceWorkerReset)

        # 스레드의 루프를 중단하고 다시 처음으로 대기시키는 함수
        # def forceWorkerReset(self):
        #     if self.worker_thread.isRunning():  #쓰레드가돌아가고있다면
        #     self.worker_thread.terminate() #현재돌아가는thread를중지시킨다
        #     self.worker_thread.wait() # 새롭게thread를대기한후
        #     self.worker_thread.start() # 다시처음부터시작

        # ** 소소한 Tip**
        # 이것을 하다가 보면 쓰레드를 종료할수 있는 코드가 중요합니다.
        # 진행중인 코드에서 쓰레드의 작동을 감지한후 (isRunning()) => 작동한다면 종료(.terminate()) =>
        # thread를 유지, 대기한후( wait()) => 이 쓰레드를 다시 처음으로 돌린다( start())
        # 이 코드는 많이들 이용하는 코드 이더군요...

    def parse_download_state_to_gui(self):
        img_list = self.download_gui.img_list
        self.progress_gui.set_total_image_amount(list_size=len(img_list))

    def on_finished_download(self):
        self.progress_gui.hide()
        self.main_worker.start()
        self.main_gui.show()

    @pyqtSlot(str)
    def inflate_download_gui(self, event):
        print('inflate_download_gui')
        self.download_gui.show()

    def terminate_img_down_thread(self):
        if self.img_worker_thread.isRunning():  # 쓰레드가돌아가고있다면
            self.img_worker_thread.terminate()  # 현재돌아가는thread를중지시킨다
            self.img_worker_thread.wait() # 새롭게thread를대기한후
            self.img_worker_thread.start() # 다시처음부터시작


class MainGui(QDialog):
    get_wallpaper_signal = pyqtSignal(str)

    def __init__(self, path):
        super().__init__()
        self.abs_path = path
        self.config = ConfigManager(self.abs_path)
        self.wallpaper_type = self.config.get_current_wallpaper_type()
        self.init_image()
        self.initUI()
        self.initTray()
        self.main_app = Main(self.abs_path)
        self.prev_chked_item = '10.15 Catalina'

    def init_image(self):
        # Image
        self.wallpaper_type = self.config.get_current_wallpaper_type()
        self.image_label = QLabel()
        os.chdir(self.abs_path)
        if os.path.exists('./wallpaper'):
            os.chdir('./wallpaper')

        if self.wallpaper_type == 'Catalina' and os.path.exists('catalina_processed.jpg'):
            image = cv2.imread('catalina_processed.jpg', cv2.IMREAD_COLOR)
            resize = cv2.resize(image, (3008, 3008), cv2.INTER_AREA)
            width = 100
            height = 800
            processed = resize[height:height + 500, width:width + 1500]
        elif self.wallpaper_type == 'Mojave' and os.path.exists('mojave_processed.jpg'):
            image = cv2.imread('mojave_processed.jpg', cv2.IMREAD_COLOR)
            resize = cv2.resize(image, (3008, 3008), cv2.INTER_AREA)
            width = 50
            height = 950
            processed = resize[height:height + 600, width:width + 1800]
        else:
            print('there\'s no dynamic wallpaper')
            pass

        try:
            cv2.imwrite('title_img.png', processed)
            pixmap = QPixmap('title_img.png')
            pixmap = pixmap.scaled(750, 250, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
        except:
            pass

    def initUI(self):
        # text
        self.txt_curr_time = QLabel('time')
        self.txt_curr_time.setAlignment(Qt.AlignLeft)
        self.txt_prev_time = QLabel('next_time')
        self.txt_prev_time.setAlignment(Qt.AlignRight)
        self.txt_wallpaper_info = QLabel('wallpaper')
        os_version = QLabel('set os version : ')

        self.txt_wallpaper_info.setAlignment(Qt.AlignCenter)

        # Text
        title_text = QLabel('PyWallpaper', self)
        desc_text = QLabel('An Application that helps apply iMac wallpaper \nfor 4k+ Monitor with Windows')
        title_text.setAlignment(Qt.AlignCenter)
        desc_text.setAlignment(Qt.AlignCenter)

        version_list = ['10.15 Catalina', '10.14 Mojave', '10.13 High Sierra',
                        '10.12 Sierra', '10.11 El Captain', '10.10 Yosemite', '10.9  Mavericks',
                        '10.8  Mountain Lion', '10.7  Lion', '10.6  Snow Leopard', '10.5  Leopard',
                        '10.4  Tiger', '10.3  Panther', '10.2  Jaguar', '10.0  Cheetah & 10.1 Puma']

        # ComboBox & button
        self.cb_select_version = QComboBox(self)
        self.cb_select_version.addItems(version_list)
        self.cb_select_version.activated[str].connect(self.on_version_chkbox_changed)
        self.btn_manage_wallpaper = QPushButton('Manage Wallpaper')
        self.btn_manage_wallpaper.clicked.connect(self.onManageBtnClicked)

        if self.wallpaper_type == 'Catalina':
            self.cb_select_version.setCurrentIndex(0)
        elif self.wallpaper_type == 'Mojave':
            self.cb_select_version.setCurrentIndex(1)
        elif self.wallpaper_type == None:
            print('in maingui, wallpaper_type is none')
            # self.cb_select_version.setCurrentIndex(version_list.index(self.wallpaper_type))

        # Checkbox
        self.cb_minimize = QCheckBox('Minimize to Tray')
        self.cb_minimize.stateChanged.connect(self.closeEvent)

        # Checkbox
        self.cb_start_app_when_start = QCheckBox('Start Application when Windows start', self)
        if self.config.getAutostart() == 'False':
            print(self.config.getAutostart())
            self.cb_start_app_when_start.setChecked(False)
        else:
            self.cb_start_app_when_start.setChecked(True)
        self.cb_start_app_when_start.stateChanged.connect(self.config.setAutostart)

        # Button
        btn_cancel = QPushButton('Close')
        btn_cancel.clicked.connect(self.closeEvent)

        # Text
        blog_text = QLabel('<a href="https://whiteknight3672.tistory.com">https://whiteknight3672.tistory.com</a>')
        blog_text.setOpenExternalLinks(True)
        developer_text = QLabel('© 2009-2020 Whiteknight')
        blog_text.setAlignment(Qt.AlignCenter)
        developer_text.setAlignment(Qt.AlignCenter)

        family_font = self.font()
        family_font.setPointSize(12)
        family_font.setFamily('AppleSDGothicNeoUL00')
        self.setFont(family_font)

        title_font = title_text.font()
        title_font.setPointSize(45)
        title_text.setFont(title_font)

        maker_font = developer_text.font()
        maker_font.setPointSize(10)
        developer_text.setFont(maker_font)

        hbox_time = QHBoxLayout()
        hbox_time.addWidget(self.txt_curr_time)
        hbox_time.addWidget(self.txt_prev_time)

        hbox_version = QHBoxLayout()
        hbox_version.addStretch(1)
        hbox_version.addWidget(os_version)
        hbox_version.addWidget(self.cb_select_version)
        hbox_version.addWidget(self.btn_manage_wallpaper)
        hbox_version.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(0.7)
        vbox.addLayout(hbox_time)
        vbox.addWidget(self.txt_wallpaper_info)

        vbox.addWidget(self.image_label)
        vbox.addWidget(title_text)
        vbox.addWidget(desc_text)
        vbox.addStretch(1)
        vbox.addLayout(hbox_version)
        vbox.addStretch(1)
        vbox.addWidget(self.cb_start_app_when_start)
        vbox.addWidget(self.cb_minimize)
        vbox.addStretch(1)
        vbox.addWidget(btn_cancel)  # cancel button
        vbox.addStretch(1)
        vbox.addWidget(blog_text)
        vbox.addWidget(developer_text)
        vbox.addStretch(0.8)
        self.setLayout(vbox)

        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(pal)

        self.setMinimumSize(QSize(650, 800))  # 사이즈 설정
        self.setMaximumSize(QSize(1000, 1000))  # 사이즈 설정
        self.setWindowTitle('PyWallpaper')  # 타이틀 설정
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 트레이 아이콘에 대해 초기화를 수행합니다.
    def initTray(self):
        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        info_action = QAction('PyWallpaper v0.8', self)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.inflate_window)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(info_action)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.DoubleClick

        self.tray_icon.show()

    # 앱 실행할 때 설정에서 값을 안불러오고 그냥 시작프로그램에 해당 파일이 등록되어 있는지 확인 하고 창을 띄운다.
    def inflate_window(self):
        location = r'%appdata%\Microsoft\Windows\Start Menu\Programs\Startup'
        launcher_location = os.path.expandvars(location) + r'\launcher.bat'
        isStartExist = os.path.exists(launcher_location)
        if isStartExist:
            self.cb_start_app_when_start.setChecked(True)
            print('Autostart enabled')
        else:
            print('Autostart disabled')
            self.cb_start_app_when_start.setChecked(False)
        self.show()

    def on_version_chkbox_changed(self, selected_item):
        # self.cb_select_version.
        version_dict = {'10.15 Catalina': 'Catalina', '10.14 Mojave': 'Mojave', '10.13 High Sierra': '10-13.jpg',
                        '10.12 Sierra': '10-12.jpg', '10.11 El Captain': '10-11.jpg', '10.10 Yosemite': '10-10.jpg',
                        '10.9  Mavericks': '10-9.jpg',
                        '10.8  Mountain Lion': '10-8.jpg', '10.7  Lion': '10-7.png', '10.6  Snow Leopard': '10-6.png',
                        '10.5  Leopard': '10-5.png',
                        '10.4  Tiger': '10-4.png', '10.3  Panther': '10-3.png', '10.2  Jaguar': '10-2.png',
                        '10.0  Cheetah & 10.1 Puma': '10-0_10.1.png'}

        version_list = ['10.15 Catalina', '10.14 Mojave', '10.13 High Sierra',
                        '10.12 Sierra', '10.11 El Captain', '10.10 Yosemite', '10.9  Mavericks',
                        '10.8  Mountain Lion', '10.7  Lion', '10.6  Snow Leopard', '10.5  Leopard',
                        '10.4  Tiger', '10.3  Panther', '10.2  Jaguar', '10.0  Cheetah & 10.1 Puma']

        os.chdir(self.abs_path)
        if os.path.exists('./wallpaper/' + version_dict[selected_item]):
            # cw = Main()
            if version_dict[selected_item] == 'Catalina' or version_dict[selected_item] == 'Mojave':
                os.chdir('./wallpaper')
                self.config.set_current_wallpaper_type(version_dict[selected_item])
                os.chdir('../')
                self.main_app.wallpaper_selector(version_dict[selected_item], initial_apply=True)
            else:
                os.chdir('./wallpaper')
                self.config.set_current_wallpaper_type(selected_item)
                self.main_app.wallpaper_selector(selected_item, initial_apply=True)
                os.chdir('../')
        else:

            print('not exist')
            message = 'The image you\'ve selected seems not downloaded to your system. \n\ndo you want to get it now?'

        self.prev_chked_item = selected_item

    def get_wallpaper_type(self):
        return self.wallpaper_type

    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box

    # GUI를 최소화 할 때 알림 메시지를 표시합니다.

    # 현재 시간을 구해 GUI에 표시합니다. -스레드에서 호출되어 실시간으로 업데이트됨
    @pyqtSlot(str)
    def setCurrTime(self, status):
        self.txt_curr_time.setText(status)

    # 다음 배경화면 나올 시간을 구해 GUI에 표시합니다.- 스레드에서 호출되어 실시간으로 시간 업데이트됨
    @pyqtSlot(str)
    def setNextTime(self, status):
        self.txt_prev_time.setText(status)

    # 현재 배경화면 및 비율을 GUI에 표시합니다. -스레드에서 호출되어 실시간으로 업데이트됨
    @pyqtSlot(str)
    def setWallpaperInfo(self, status):
        self.txt_wallpaper_info.setText(status)

    # X를 눌러 창을 닫았을 때 이벤트
    def closeEvent(self, event):
        if self.cb_minimize.isChecked():
            self.hide()
            self.tray_icon.showMessage(
                "Running in Background",
                "PyWallpaper is changing wallpaper every 18 minutes.",
                QSystemTrayIcon.Information,
                2000)
        else:
            message = 'PyWallpaper will be terminated and your wallpaper won\'t change anymore.' \
                      '\nAre you want to proceed?\n\n(Instead, you can check \'Minimize to Tray\' option.)'
            reply = QMessageBox.question(self, 'Message', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                sys.exit(app.exec_())
                pass
            else:
                pass

    def onManageBtnClicked(self):
        self.get_wallpaper_signal.emit(self.cb_select_version.currentText())


class MainThread(QThread):
    time_signal = pyqtSignal(str)
    next_time_signal = pyqtSignal(str)
    wallpaper_info_sig = pyqtSignal(str)
    apply_gui_signal = pyqtSignal(int)

    def __init__(self, location=None):
        super(self.__class__, self).__init__()
        self.abs_path = location
        self.main_app = Main(self.abs_path)
        self.config = ConfigManager(self.abs_path)
        self.curr_wallpaper = None
        self.wallpaper_type = self.config.get_current_wallpaper_type()
        self.main_app.wallpaper_selector(wallpaper_type=self.wallpaper_type, initial_apply=True)

    @pyqtSlot()
    def run(self):
        while True:
            # time
            t = time.localtime()
            self.wallpaper_type = self.config.get_current_wallpaper_type()

            next_hour, next_min = self.main_app.get_next_change_time(self.wallpaper_type)

            self.time_signal.emit('{}:{}:{}'.format(t.tm_hour, t.tm_min, t.tm_sec))

            if self.wallpaper_type == 'Catalina' or self.wallpaper_type == 'Mojave':
                cur_pic, prev_pic, mix = self.main_app.get_wallpaper_info()
                self.wallpaper_info_sig.emit(
                    'Current : {} {}% | Previous : {} {}%'.format(cur_pic, mix, prev_pic, round((100 - mix), 2)))
                self.next_time_signal.emit('Wallpaper will be updated at {}:{}'.format(next_hour, next_min))
                self.main_app.wallpaper_selector(wallpaper_type=self.wallpaper_type, initial_apply=False)
            else:
                print(
                    'curr_wallapaper : {} , change wallpaper_to : {}'.format(self.curr_wallpaper, self.wallpaper_type))
                self.wallpaper_info_sig.emit(
                    'Using Static Wallpaper. \nSet wallpaper with Catalina or Mojave to see more information.')
                self.next_time_signal.emit('')
                if not self.curr_wallpaper == self.wallpaper_type:
                    self.main_app.wallpaper_selector(wallpaper_type=self.wallpaper_type, initial_apply=False)
                    self.curr_wallpaper = self.wallpaper_type

            time.sleep(1)


if __name__ == '__main__':
    print('welcome to pyWallpaper.')
    path = os.path.abspath(os.getcwd())

    app = QApplication(sys.argv)
    # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyle('Fusion')
    example = MainQLogic(app, path, is_called_from_main=True)
    sys.exit(app.exec_())
