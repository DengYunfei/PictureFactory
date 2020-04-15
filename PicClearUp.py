import json
import os
import tkinter as tk
from shutil import copyfile
from tkinter import filedialog

from PIL import Image

count = 0
with open("PicSizeinfo.json", 'r', encoding='utf-8') as json_file:
    picSizeinfo = json.load(json_file)


def mkdir(path, file):
    if os.path.isdir(os.path.join(path, file)):
        return
    else:
        os.mkdir(os.path.join(path, file))


def getPicSize(img):
    size = (img.width, img.height)
    return size


def getPicType(sized):
    for items in picSizeinfo:
        for size in picSizeinfo[items]:
            if sized[0] > size["width"] - 100 and sized[0] < size["width"] + 100:
                if sized[1] > size["height"] - 100 and sized[1] < size["height"] + 100:
                    return items, size["name"]

    return "未知尺寸", str(sized[0]) + "x" + str(sized[1])


def PicFiltrate(path):
    # 制作忽略目录列表
    InvalidDirectory = ['未知尺寸']
    tpyeLine = ['未知尺寸']
    for items in picSizeinfo:
        InvalidDirectory.append(items)
        tpyeLine.append(items)
        for size in picSizeinfo[items]:
            InvalidDirectory.append(size["name"])
    print(InvalidDirectory)  # 查看忽略目录列表
    print(tpyeLine)  # 查看忽略目录列表
    count = 0
    # 遍历指定路径下所有jpg文件
    for root, dir, files in os.walk(path):
        # 快速跳出忽略目录
        if len(root.split("\\")) < 3:
            print(root.split("\\")[-1])
            if root.split("\\")[-1] in InvalidDirectory:
                continue
        picCuunt = len(files)  # 同品数量（相册P数）
        for file in files:
            if file.split('.')[-1].lower() == 'jpg':
                img_pillow = Image.open(os.path.join(root, file))
                PicSize = getPicSize(img_pillow)  # 获得图片宽高    返回值：元组
                PicType = getPicType(PicSize)  # 获得细分品类    返回值：元组
                # print(type(PicType))
                print(type(os.path.join(root, file)[len(path) + 1:]))
                newFileName = os.path.join(root, file)[len(path) + 1:]

                newFileName = newFileName.replace('\\', '-')
                # print(newFileName)
                # newFileName = newFileName.replace('\\', '-')

                # print("newFileName",newFileName)
                if PicType[0] == "未知尺寸":
                    mkdir(path, PicType[0])
                    savepath = os.path.join(path, PicType[0])
                else:
                    newFileNameList = newFileName.split("-")
                    newFileNameList[-1] = "★" + newFileNameList[-1]
                    newFileName = "-".join(newFileNameList)
                    newFileName = newFileName[:-4] + "_" + str(picCuunt) + ".jpg"
                    mkdir(path, PicType[0])
                    mkdir(os.path.join(path, PicType[0]), PicType[1])
                    savepath = os.path.join(path, PicType[0], PicType[1])
                # print(os.path.join(root, file),os.path.join(path, PicType[1], newFileName))
                copyfile(os.path.join(root, file), os.path.join(path, savepath, newFileName))

                # print(os.path.join(root, file)[len(path) + 1:])
                count += 1
                print("文件已COPY到", count, os.path.join(path, savepath, newFileName))
                # print(picsize)
                # else:
                # mkdir(path, "未知尺寸")
                # os.system('copy' + os.path.join(root, file) + os.path.join(path, size["name"], file))
                # print(os.path.join(root, file)[len(path) + 1:])
                # print(picsize)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    # for items in picSizeinfo:
    #     for size in picSizeinfo[items]:
    #         print(items+"-"+size["name"])
    Fpath = filedialog.askdirectory()
    # mkdir(Fpath, '7c')
    PicFiltrate(Fpath)
    # print(Fpath)
