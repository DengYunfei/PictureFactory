import hashlib, json, os, PicClearUp, time
from PIL import Image
from shutil import copyfile

# 读取尺寸描述文件
with open("PicSizeinfo.json", 'r', encoding='utf-8') as json_file:
    picSizeinfo = json.load(json_file)


class Ke_ren():
    def __init__(self, dir, path):
        self.chan_pin = []
        self.ke_ren = {"名称": dir, "收件日期": time.strftime("%Y/%m/%d", time.localtime()), "产品列表": self.chan_pin}
        print("mainpath", self.ke_ren)
        self.path = path
        self.mainpath = path[:-len(dir)]
        # print("mainpath", self.mainpath)
        self.Fen_jian()

    def Fen_jian(self):
        count = 0
        copyright_count = 0
        erorr_count = 0
        error_info = []
        picCuunt = 0
        for root, dirs, files in os.walk(self.path):
            # 同品数量（相册P数）
            for file in files:
                if file.split('.')[-1].lower() == 'jpg':
                    picCuunt += 1
            # 分拣图片
            for file in files:
                if file.split('.')[-1].lower() == 'jpg':
                    # 仅处理*.jpg文件
                    with Image.open(os.path.join(root, file)) as img_pillow:

                        pic_size, pic_dpi = self.get_pic_size(img_pillow)  # 获得图片宽高    返回值：元组(宽，高)
                        pic_type = self.get_pic_type(pic_size)  # 获得细分品类    返回值：元组(类型，尺寸)
                    newFileName = os.path.join(root, file)[len(root) + 1:]  # 取得选择路径以后部分
                    # print("root",root)
                    print("newFileName", newFileName)
                    newFileName = newFileName.replace('/', '-')  # 非windows系统路径扁平化
                    newFileName = newFileName.replace('\\', '-')  # windows系统路径扁平化
                    if pic_type[0] == "未知尺寸":
                        # 未知尺寸产品处理
                        PicClearUp.mk_dir(os.path.join(self.mainpath, '分拣'), pic_type[0])
                        savepath = os.path.join(self.mainpath, '分拣', pic_type[0])
                    elif pic_type[0] == "相册":
                        # 相册产品处理
                        newFileNameList = newFileName.split("-")
                        newFileNameList[-1] = "★" + newFileNameList[-1]
                        newFileName = "-".join(newFileNameList)
                        newFileName = newFileName[:-4] + "_" + str(picCuunt) + ".jpg"
                        # print('type：',PicSize[0])

                        PicClearUp.mk_dir(os.path.join(self.mainpath, '分拣'), pic_type[1])
                        savepath = os.path.join(self.mainpath, '分拣', pic_type[1])
                    else:
                        # 其他产品处理
                        PicClearUp.mk_dir(os.path.join(self.mainpath, '分拣'), pic_type[0])
                        savepath = os.path.join(self.mainpath, '分拣', pic_type[0])
                        newFileName = pic_type[1] + '-' + newFileName

                    count += 1  # 计数器增加1
                    if self.diff(os.path.join(root, file), os.path.join(self.mainpath, savepath, newFileName)):
                        print(count, os.path.join(root, file), "没有改变。")
                    else:
                        # 文件不同 尝试移动文件
                        try:
                            # 移动成功
                            copyfile(os.path.join(root, file), os.path.join(self.mainpath, savepath, newFileName))
                            print(count, "文件已COPY到", os.path.join(self.mainpath, savepath, newFileName))

                            copyright_count += 1
                        except:
                            # 移动失败
                            error_info.append({'path': os.path.join(root, file), 'info': '拷贝失败'})
                            erorr_count += 1
                            print('拷贝', os.path.join(root, file), '失败')

        counts = {'count': count, 'copyright_count': copyright_count, 'erorr_count': erorr_count}
        return error_info, counts

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
