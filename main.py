import tkinter as tk
from PicClearUp import pic_clear_up
from SetMeal import set_meal

class main_UI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("图片工厂")
        self.root.attributes()
        self.root.geometry('640x480')
        self.root.resizable(0, 0)  # 防止用户调整尺寸
        self._setpage()

    def _setpage(self):

        self.btn1 = tk.Button(self.root, text='设置套系', command=self.set_meal)
        self.btn2 = tk.Button(self.root, text='图片分拣', command=self.pic_clear_up)
        self.btn3 = tk.Button(self.root, text='图片裁剪', command=self.pic_clear_up)
        self.entry = tk.Entry(self.root)

        # 绘制窗口控件

        self.btn1.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.2)
        self.btn2.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.2)
        self.btn3.place(relx=0.05, rely=0.3, relwidth=0.4, relheight=0.2)

    def set_meal(self):
        set_meal()

    def pic_clear_up(self):
        pic_clear_up()

if __name__ == '__main__':
    op = main_UI()
    op.root.mainloop()
