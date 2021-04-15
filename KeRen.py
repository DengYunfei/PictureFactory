import hashlib, json, os, PicClearUp, time, re
from PIL import Image
from shutil import copyfile

# 读取尺寸描述文件
with open("PicSizeinfo.json", 'r', encoding='utf-8') as json_file:
    picSizeinfo = json.load(json_file)


class Ke_ren():
    def __init__(self, u_dir, u_path):
        self.chan_pin = []
        self.path = u_path
        self.dir = os.path.join(self.path, u_dir)
        # self.mainpath = u_path[:-len(u_dir)]
        # print("mainpath", self.mainpath)
        self.qing_di_zhi = ""
        self.csvList = []
        self.csv = [u_dir, "", time.strftime("%Y/%m/%d", time.localtime()), "", "", "", ""]
        self.Fen_jian()
        self.ke_ren = {"名称": u_dir, "收件日期": time.strftime("%Y/%m/%d", time.localtime()), "产品列表": self.chan_pin}

        # print("mainpath", self.ke_ren)

    def Fen_jian(self):
        self.count = 0
        self.CopyRight_count = 0
        self.CopyError_count = 0
        self.error_info = []
        if os.path.isfile(self.dir):
            if self.dir.split('.')[-1].lower() == 'jpg':
                self.picCount = 1
                self.Img_ChuLi(self.dir)
        else:
            for root, dirs, files in os.walk(self.dir):
                self.picCount = 0
                self.root = os.path.split(root)
                # 同品数量（相册P数）
                for file in files:
                    if file.split('.')[-1].lower() == 'jpg':
                        self.picCount += 1
                # 分拣图片
                for file in files:
                    if file.split('.')[-1].lower() == 'jpg':
                        # 仅处理*.jpg文件
                        self.Img_ChuLi(os.path.join(root, file))

    # 处理图片去向
    def Img_ChuLi(self, file):
        root = os.path.split(file)[0]
        with Image.open(file) as img_pillow:
            pic_size, pic_dpi = self.get_pic_size(img_pillow)  # 获得图片宽高    返回值：元组(宽，高)
            pic_type = self.get_pic_type(pic_size)  # 获得细分品类    返回值：元组(类型，尺寸)
            # img_pillow.show()
        newFileName = file[len(self.path) + 1:]  # 取得选择路径以后部分
        # print("root", root)
        newFileName = newFileName.replace('/', '-')  # 非windows统路径扁平化
        newFileName = newFileName.replace('\\', '-')  # windows系统路径扁平化

        savepath, newFileName = self.Fen_lei(pic_type, newFileName)

        # print("newFileName", newFileName)
        self.count += 1  # 计数器增加1
        self.qing_di_zhi = os.path.split(root)
        # print("qing_di_zhi", self.qing_di_zhi)
        if self.diff(os.path.join(root, file), os.path.join(self.path, savepath, newFileName)):
            print(self.count, os.path.join(root, newFileName), "没有改变。")
        else:
            # 文件不同 尝试移动文件
            try:
                # 移动成功
                copyfile(os.path.join(root, file), os.path.join(self.path, savepath, newFileName))
                print(self.count, "文件已COPY到", os.path.join(self.path, savepath, newFileName))

                self.CopyRight_count += 1
            except:
                # 移动失败
                self.error_info.append({'path': os.path.join(root, file), 'info': '拷贝失败'})
                self.CopyError_count += 1
                print('拷贝', os.path.join(root, file), '失败')

    # 获取图片的宽高数据
    def get_pic_size(self, img):
        dpi = img.info.get("dpi")

        if not dpi:
            dpi = (254, 254)
        width = img.width / dpi[0] * 2.54
        height = img.height / dpi[0] * 2.54
        size = (width, height)

        return size, dpi[0]

    # 获取图片宽高所对应的尺寸类别
    def get_pic_type(self, sized):
        compensation = 0.5
        for items in picSizeinfo:
            for size in picSizeinfo[items]:
                if sized[0] > size.get("width") - compensation and sized[0] < size.get("width") + compensation:
                    if sized[1] > size.get("height") - compensation and sized[1] < size.get("height") + compensation:
                        return items, size["name"], (size.get("width"), size.get("height"))

        return "未知尺寸", str(sized[0]) + "x" + str(sized[1]), sized

    # 判断两个文件是否相同
    def diff(self, file_1, file_2):
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

    # 图片产品分类
    def Fen_lei(self, pic_type, newFileName):
        newCSV = self.csv.copy()
        newCSV[3] = pic_type[0]
        if pic_type[0] == "未知尺寸":
            # 未知尺寸产品处理
            PicClearUp.mk_dir(os.path.join(self.path, '分拣'), pic_type[0])
            savepath = os.path.join(self.path, '分拣', pic_type[0])
            self.chan_pin.append(
                {"类型": pic_type[0], "尺寸": pic_type[1], "数量": self.picCount,
                 "保存位置": os.path.join(self.path, '分拣', pic_type[0]),
                 "图片列表": [newFileName]})
            chackOver = csvCheck(newCSV,self.dir).csv_t
            self.csvList.append(chackOver)

        elif pic_type[0] == "相册":
            # 相册产品处理
            newFileNameList = newFileName.split("-")
            newFileNameList[-1] = "★" + newFileNameList[-1]
            newFileName = "-".join(newFileNameList)
            newFileName = newFileName[:-4] + "_" + str(self.picCount) + ".jpg"
            # print('type：',PicSize[0])

            PicClearUp.mk_dir(os.path.join(self.path, '分拣'), pic_type[1])
            savepath = os.path.join(self.path, '分拣', pic_type[1])
            if not self.qing_di_zhi == self.root:
                self.chan_pin.append(
                    {"类型": pic_type[0], "尺寸": pic_type[1], "数量": self.picCount,
                     "保存位置": os.path.join(self.path, '分拣', pic_type[0]),
                     "图片列表": [newFileName]})
                newCSV[5] = pic_type[1]
                newCSV[6] = self.picCount
                chackOver = csvCheck(newCSV,self.dir).csv_t
                self.csvList.append(chackOver)
            else:
                self.chan_pin[-1].get("图片列表").append(newFileName)

        elif pic_type[0] == "台历":
            PicClearUp.mk_dir(os.path.join(self.path, '分拣'), pic_type[0])
            savepath = os.path.join(self.path, '分拣', pic_type[0])
            newFileName = pic_type[1] + '-' + newFileName
            if not self.qing_di_zhi == self.root:
                self.chan_pin.append(
                    {"类型": pic_type[0], "尺寸": pic_type[1], "数量": self.picCount,
                     "保存位置": os.path.join(self.path, '分拣', pic_type[0]),
                     "图片列表": [newFileName]})
                newCSV[5] = pic_type[1]
                newCSV[6] = self.picCount
                newCSV[4] = "实木"
                self.csvList.append(newCSV)
            else:
                self.chan_pin[-1].get("图片列表").append(newFileName)

        else:
            # 其他产品处理
            PicClearUp.mk_dir(os.path.join(self.path, '分拣'), pic_type[0])
            savepath = os.path.join(self.path, '分拣', pic_type[0])
            newFileName = pic_type[1] + '-' + newFileName
            self.chan_pin.append(
                {"类型": pic_type[0], "尺寸": pic_type[1], "数量": self.picCount,
                 "保存位置": os.path.join(self.path, '分拣', pic_type[0]),
                 "图片列表": [newFileName]})
            newCSV[5] = pic_type[1][:-2]
            newCSV[6] = 1
            chackOver = csvCheck(newCSV,self.dir).csv_t
            self.csvList.append(chackOver)
        # print("csv=",newCSV)
        return savepath, newFileName


