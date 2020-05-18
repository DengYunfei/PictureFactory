from PIL import Image
import os
sizeInfo = {"5": [(850, 1220), (1220, 850)], "6": [(1000, 1490), (1490, 1000)], "7": [(1200, 1680),
                                                                                      (1680, 1200)]}
myDPI = (254, 254)

def check_icc(fname):
    pass

def im_resized(pic, size):
    w, h = pic.size
    if w / h < 1:  # 判断图片为横版 or 竖版
        # 竖版
        if w / h > sizeInfo[size][0][0] / sizeInfo[size][0][1]:
            mode = 'h'
            num = sizeInfo[size][0][1]
            num_w = sizeInfo[size][0][0]
        else:
            mode = 'w'
            num = sizeInfo[size][0][0]
            num_h = sizeInfo[size][0][1]
    else:
        # 横版
        if w / h < sizeInfo[size][1][0] / sizeInfo[size][1][1]:
            mode = 'w'
            num = sizeInfo[size][1][0]
            num_h = sizeInfo[size][1][1]
        else:
            mode = 'h'
            num = sizeInfo[size][1][1]
            num_w = sizeInfo[size][1][0]
    if mode == 'w':
        h = int(num * h / w)
        w = num
        pic_resized = pic.resize((w, h), Image.ANTIALIAS)
        pic_resized = pic_resized.crop((0, (h - num_h) / 2, num, num_h + (h - num_h) / 2))
    if mode == 'h':
        w = int(num * w / h)
        h = num
        pic_resized = pic.resize((w, h), Image.ANTIALIAS)
        pic_resized = pic_resized.crop(((w - num_w) / 2, 0, num_w + (w - num_w) / 2, num))
    return pic_resized


if __name__ == '__main__':
    # pic = Image.open('IMG_5001.JPG')
    # dict_exif = pic._getexif()
    # print(dict_exif[274])
    # im_resized = im_resized(pic, '7')
    # print(im_resized)
    # im_resized.save('123_h.jpg', dpi=myDPI, quality=100, subsampling=0)
    for root,dir,files in os.walk('韩礼\\'):
        os.mkdir(root+'./7寸')
        for file in files:

            pic = Image.open(os.path.join(root,file))
            print(pic)
            pic_resized = im_resized(pic, '7')
            print(pic_resized)
            pic_resized.save(os.path.join(root,'7寸',file), dpi=myDPI, quality=100, subsampling=0)
