import json
import os
import tkinter as tk
from shutil import copyfile

try:
    from tkinter import filedialog
except:
    print("加载tkinter组件失败")

from PIL import Image

count = 0
# 读取尺寸描述文件
with open("PicSizeinfo.json", 'r', encoding='utf-8') as json_file:
    picSizeinfo = json.load(json_file)


# 创建文件夹
def mkdir(path, file):
    if os.path.isdir(os.path.join(path, file)):
        # 要创建的文件夹已经存在
        return
    else:
        # 文件夹不存在，立即创建
        os.mkdir(os.path.join(path, file))


# 获取图片的宽高数据
def getPicSize(img):
    size = (img.width, img.height)
    return size


# 获取图片宽高所对应的尺寸类别
def getPicType(sized):
    for items in picSizeinfo:
        for size in picSizeinfo[items]:
            if sized[0] > size["width"] - 100 and sized[0] < size["width"] + 100:
                if sized[1] > size["height"] - 100 and sized[1] < size["height"] + 100:
                    return items, size["name"]

    return "未知尺寸", str(sized[0]) + "x" + str(sized[1])


# 图片分拣主方法
def PicFiltrate(path):
    # 制作忽略目录列表
    InvalidDirectory = ['未知尺寸','分拣']
    tpyeLine = ['未知尺寸','分拣']
    for items in picSizeinfo:
        InvalidDirectory.append(items)
        tpyeLine.append(items)
        for size in picSizeinfo[items]:
            InvalidDirectory.append(size["name"])
    # print(InvalidDirectory)  # 查看忽略目录列表
    # print(tpyeLine)  # 查看忽略目录列表
    count = 0

    mkdir(path, '分拣')
    # 遍历指定路径下所有jpg文件
    for root, dir, files in os.walk(path):
        # 快速跳出忽略目录
        if len(root.split("\\")) < 3:
            # 保证当前在最外层目录
            # print(root.split("\\")[-1])
            if root.split("\\")[-1] in InvalidDirectory:
                # 如果当前文件夹在忽略列表中则跳出本次循环
                continue
        picCuunt = len(files)  # 同品数量（相册P数）
        for file in files:
            if file.split('.')[-1].lower() == 'jpg':
                with Image.open(os.path.join(root, file)) as img_pillow:
                    PicSize = getPicSize(img_pillow)  # 获得图片宽高    返回值：元组(宽，高)

                # img_pillow = Image.open(os.path.join(root, file))
                PicType = getPicType(PicSize)  # 获得细分品类    返回值：元组(类型，尺寸)
                # print(type(PicType))
                # print(type(os.path.join(root, file)[len(path) + 1:]))
                newFileName = os.path.join(root, file)[len(path) +1:]
                print('newFileName：',newFileName)
                newFileName = newFileName.replace('/', '-')
                # print(newFileName)
                # newFileName = newFileName.replace('\\', '-')

                # print("newFileName",newFileName)
                if PicType[0] == "未知尺寸":
                    mkdir(os.path.join(path, '分拣'), PicType[0])
                    savepath = os.path.join(path, '分拣', PicType[0])
                else:
                    newFileNameList = newFileName.split("-")
                    newFileNameList[-1] = "★" + newFileNameList[-1]
                    newFileName = "-".join(newFileNameList)
                    newFileName = newFileName[:-4] + "_" + str(picCuunt) + ".jpg"
                    # print('type：',PicSize[0])
                    if PicType[0] == "相册":
                        mkdir(os.path.join(path, '分拣'), PicType[1])
                        savepath = os.path.join(path, '分拣', PicType[1])
                        # print('相册savepath:',savepath)
                    else:
                        mkdir(os.path.join(path, '分拣'), PicType[0])
                        savepath = os.path.join(path, '分拣',PicType[0])
                        # print('savepath:',savepath)
                        newFileName = PicType[1] + '-' + newFileName
                print(os.path.join(root, file), "\n", os.path.join(savepath, newFileName), "\n\n\n")
                copyfile(os.path.join(root, file), os.path.join(savepath, newFileName))
                try:
                    copyfile(os.path.join(root, file), os.path.join(path, savepath, newFileName))
                    print("文件已COPY到", count, os.path.join(path, savepath, newFileName))
                except:
                    print('拷贝', os.path.join(root, file), '失败')
                # print(os.path.join(root, file)[len(path) + 1:])
                count += 1
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
    # Fpath = filedialog.askdirectory()
    # mkdir(Fpath, '7c')
    PicFiltrate("/Users/dengyunfei/PycharmProjects/2020.04.17")
    # print(Fpath)
