from PIL import Image
import os, re
from PicClearUp import get_input_path, mk_dir

sizeInfo = {"5": [(850, 1220), (1220, 850)], "6": [(1000, 1490), (1490, 1000)], "7": [(1200, 1680),
                                                                                      (1680, 1200)]}
myDPI = (254, 254)


class m_img():
    def __init__(self, path):
        self.path = path
        self.img = Image.open(self.path)
        # self.new_img.show()
        self.info = self.img.info
        self.width = self.img.width
        self.height = self.img.height

    def clip_img(self, width, height):
        self.img = self.img.crop(
            ((self.width - width) / 2, (self.height - height) / 2, width + (self.width - width) / 2,
             height + (self.height - height) / 2))
        self.width = self.img.width
        self.height = self.img.height

    def zoom_img(self, width, height):
        w = width
        h = int(width * self.height / self.width)
        if h < height:
            h = height
            w = int(height * self.width / self.height)

        self.img = self.img.resize((w, h), Image.ANTIALIAS)
        self.width = self.img.width
        self.height = self.img.height

    def show(self):
        self.img.show()

    def save(self, path):
        self.img.save(path, dip=(254, 254))

    def check_icc(self):
        try:
            if 'icc_profile' not in self.info:
                # print("\033[1;33;44m注意！%s没有icc信息\033[0m" % img.filename)
                return False
        except:
            return True
        #
        # def im_resized(pic, size):
        #     w, h = pic.size
        #     if w / h < 1:  # 判断图片为横版 or 竖版
        #         # 竖版
        #         if w / h > sizeInfo[size][0][0] / sizeInfo[size][0][1]:
        #             mode = 'h'
        #             num = sizeInfo[size][0][1]
        #             num_w = sizeInfo[size][0][0]
        #         else:
        #             mode = 'w'
        #             num = sizeInfo[size][0][0]
        #             num_h = sizeInfo[size][0][1]
        #     else:
        #         # 横版
        #         if w / h < sizeInfo[size][1][0] / sizeInfo[size][1][1]:
        #             mode = 'w'
        #             num = sizeInfo[size][1][0]
        #             num_h = sizeInfo[size][1][1]
        #         else:
        #             mode = 'h'
        #             num = sizeInfo[size][1][1]
        #             num_w = sizeInfo[size][1][0]
        #     if mode == 'w':
        #         h = int(num * h / w)
        #         w = num
        #         pic_resized = pic.resize((w, h), Image.ANTIALIAS)
        #         pic_resized = pic_resized.crop((0, (h - num_h) / 2, num, num_h + (h - num_h) / 2))
        #     if mode == 'h':
        #         w = int(num * w / h)
        #         h = num
        #         pic_resized = pic.resize((w, h), Image.ANTIALIAS)
        #         pic_resized = pic_resized.crop(((w - num_w) / 2, 0, num_w + (w - num_w) / 2, num))
        #     return pic_resized


if __name__ == '__main__':
    # img = img('img.jpg')
    # img.zoom_img(2500, 2500)
    # img.clip_img(2500, 2500)
    # img.show()

    # 遍历指定路径下所有jpg文件

    path = get_input_path()

    mk_dir(path, '大7寸')
    for root, dir, files in os.walk(path):
        # 快速跳出分,拣目录

        if re.search('大7寸', root):
            continue
        for file in files:
            print("file:", file)
            if re.search('7寸', file):
                print("path:", os.path.join(root, file))
                img = m_img(os.path.join(root, file))
                if img.width < 1300:
                    img.zoom_img(1300, 1820)
                    img.clip_img(1300, 1800)
                else:
                    img.zoom_img(1820, 1300)
                    img.clip_img(1800, 1300)
                img.save(os.path.join(path, "大7寸", file))

    # pic = Image.open('img.jpg')
    # pic.show()
    # dict_exif = pic._getexif()
    # print(dict_exif[274])
    # im_resized = im_resized(pic, '7')
    # print(im_resized)
    # im_resized.save('123_h.jpg', dpi=myDPI, quality=100, subsampling=0)
    # for root, dir, files in os.walk('韩礼\\'):
    #     os.mkdir(root + './7寸')
    #     for file in files:
    #         pic = Image.open(os.path.join(root, file))
    #         print(pic)
    #         pic_resized = im_resized(pic, '7')
    #         print(pic_resized)
    #         pic_resized.save(os.path.join(root, '7寸', file), dpi=myDPI, quality=100, subsampling=0)
