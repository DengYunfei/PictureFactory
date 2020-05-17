import datetime
import json
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image

from MySQL import MySQL
with open('PicSizeinfo.json', 'r', encoding='utf-8') as Jfile:
    sizeInfo = json.load(Jfile)
    sizename = {"相册": [], "摆台": [], "放大": [], "台历": []}
    for a in sizeInfo:
        for b in sizeInfo[a]:
            sizename[a].append(b["name"])
    # print(sizename["相册"])

with open('PriceList.json', 'r', encoding='utf-8') as Jfile:
    PriceList = json.load(Jfile)
    combination = {"相册": [], "摆台": [], "放大": [], "其他": []}
    for a in PriceList:
        for a_key in a.keys():
            if a_key == "相册":
                combination["相册"].append(a["套系"])
            elif a_key == "摆台":
                combination["摆台"].append(a["套系"])
            elif a_key == "放大":
                combination["放大"].append(a["套系"])
            elif a_key == "套系":
                pass
            else:
                combination["其他"].append(a["套系"])
    # print(combination)


class pictureSortedUI():
    def __init__(self):
        print(pictureSorted.userList[-1].products)
        self.root = tk.Tk()
        self.root.title(pictureSorted.userList[-1].userName)
        self.root.attributes()
        self.root.geometry('640x480')
        self.root.resizable(0, 0)  # 防止用户调整尺寸
        self._setpage()
        self.root.update()  # 必须
        self.set_win_center()

    def _setpage(self):
        # print(len(pictureSorted.userList[-1].products))
        # x = 0
        self.comboxlists = []
        self.frames = []
        self.label_0 = tk.Label(self.root, text=pictureSorted.userList[-1].userName, anchor="w")
        self.label_0_1 = tk.Label(self.root, text=len(pictureSorted.userList))
        self.label_0_2 = tk.Label(self.root, text='客户性别', anchor="e")
        self.comvalue = tk.StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = ttk.Combobox(self.root, values=("王子", "公主"))
        # self.comboxlist.current(x)
        self.label_0.place(relx=.01, rely=.01, relwidth=0.5, relheight=0.05)
        self.label_0_1.place(relx=.45, rely=.01, relwidth=0.1, relheight=0.05)
        self.label_0_2.place(relx=.59, rely=.01, relwidth=0.2, relheight=0.05)
        self.comboxlist.place(relx=.79, rely=.01, relwidth=0.2, relheight=0.05)
        for frame in range(len(pictureSorted.userList[-1].products)):
            self.frames.append(tk.LabelFrame(self.root))
            self.frames[-1].place(relx=.01, rely=.07 + frame * .1, relwidth=0.98, relheight=0.10)
            self.label_1_1 = tk.Label(self.frames[-1], text='请选择产品套系', anchor="w")
            self.label_1_1.place(relx=0.01, rely=0.05, relwidth=0.19, relheight=0.45)
            self.list = pictureSorted.userList[-1].products[frame].combination
            print(pictureSorted.userList[-1].products[frame].combination)
            self.comvalue_1 = tk.StringVar()  # 窗体自带的文本，新建一个值
            self.comboxlist_1_2 = ttk.Combobox(self.frames[-1], values=self.list)
            self.comboxlists.append(self.comboxlist_1_2)
            # self.comboxlist_1_2.current(x)
            self.comboxlist_1_2.place(relx=0.01, rely=0.5, relwidth=0.16, relheight=0.5)
            self.label_2_1 = tk.Label(self.frames[-1], text='产品类型')
            self.label_2_1.place(relx=.17, rely=0.05, relwidth=0.16, relheight=0.45)
            self.label_2_2 = tk.Label(self.frames[-1], text=pictureSorted.userList[-1].products[frame].product["type"])
            self.label_2_2.place(relx=.17, rely=0.5, relwidth=0.16, relheight=0.45)
            self.label_3_1 = tk.Label(self.frames[-1], text='产品尺寸')
            self.label_3_1.place(relx=.34, rely=0.05, relwidth=0.16, relheight=0.45)
            self.label_3_2 = tk.Label(self.frames[-1],
                                      text=str(pictureSorted.userList[-1].products[frame].product["size"][0]) + 'x' +
                                           str(pictureSorted.userList[-1].products[frame].product["size"][1]))
            self.label_3_2.place(relx=.34, rely=0.5, relwidth=0.16, relheight=0.45)
            self.label_4_1 = tk.Label(self.frames[-1], text='尺寸别名')
            self.label_4_1.place(relx=.51, rely=0.05, relwidth=0.16, relheight=0.45)
            self.label_4_2 = tk.Label(self.frames[-1],
                                      text=pictureSorted.userList[-1].products[frame].product["category"])
            self.label_4_2.place(relx=.51, rely=0.5, relwidth=0.16, relheight=0.45)
            self.label_5_1 = tk.Label(self.frames[-1], text='数量')
            self.label_5_1.place(relx=.68, rely=0.05, relwidth=0.16, relheight=0.45)
            self.label_5_2 = tk.Label(self.frames[-1], text=pictureSorted.userList[-1].products[frame].product["count"])
            self.label_5_2.place(relx=.68, rely=0.5, relwidth=0.16, relheight=0.45)
            path = pictureSorted.userList[-1].products[frame].product["files"][0]["Path"]
            self.btn_showImg = tk.Button(self.frames[-1], text='显示图片', command=lambda arg=path: self.showImg(arg))
            self.btn_showImg.place(relx=.85, rely=0.25, relwidth=0.14, relheight=0.5)
            # self.label_1 = tk.Label(self.frames[-1], text=pictureSorted.userList[-1].products[a]["type"])
            # self.label_2 = tk.Label(self.frames[-1], text='x'.join(pictureSorted.userList[-1].products[a]["size"]))
            # self.entry = tk.Entry(self.frames[-1])
            # self.entry.grid(row=1, column=1, sticky=W)
            # 绘制窗口控件

        self.btn_save = tk.Button(self.root, text='保存', command=self.save_sorted)
        self.btn_save.place(relx=0.45, rely=0.94, relwidth=0.1, relheight=0.05)

    # 窗口居中显示
    def set_win_center(self, curWidth='', curHight=''):
        '''
        设置窗口大小，并居中显示
        :param root:主窗体实例
        :param curWidth:窗口宽度，非必填，默认200
        :param curHight:窗口高度，非必填，默认200
        :return:无
        '''
        if not curWidth:
            '''获取窗口宽度，默认200'''
            curWidth = self.root.winfo_width()
        if not curHight:
            '''获取窗口高度，默认200'''
            curHight = self.root.winfo_height()
        # print(curWidth, curHight)

        # 获取屏幕宽度和高度
        scn_w, scn_h = [1280, 800]
        # print(scn_w, scn_h)

        # 计算中心坐标
        cen_x = (scn_w - curWidth) / 2
        cen_y = (scn_h - curHight) / 2
        # print(cen_x, cen_y)

        # 设置窗口初始大小和位置
        size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
        # print(size_xy)
        self.root.geometry(size_xy)

    def save_sorted(self):
        a = 0
        for comboxlist in self.comboxlists:
            if comboxlist.get():
                pictureSorted.userList[-1].products[a].product["setmeal"] = comboxlist.get()
            else:
                pictureSorted.userList[-1].products[a].product["setmeal"] = '未知套系'
            a += 1
            print(comboxlist.get())
        self.root.destroy()

    def showImg(self, path):
        with Image.open(path) as img:
            if img.width > img.height:
                new_w = 1500
                new_h = int(img.height * 1500 / img.width)
            else:
                new_h = 800
                new_w = int(img.width * 800 / img.height)
            img_deal = img.resize((new_w, new_h), Image.ANTIALIAS)
            img_deal.show()


