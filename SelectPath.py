import tkinter as tk
from tkinter import filedialog


class selectPathUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes()
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
        self.paht = self.entry.get()
        self.root.destroy()


if __name__ == '__main__':
    op = selectPathUI()
    op.root.mainloop()

    