import json
import os
import tkinter as tk
from shutil import copyfile
import re
from tkinter import filedialog
from PIL import Image

# 加载尺寸信息
# 读取尺寸描述文件
with open("PicSizeinfo.json", 'r', encoding='utf-8') as json_file:
    picSizeinfo = json.load(json_file)


# 创建文件夹
def mk_dir(path, file):
    if os.path.isdir(os.path.join(path, file)):
        # 要创建的文件夹已经存在
        return
    else:
        # 文件夹不存在，立即创建
        os.mkdir(os.path.join(path, file))


# 获取图片的宽高数据
def get_pic_size(img):
    size = (img.width, img.height)
    return size


# 获取图片宽高所对应的尺寸类别
def get_pic_type(sized):
    compensation = 50
    for items in picSizeinfo:
        for size in picSizeinfo[items]:
            if sized[0] > size["width"] - compensation and sized[0] < size["width"] + compensation:
                if sized[1] > size["height"] - compensation and sized[1] < size["height"] + compensation:
                    return items, size["name"]

    return "未知尺寸", str(sized[0]) + "x" + str(sized[1])


# 图片分拣主方法
def pic_filtrate(path):
    count = 0

    mk_dir(path, '分拣')
    # 遍历指定路径下所有jpg文件
    for root, dir, files in os.walk(path):
        # 快速跳出分拣目录
        if re.search('分拣', root):
            continue

        picCuunt = len(files)  # 同品数量（相册P数）
        for file in files:
            if file.split('.')[-1].lower() == 'jpg':
                # 处理*.jpg文件
                with Image.open(os.path.join(root, file)) as img_pillow:
                    PicSize = get_pic_size(img_pillow)  # 获得图片宽高    返回值：元组(宽，高)
                PicType = get_pic_type(PicSize)  # 获得细分品类    返回值：元组(类型，尺寸)
                newFileName = os.path.join(root, file)[len(path) + 1:]  # 取得选择路径以后部分
                newFileName = newFileName.replace('/', '-')  # 非windows系统路径扁平化
                newFileName = newFileName.replace('\\', '-')  # windows系统路径扁平化
                if PicType[0] == "未知尺寸":
                    # 未知尺寸产品处理
                    mk_dir(os.path.join(path, '分拣'), PicType[0])
                    savepath = os.path.join(path, '分拣', PicType[0])
                elif PicType[0] == "相册":
                    # 相册产品处理
                    newFileNameList = newFileName.split("-")
                    newFileNameList[-1] = "★" + newFileNameList[-1]
                    newFileName = "-".join(newFileNameList)
                    newFileName = newFileName[:-4] + "_" + str(picCuunt) + ".jpg"
                    mk_dir(os.path.join(path, '分拣'), PicType[1])
                    savepath = os.path.join(path, '分拣', PicType[1])
                else:
                    # 其他产品处理
                    mk_dir(os.path.join(path, '分拣'), PicType[0])
                    savepath = os.path.join(path, '分拣', PicType[0])
                    newFileName = PicType[1] + '-' + newFileName
                # 尝试copy图片到分拣目录
                try:
                    copyfile(os.path.join(root, file), os.path.join(path, savepath, newFileName))
                    print("文件已COPY到", count, os.path.join(path, savepath, newFileName))
                except:
                    print('拷贝', os.path.join(root, file), '失败')

                count += 1  # 计数器增加1


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    fpath = filedialog.askdirectory()
    pic_filtrate(fpath)
