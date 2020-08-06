import os, cv2, time, ctypes

class Main:
    def __init__(self, abs_path):
        super().__init__()
        self.abs_path = abs_path
        self.wallpaper_list = []
        self.wall_type = None
        self.current_picture = None
        self.previous_picture = None
        self.mix = 0

    # 파일이 존재하는 위치에서 배경화면 파일 리스트 불러오기
    def get_wallpaper_label(self):
        os.chdir(self.abs_path)
        if self.wall_type == 'Catalina' and os.path.exists('./wallpaper/Catalina'):
            return os.listdir(self.abs_path + '\\wallpaper\\Catalina')
        else:
            print('requirement is not fulfilled.')

    # 사진 불러오고 합성하는 핵심 기능 담겨있음
    def change_background_catalina(self, wall_type, apply_now=False):
        self.wall_type = wall_type
        self.wallpaper_list = self.get_wallpaper_label()

        hour = time.localtime().tm_hour
        min = time.localtime().tm_min
        sec = time.localtime().tm_sec
        elasped = min + hour * 60

        # image_amount = 8, wallpapers are changed every 3 hours(180min)
        # when resolution is 10, image_amount = 8, wallpapers are changed every 18min


        # 매 18분 마다 이미지의 비율을 확인하고 변경합니다.
        if (elasped % 18 == 0) and sec < 5 or apply_now == True:
            os.chdir(self.abs_path)
            self.mix = (elasped - (hour // 3) * 180) * 10 / 18
            # print(elasped, mix)
            print('배경화면을 변경합니다. time {}:{},  elasped :{}   cur : {} {}%, prev :{} {}%'
                  .format(hour, min, elasped, self.current_picture, int(self.mix), self.previous_picture,
                          int(100 - self.mix)))

            # 시간 경과에 따라 이미지 합성을 수행합니다. 이전에 이미지를 불러온 적이 없다면 이미지를 불러온 후 합성을 수행합니다.
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
            self.apply_wallpaper()
            os.chdir('../')

    # 합성한 이미지를 배경화면으로 설정합니다.
    def apply_wallpaper(self):
        os.chdir(self.abs_path)
        os.chdir('./wallpaper')
        wallpaper_path = os.getcwd() + r'\catalina_processed.jpg'
        ctypes.windll.user32.SystemParametersInfoW(0x14, 0, wallpaper_path, 0x3)  # SystemParametersInfoA

if __name__ == '__main__':
    abs_path = os.getcwd()
    main = Main(abs_path)

    initial_apply = True
    main.change_background_catalina(apply_now=initial_apply)
    initial_apply = False
