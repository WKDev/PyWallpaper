import ctypes
import time
import cv2

import os


def get_wallpaper_label():
    os.path.abspath(os.getcwd())
    wallpaper_list = os.listdir('./wallpaper/Catalina')
    return wallpaper_list

# https://512pixels.net/projects/default-mac-wallpapers-in-5k/

def onMouse(x):
    pass

def smooth_change(hour, min, sec, wallpaper_list, mix):
    #image_amount = 8, wallpapers are changed every 3 hours(180min)
    #when resolution is 10, image_amount = 8, wallpapers are changed every 18min

    cur_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(t.tm_hour // 3) - 1]
    prev_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(t.tm_hour // 3) - 2]

    cur_pic = cv2.imread(cur_pic_path)
    prev_pic = cv2.imread(prev_pic_path)
    # hour_to_min = hour*60
    # elasped_min = hour_to_min + min
    for i in range(0,24):
        cur_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(i // 3) - 1]
        prev_pic_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(i // 3) - 2]
        cur_pic = cv2.imread(cur_pic_path)
        prev_pic = cv2.imread(prev_pic_path)
        cur_pic = cv2.resize(cur_pic, (1504, 1504))
        prev_pic = cv2.resize(prev_pic, (1504, 1504))
        for j in range(0,60):
            test_elasped = j + i*60
            if(test_elasped % 18 == 0):
                print('배경화면을 변경합니다. mix : {}, simulated_time | {} : {}, test_elasped :{}cur : {}, prev :{}'.format(mix, i, j, test_elasped, wallpaper_list[(i // 3) - 1], wallpaper_list[(i // 3) - 2]))
                mix +=10
                cv2.namedWindow("test", cv2.WINDOW_GUI_NORMAL)
                weighted_img = cv2.addWeighted(cur_pic, float(mix) / 100, prev_pic, float(100 - mix) / 100, 0)
                cv2.imshow('test', weighted_img)
                if(mix ==110):
                    mix = 10
                time.sleep(0.2)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

def change_wallpaper():
    # 'C:/Users/chanh/PyCharmProjects/PyWallpaper/wallpaper/Mojave/10-14-Mojave-15.jpg'
    print("배경화면을 바꿉니다.")
    # wallpaper_path = os.getcwd() + '\\wallpaper\\Catalina\\' + wallpaper_list[(t.tm_hour // 3)-1]
    # wallpaper_path.replace('\\', '/')
    # print(wallpaper_path, t.tm_hour // 3)
    wallpaper_path = os.getcwd() + 'wallpaper.jpg'
    ctypes.windll.user32.SystemParametersInfoW(0x14, 0, wallpaper_path, 0x3)  # SystemParametersInfoA
    print('현재 시간 {}:{}'.format(t.tm_hour, t.tm_min))

if __name__ == '__main__':
    mix = 10
    list = get_wallpaper_label()

    # image = Image.open("image.gif")
    # icon = pystray.Icon(name="SPAM!", icon=image, title="MOBASuite", menu=None)

    # while True:
    #     # icon.run()
    #     t = time.localtime()
    #
    #     change_wallpaper(list)
    t = time.localtime()
    smooth_change(t.tm_hour, t.tm_min, t.tm_sec, list, mix)



