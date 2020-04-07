import ctypes
import shutil
import time
import cv2
import os

import sys

from PyQt5.QtWidgets import QApplication,QWidget, QAction, qApp, QHBoxLayout, \
    QVBoxLayout, QPushButton, QLabel, QCheckBox, QSystemTrayIcon, QMenu,  QStyle
from PyQt5.QtCore import QThread, Qt, QSize
from PyQt5.QtGui import QPixmap

# https://512pixels.net/projects/default-mac-wallpapers-in-5k/

class main:
    def __init__(self):
        self.wallpaper_list = []
        self.current_picture = ''
        self.previous_picture = ''
        self.image_location = []
        self.wallpaper_path = ''
        self.mix = 0
        self.config = []

    #파일이 존재하는 위치에서 배경화면 파일 리스트 불러오기
    def get_wallpaper_label(self):
        os.path.abspath(os.getcwd())
        self.wallpaper_list = os.listdir('./wallpaper/Catalina')


    def get_next_change_time(self):
        t = time.localtime()
        curr_min = t.tm_hour * 60 + t.tm_min
        while not curr_min % 18 == 0:
            curr_min += 1

        next_hour = t.tm_hour
        next_min = curr_min - t.tm_hour * 60
        if next_min >= 60:
            next_hour += 1
            next_min -= 60

        if next_hour == 24:
            next_hour = 0

        return next_hour, next_min

    def get_wallpaper_info(self):
        return self.current_picture, self.previous_picture, self.mix

    def smooth_change(self):
        # image_amount = 8, wallpapers are changed every 3 hours(180min)
        # when resolution is 10, image_amount = 8, wallpapers are changed every 18min

        hour = time.localtime().tm_hour
        min = time.localtime().tm_min
        sec = time.localtime().tm_sec

        elasped = min + hour * 60
        if hour % 3 == 0 and min == 0 and sec < 20:
            self.current_picture = self.wallpaper_list[(hour // 3)][:-4]
            self.previous_picture = self.wallpaper_list[(hour // 3) - 1][:-4]
            cur_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + self.current_picture + '.jpg'
            prev_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + self.previous_picture + '.jpg'

            cur_pic = cv2.imread(cur_pic_path)
            prev_pic = cv2.imread(prev_pic_path)

        if (elasped % 18 == 0) and sec < 10:
            self.mix = (elasped - (hour // 3) * 180) * 10 / 18
            # print(elasped, mix)
            print('배경화면을 변경합니다. time {}:{},  elasped :{}   cur : {} {}%, prev :{} {}%'
                  .format(hour, min, elasped, self.current_picture, self.mix, self.previous_picture, (100 - self.mix)))

            try:
                weighted_img = cv2.addWeighted(cur_pic, float(self.mix) / 100, prev_pic, float(100 - self.mix) / 100, 0)
            except:
                print('배경화면이 불러와져 있지않아 불러온 후 이미지를 처리합니다.')
                self.current_picture = self.wallpaper_list[(hour // 3)][:-4]
                self.previous_picture = self.wallpaper_list[(hour // 3) - 1][:-4]
                cur_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + self.current_picture + '.jpg'
                prev_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + self.previous_picture + '.jpg'
                cur_pic = cv2.imread(cur_pic_path)
                prev_pic = cv2.imread(prev_pic_path)
                weighted_img = cv2.addWeighted(cur_pic, float(self.mix) / 100, prev_pic, float(100 - self.mix) / 100, 0)

            t1 = time.time()
            cv2.imwrite('wallpaper.jpg', weighted_img)
            t2 = time.time()
            print('배경화면 생성 완료, {}초 소요'.format(t2 - t1))
            self.apply_wallpaper()

    def apply_wallpaper(self):
        self.wallpaper_path = os.getcwd() + r'\wallpaper.jpg'
        print('경로 :' + self.wallpaper_path)
        hour, min = self.get_next_change_time()
        print('에서 배경화면 적용 완료. 다음 적용 시간은 {}:{}입니다.'.format(hour, min))
        ctypes.windll.user32.SystemParametersInfoW(0x14, 0, self.wallpaper_path, 0x3)  # SystemParametersInfoA

    def import_setting(self):
        with open('config.ini', 'r') as f:
            self.config = f.readlines()

    def export_setting(self):
        with open('config.ini', 'w') as f:
            for i in self.config:
                f.write(i)


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTray()

        # Thread start
        self.worker = Worker()
        self.worker.start()

    def initUI(self):
        # text
        self.text_field = QLabel('time')
        self.next_field = QLabel('next_time')
        self.wallpapaer_title_field = QLabel('wallpaper')
        self.wallpapaer_title_field.setAlignment(Qt.AlignCenter)

        # Image
        image_label = QLabel()
        image = cv2.imread('wallpaper.jpg', cv2.IMREAD_COLOR)
        resize = cv2.resize(image, (3008, 3008), cv2.INTER_AREA)
        width = 100
        height = 800
        processed = resize[height:height + 500, width:width + 1500]

        cv2.imwrite('title_img.png', processed)

        pixmap = QPixmap('title_img.png')

        pixmap = pixmap.scaled(750, 250, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Text
        title_text = QLabel('PyWallpaper', self)
        desc_text = QLabel('An Application that helps apply iMac wallpaper for 4k+ Monitor with Windows')
        title_text.setAlignment(Qt.AlignCenter)
        desc_text.setAlignment(Qt.AlignCenter)

        # Checkbox
        self.cb_minimize = QCheckBox('Minimize to Tray')
        self.cb_minimize.stateChanged.connect(self.cancel)

        # Checkbox
        self.cb_start_app_when_start = QCheckBox('Start Application when Windows start', self)

        self.cb_start_app_when_start.stateChanged.connect(self.toggle_autostart)

        # Button
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.cancel)

        # Text
        blog_text = QLabel('<a href="https://whiteknight3672.tistory.com">https://whiteknight3672.tistory.com</a>')
        # blog_text.setAcceptRichText(True)
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
        hbox_time.addStretch(1)
        hbox_time.addWidget(self.text_field)
        hbox_time.addStretch(4)
        hbox_time.addWidget(self.next_field)
        hbox_time.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(0.7)
        vbox.addLayout(hbox_time)
        vbox.addWidget(self.wallpapaer_title_field)
        vbox.addWidget(image_label)
        vbox.addWidget(title_text)
        vbox.addWidget(desc_text)
        vbox.addStretch(2)
        vbox.addWidget(self.cb_start_app_when_start)
        vbox.addWidget(self.cb_minimize)
        vbox.addStretch(1)
        vbox.addWidget(btn_cancel)  # cancel button
        vbox.addStretch(1)
        vbox.addWidget(blog_text)
        vbox.addWidget(developer_text)
        vbox.addStretch(0.8)
        self.setLayout(vbox)

        self.setMinimumSize(QSize(600, 800))  # 사이즈 설정
        self.setMaximumSize(QSize(1000, 800))  # 사이즈 설정
        self.setWindowTitle('PyWallpaper')  # 타이틀 설정
        self.hide()

    def initTray(self):
        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        # hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.inflate_window)
        # hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.show()

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

    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self, event):
        if self.cb_minimize.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Running in Background",
                "PyWallpaper is changing wallpaper corresponding with time",
                QSystemTrayIcon.Information,
                2000
            )

    #현재 시간 설정(QThread에 집어넣음)
    def setCurrTime(self):
        t = time.localtime()
        curr_time = 'Current Time | {}:{}:{}'.format(t.tm_hour, t.tm_min, t.tm_sec)
        self.text_field.setText(curr_time)

    # 다음 배경화면 나올 시간 설정 - 스레드에서 호출되어 실시간으로 시간 업데이트됨
    def setNextTime(self, hour, min):
        next_time = 'Wallpaper will be changed at | {}:{}'.format(hour, min)
        self.next_field.setText(next_time)

    # 현재 배경화면 및 비율 표시 -스레드에서 호출되어 실시간으로 업데이트됨
    def setWallpaperTitle(self, title):
        self.wallpapaer_title_field.setText(title)

    # 자동시작 여부 확인 및 자동시작 세팅
    def toggle_autostart(self, state):
        location = r'%appdata%\Microsoft\Windows\Start Menu\Programs\Startup'
        launcher_location = os.path.expandvars(location) + r'\launcher.bat'

        if state == Qt.Checked:
            with open('launcher.bat', 'w') as f:
                f.write('cd '+ os.getcwd()+'\n')
                f.write('start pythonw pywallpaper.py')
            shutil.copy('launcher.bat', launcher_location)

        else:
            if os.path.isfile(launcher_location):
                os.remove(launcher_location)
                print('startup_file removed')

    #X를 눌러 창을 닫았을 때 이벤트
    def cancel(self):
        if self.cb_minimize.isChecked():
            self.hide()
            self.tray_icon.showMessage(
                "Running in Background",
                "PyWallpaper is changing wallpaper every 18 minutes.",
                QSystemTrayIcon.Information,
                2000)
        else:
            sys.exit(app.exec_())

class Worker(QThread):
    def run(self):
        while True:
            main_app.smooth_change()
            next_hour, next_min = main_app.get_next_change_time()
            ev.setCurrTime()
            ev.setNextTime(next_hour, next_min)
            title1, title2, mix = main_app.get_wallpaper_info()
            ev.setWallpaperTitle('Prev : '+title2+' '+ str(100-mix)+'%    |   Now : ' + title1 +' '+str(mix)+'%')
            time.sleep(1)

if __name__ == '__main__':
    print('welcome to pyWallpaper.')
    main_app = main()
    # main_app.import_setting()  #later versions
    main_app.get_wallpaper_label()

    # gui 부분
    os.system("exit")
    app = QApplication(sys.argv)
    ev = Gui()

    # 트레이 아이콘
    sys.exit(app.exec_())
