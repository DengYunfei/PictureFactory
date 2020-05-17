import tkinter as tk
from tkinter import filedialog
from PictureSorted import pictureSorted
import os, re


class SetMeal_UI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("设置套系")
        self.root.attributes()
        self.path =""
        self.root.geometry('480x120')
        self.root.resizable(0, 0)  # 防止用户调整尺寸
        self._setpage()

    def _setpage(self):
        self.label = tk.Label(self.root, text='请选择日期文件夹', anchor="w")
        self.btn1 = tk.Button(self.root, text='...', command=self.chooseDir)
        self.btn2 = tk.Button(self.root, text='确认', command=self.enterPath)
        self.entry = tk.Entry(self.root)

        # 绘制窗口控件

        self.label.place(relx=0.01, rely=0.1, relwidth=0.5, relheight=0.2)
        self.btn1.place(relx=0.84, rely=0.4, relwidth=0.15, relheight=0.2)
        self.entry.place(relx=0.01, rely=0.4, relwidth=0.82, relheight=0.2)
        self.btn2.place(relx=0.4, rely=0.7, relwidth=0.15, relheight=0.2)

    def chooseDir(self):
        Fpath = filedialog.askdirectory()
        self.entry.insert(0, Fpath)

    def enterPath(self):
        self.path = self.entry.get()
        self.root.destroy()


# invalidDirectory = ['未知尺寸', "@P$%#", '窄8', '方8', '方10', '16寸竖版', '相框', '琉璃', '琉璃-封面']
def set_meal():
    op = SetMeal_UI()
    op.root.mainloop()  # 显示获取路径窗体
    if op.path:
        with os.scandir(op.path) as it:
            for entry in it:
                # print('entry:'.split(), entry.path)
                if re.search('分拣', entry.path):
                    # 快速跳出分拣目录
                    continue
                if not entry.is_dir():
                    # 该层文件视为无效，跳过
                    continue
                for item in os.scandir(entry.path):
                    # 影楼文件夹
                    if item.is_dir():
                        # 客人文件夹
                        # print(item.path)
                        pictureSorted(item.path)  # 调用风格输入方法


if __name__ == '__main__':
    op = SetMeal_UI()
    op.root.mainloop()
