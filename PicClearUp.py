import json, os, re, hashlib
from shutil import copyfile
from PIL import Image
from tkinter import messagebox
import tkinter as tk
from tkinter import filedialog


class PicClearUp_UI():
    def __init__(self, path=""):
        self.root = tk.Tk()
        self.root.title("图片分拣")
        self.root.attributes()
        self.root.geometry('480x120')
        self.path = path
        self.root.resizable(0, 0)  # 防止用户调整尺寸
        self._setpage()
        print(self.path)

    def _setpage(self):
        self.label = tk.Label(self.root, text='请选择日期文件夹', anchor="w")
        self.btn1 = tk.Button(self.root, text='...', command=self.chooseDir)
        self.btn2 = tk.Button(self.root, text='确认', command=self.enterPath)
        self.entry = tk.Entry(self.root, textvariable=tk.StringVar(value=self.path))

        # 绘制窗口控件

        self.label.place(relx=0.01, rely=0.1, relwidth=0.5, relheight=0.2)
        self.btn1.place(relx=0.84, rely=0.4, relwidth=0.15, relheight=0.2)
        self.entry.place(relx=0.01, rely=0.4, relwidth=0.82, relheight=0.2)
        self.btn2.place(relx=0.4, rely=0.7, relwidth=0.15, relheight=0.2)

    def chooseDir(self):
        Fpath = filedialog.askdirectory()
        self.entry.delete(0, 'end')
        self.entry.insert(0, Fpath)

    def enterPath(self):
        self.path = self.entry.get()
        self.root.destroy()


# 读取尺寸描述文件
with open("PicSizeinfo.json", 'r', encoding='utf-8') as json_file:
    picSizeinfo = json.load(json_file)


# 判断两个文件是否相同
def diff(file_1, file_2):
    with open(file_1, 'rb') as file:
        data = file.read()
        file_1_md5 = hashlib.md5(data).hexdigest()
    if os.path.isfile(file_2):
        with open(file_2, 'rb') as file:
            data = file.read()
            file_2_md5 = hashlib.md5(data).hexdigest()
    else:
        file_2_md5 = ""
    if file_1_md5 == file_2_md5:
        return True


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
    dpi = img.info.get("dpi")

    if not dpi:
        dpi = (254, 254)
    width = img.width / dpi[0] * 2.54
    height = img.height / dpi[0] * 2.54
    size = (width, height)

    return size, dpi[0]


# 获取图片宽高所对应的尺寸类别
def get_pic_type(sized):
    compensation = 0.5
    for items in picSizeinfo:
        for size in picSizeinfo[items]:
            if sized[0] > size.get("width") - compensation and sized[0] < size.get("width") + compensation:
                if sized[1] > size.get("height") - compensation and sized[1] < size.get("height") + compensation:
                    return items, size["name"], (size.get("width"), size.get("height"))

    return "未知尺寸", str(sized[0]) + "x" + str(sized[1]), sized


# 图片分拣主方法
def pic_filtrate(path):
    count = 0
    copyright_count = 0
    erorr_count = 0
    error_info = []
    mk_dir(path, '分拣')
    # 遍历指定路径下所有jpg文件
    for root, dir, files in os.walk(path):
        # 快速跳出分拣目录
        if re.search('分拣', root):
            continue
        picCuunt = 0
        # 同品数量（相册P数）
        for file in files:
            if file.split('.')[-1].lower() == 'jpg':
                picCuunt += 1
        #分拣图片
        for file in files:
            if file.split('.')[-1].lower() == 'jpg':
                # 仅处理*.jpg文件
                with Image.open(os.path.join(root, file)) as img_pillow:

                    pic_size, pic_dpi = get_pic_size(img_pillow)  # 获得图片宽高    返回值：元组(宽，高)
                    pic_type = get_pic_type(pic_size)  # 获得细分品类    返回值：元组(类型，尺寸)
                newFileName = os.path.join(root, file)[len(path) + 1:]  # 取得选择路径以后部分
                print(newFileName)
                newFileName = newFileName.replace('/', '-')  # 非windows系统路径扁平化
                newFileName = newFileName.replace('\\', '-')  # windows系统路径扁平化
                if pic_type[0] == "未知尺寸":
                    # 未知尺寸产品处理
                    mk_dir(os.path.join(path, '分拣'), pic_type[0])
                    savepath = os.path.join(path, '分拣', pic_type[0])
                elif pic_type[0] == "相册":
                    # 相册产品处理
                    newFileNameList = newFileName.split("-")
                    newFileNameList[-1] = "★" + newFileNameList[-1]
                    newFileName = "-".join(newFileNameList)
                    newFileName = newFileName[:-4] + "_" + str(picCuunt) + ".jpg"
                    # print('type：',PicSize[0])

                    mk_dir(os.path.join(path, '分拣'), pic_type[1])
                    savepath = os.path.join(path, '分拣', pic_type[1])
                else:
                    # 其他产品处理
                    mk_dir(os.path.join(path, '分拣'), pic_type[0])
                    savepath = os.path.join(path, '分拣', pic_type[0])
                    newFileName = pic_type[1] + '-' + newFileName

                count += 1  # 计数器增加1
                if diff(os.path.join(root, file), os.path.join(path, savepath, newFileName)):
                    print(count, os.path.join(root, file), "没有改变。")
                else:
                    # 文件不同 尝试移动文件
                    try:
                        # 移动成功
                        copyfile(os.path.join(root, file), os.path.join(path, savepath, newFileName))
                        # print(count, "文件已COPY到", os.path.join(path, savepath, newFileName))

                        copyright_count += 1
                    except:
                        # 移动失败
                        error_info.append({'path': os.path.join(root, file), 'info': '拷贝失败'})
                        erorr_count += 1
                        # print('拷贝', os.path.join(root, file), '失败')

    counts = {'count': count, 'copyright_count': copyright_count, 'erorr_count': erorr_count}
    return error_info, counts


def get_input_path(path=""):
    op = PicClearUp_UI(path)
    op.root.mainloop()  # 显示获取路径窗体
    # 判断用户有无输入路径
    if op.path:
        # 有路径信息
        fpath = op.path
        return fpath
    else:
        # 无路径信息，退出方法
        return


def pic_clear_up(fpath):
    error_info, counts = pic_filtrate(fpath)
    # 反馈运行结果
    messagebox.showinfo("成功", '共导检测到【' + str(counts.get('count')) + '】张照片\n新添加【' + str(
        counts.get('copyright_count')) + '】张照片\n包含错误【' + str(counts.get('erorr_count')) + '】个错误')
    # 反馈错误信息
    if error_info:
        error_text = '错误信息'
        count = 1
        for info in error_info:
            error_text = error_text + '\n' + str(count) + '/' + str(counts.get('erorr_count')) + "\n" + info.get(
                'path') + "\n" + info.get('info')
            count += 1
        messagebox.showinfo("错误", error_text)


if __name__ == '__main__':

    # #win_test
    # path = ""
    # #mac_test
    path = "/Users/dengyunfei/Public/照片接收/11.29儿童"
    try:
        path = get_input_path(path)
    except:
        path = get_input_path()
    if path:
        pic_clear_up(path)
