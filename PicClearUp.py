import os, re, KeRen, json
from tkinter import messagebox
import tkinter as tk
from tkinter import filedialog

chan_pin = []

'''
[
  {
    "客人名": "",
    "收件日期": "",
    "产品列表": [
      {
        "类型": "",
        "尺寸": "",
        "数量": "",
        "图列表": [
          "图名"
        ]
      }
    ]
  }
]
'''


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


# 创建文件夹
def mk_dir(path, file):
    if os.path.isdir(os.path.join(path, file)):
        # 要创建的文件夹已经存在
        return
    else:
        # 文件夹不存在，立即创建
        os.mkdir(os.path.join(path, file))


# 图片分拣主方法
def pic_filtrate(path):
    mk_dir(path, '分拣')
    # 遍历指定路径下所有jpg文件
    for dir in os.listdir(path):
        # 快速跳出分拣目录
        if re.search('分拣', dir):
            continue

        ke_ren = KeRen.Ke_ren(dir, path)
        chan_pin.append(ke_ren.ke_ren)
    # print()
    with open(os.path.join(path, '分拣', 'chan_pin.json'), 'w', encoding='utf-8') as json_file:
        json.dump(chan_pin, json_file, ensure_ascii=False, indent=4)


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


# def pic_clear_up(fpath):
# error_info, counts = pic_filtrate(fpath)
# 反馈运行结果
# messagebox.showinfo("成功", '共导检测到【' + str(counts.get('count')) + '】张照片\n新添加【' + str(
#     counts.get('copyright_count')) + '】张照片\n包含错误【' + str(counts.get('erorr_count')) + '】个错误')
# # 反馈错误信息
# if error_info:
#     error_text = '错误信息'
#     count = 1
#     for info in error_info:
#         error_text = error_text + '\n' + str(count) + '/' + str(counts.get('erorr_count')) + "\n" + info.get(
#             'path') + "\n" + info.get('info')
#         count += 1
#     messagebox.showinfo("错误", error_text)


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
        pic_filtrate(path)