class product():
    def __init__(self, path):

        # self.path = path
        self.product = {}
        self.product["files"] = []
        self.file = {}
        self.product["count"] = 0
        if os.path.isdir(path):
            # 相册或台历产品
            for item in os.scandir(path):
                if item.name.split('.')[-1].lower() == "jpg":
                    self.product["size"] = self.get_picSize(item.path)
                    self.product["category"] = self.get_Sizename(self.product["size"])
                    self.product["checkPic"] = self.check_Pic(item.path)
                    self.product["count"] += 1
                    self.file["checkPic"] = self.check_Pic(item.path)
                    self.file["Path"] = item.path
                    self.product["files"].append(self.file)

                    # print(self.product["size"])
            if self.product["category"].split('-')[0] == "相册":
                self.product["type"] = '相册'
            else:
                self.product["type"] = '台历'
                self.product["category"] = "-".join((self.product["type"], self.product["category"].split('-')[1]))


        else:
            # 放大、摆台、其他产品
            self.product["size"] = self.get_picSize(path)
            self.product["category"] = self.get_Sizename(self.product["size"])
            self.product["type"] = self.product["category"].split('-')[0]
            self.product["count"] = 1
            self.file["checkPic"] = self.check_Pic(path)
            self.file["Path"] = path
            self.product["files"].append(self.file)

        self.combination = self.get_combinationList()

    def check_Pic(self, path):
        return True

    def get_picSize(self, path):
        with Image.open(path) as pic:
            return [pic.width, pic.height]

    def get_Sizename(self, sized):
        for items in sizeInfo:
            for size in sizeInfo[items]:
                if sized[0] >= size["width"] and sized[0] <= size["width"] + 100:
                    if sized[1] >= size["height"] and sized[1] <= size["height"] + 100:
                        return items + '-' + size["name"]

        return "未知尺寸"

    def get_combinationList(self):
        combination = []
        for a in PriceList:
            if self.product["type"] in a.keys():
                for b in a[self.product["type"]]:
                    if self.product["category"].split('-')[1] == b["尺寸"]:
                        combination.append(a["套系"])
            # print(combination)
        return combination