class csvCheck():
    def __init__(self, csv_t,path=""):
        self.csv_t = csv_t
        self.path = path
        self.nameCheck()
        self.chanPinChack()
        print("csv",self.csv_t)


    def nameCheck(self):
        deltxtlist = ["制作", "不看", "看板", "（刚）", "（", "）", "(", ")", "_", " ",".","1","2","3","4","5","6","7","8","9","0"]
        name = self.csv_t[0]
        for i in deltxtlist:
            name = name.replace(i, "")
        self.csv_t[0] = name

    def chanPinChack(self):
        if self.csv_t[3] == "相册":
            if self.csv_t[5] == "方10":
                if re.search('薄', self.path):
                    self.csv_t[4] ="超薄"
                elif re.search('水泥', self.path):
                    self.csv_t[4] ="水泥灰"
                else:
                    self.csv_t[4] ="普通册"

            elif self.csv_t[5] == "方8":
                if re.search('蓝', self.path):
                    self.csv_t[4] ="蓝色"
                elif re.search('粉', self.path):
                    self.csv_t[4] ="粉色"
                elif re.search('水泥', self.path):
                    self.csv_t[4] ="水泥灰"
                elif re.search('灰', self.path):
                    self.csv_t[4] ="399套（灰）"
                else:
                    self.csv_t[4] ="普通册"

            elif self.csv_t[5] == "窄8" or self.csv_t[5] == "8寸琉璃":
                if re.search('蓝', self.path):
                    self.csv_t[4] ="蓝色"
                elif re.search('粉', self.path):
                    self.csv_t[4] ="粉色"
                elif re.search('琉璃', self.path):
                    self.csv_t[4] ="琉璃"
                elif re.search('水晶', self.path):
                    self.csv_t[4] = "琉璃"
                else:
                    self.csv_t[4] ="普通册"

            elif self.csv_t[5] == "16寸":
                self.csv_t[4] ="白色"

            elif self.csv_t[5] == "12寸":
                if re.search('水晶', self.path):
                    self.csv_t[4] ="琉璃"
                elif re.search('琉璃', self.path):
                    self.csv_t[4] ="琉璃"
                else:
                    self.csv_t[4] ="普通册"

        elif self.csv_t[3] == "摆台":
            if self.csv_t[5] == "方10":
                self.csv_t[4] = "板画"
            elif self.csv_t[5] == "8寸":
                if re.search('灰', self.path):
                    self.csv_t[4] ="399套（灰）"
                elif re.search('绿', self.path):
                    self.csv_t[4] ="初音"
                else:
                    self.csv_t[4] ="芳华"
            elif self.csv_t[5] == "10寸":
                self.csv_t[4] ="芳华"
            elif self.csv_t[5] == "大10寸":
                self.csv_t[4] ="芳华"

        elif self.csv_t[3] == "放大":
            if self.csv_t[5] == "20寸":
                if re.search('灰', self.path):
                    self.csv_t[4] ="399套（灰）"
                elif re.search('绿', self.path):
                    self.csv_t[4] ="初音"
                else:
                    self.csv_t[4] ="芳华"
            elif self.csv_t[5] == "窄30寸":
                self.csv_t[4] ="水泥灰"
            elif self.csv_t[5] == "32寸":
                self.csv_t[4] ="实木"
            elif self.csv_t[5] == "24寸":
                self.csv_t[4] ="巧克力"

if __name__ == '__main__':
    test = ["1 2 3 4 5 6", "", time.strftime("%Y/%m/%d", time.localtime()), "", "", "", ""]
    a = csvCheck(test)