class pictureSorted():
    userList = []

    def __init__(self, path):
        self.userPath = path.replace("\\", "/")
        self.sizeInfo = sizeInfo
        self.userName = self.userPath.split('/')[-1]
        self.products = []
        self.clientDict = {}
        self.userList.append(self)
        self.viewProduct()
        self.gatjson()
        # self.write_MySQL()
        self.save_pictureSorted()

    def viewProduct(self):
        invalidDirectory = ['未知尺寸', "@P$%#"]
        for item in os.scandir(self.userPath):

            # 制作忽略目录列表
            if item.name in invalidDirectory:
                continue
            if item.is_dir():
                self.products.append(product(item.path))
            if item.name.split('.')[-1].lower() != "jpg":
                continue
            self.products.append(product(item.path))
        # print(self.products)
        self.op = pictureSortedUI()
        self.op.root.mainloop()

    def save_pictureSorted(self):
        with open(self.userName + '.json', "w", encoding='utf-8') as jfile:
            json.dump(self.clientDict, jfile, ensure_ascii=False)

    def gatjson(self):
        print('12345363', self.userPath)
        self.clientDict['studio'] = self.userPath.split("/")[-2]
        self.clientDict['client_path'] = '/'.join(self.userPath.split('/')[-3:])
        self.clientDict['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(self.clientDict.get('date'))
        self.clientDict['client'] = self.userPath.split("/")[-1]
        self.clientDict['productCount'] = len(self.products)
        self.clientDict['products'] = []
        for product in self.products:
            self.clientDict['products'].append(product.product)

    def write_MySQL(self):
        print(self.clientDict.get('studio'))
        if not MySQL("select studio_id from studio where studio_name = '%s'" % (self.clientDict.get('studio'))):
            MySQL(
                "INSERT INTO studio ( factory_id,studio_name,studio_number,studio_address)VALUES( 1, '%s','','' )" % (
                    self.clientDict.get('studio')))

        studio_id = MySQL("select studio_id from studio where studio_name = '%s'" % (self.clientDict.get('studio')))
        print(studio_id)
        if not MySQL("select client_id from client where client_name = '%s'" % (self.clientDict.get('client'))):
            MySQL(
                "INSERT INTO client ( studio_id,client_name,client_path,product_count,date_created)VALUES\
                (%d,'%s','%s',%d,str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%s'))" % (studio_id[0].get('studio_id'),
                                                                                  self.clientDict.get('client'),
                                                                                  self.clientDict.get('client_path'),
                                                                                  self.clientDict.get('productCount'),
                                                                                  self.clientDict.get('date')))
        client = MySQL(
            "select client_id from client where client_name = '%s'" % (self.clientDict.get('client')))

        for a in self.clientDict.get('products'):
            # print('a:', a['files'][0].get('Path').split('/')[-5:-1])
            if len(a.get('files')) == 1:
                MySQL(
                    "INSERT INTO products ( factory_id,client_id,product_path,product_style,product_type,product_size,\
                    pic_count,date_created)VALUES( 1, %d,'%s','%s','%s','%s',%d, str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%s'))"
                    % (client[0].get('client_id'), '/'.join(a.get('files')[0].get('Path').split('/')[-4:-1]),
                       a.get("setmeal"),
                       a.get("type"), a.get("category"), a.get("count"),
                       datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                products = MySQL('select product_id from products order by product_id desc limit 1')
                MySQL(
                    "INSERT INTO picture ( products_id,pic_width,pic_height,pic_path)VALUES( %d, %d,%d,'%s')" % (
                        products[0].get('product_id'), a.get("size")[0], a.get("size")[1],
                        '/'.join(a.get('files')[0].get('Path').split('/')[-4:])))
            else:
                MySQL(
                    "INSERT INTO products ( factory_id,client_id,product_path,product_style,product_type,product_size,\
                    pic_count,date_created)VALUES( 1, %d,'%s','%s','%s','%s',%d, str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%s'))"
                    % (client[0].get('client_id'), '/'.join(a.get('files')[0].get('Path').split('/')[-5:-1]),
                       a.get("setmeal"),
                       a.get("type"), a.get("category"), a.get("count"),
                       datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                products = MySQL('select product_id from products order by product_id desc limit 1')
                for b in a.get('files'):
                    MySQL(
                        "INSERT INTO picture ( products_id,pic_width,pic_height,pic_path)VALUES( %d, %d,%d,'%s')" % (
                            products[0].get('product_id'), a.get("size")[0], a.get("size")[1],
                            '/'.join(b.get('Path').split('/')[-5:])))
        pass


if __name__ == '__main__':
    pathList = ["/Users/dengyunfei/Public/PycharmProjects/2020.04.17/埃尔沃克/3.22 苏莉薪 选不看（金）"
                ]
    for path in pathList:
        user = pictureSorted(path)
    for user in user.userList:
        print(user.userPath, user.products)
