import time, re, json, os


class JsonToCsv():
    def __init__(self, inputJson):
        self._mJson = inputJson
        self.csv_t = []

        self.fenRen()

    def csvFormat(self, ren):
        renCsv = []
        newCsv = ["客人名", "", "收件时间戳", "产品类型", "风格", "尺寸", "数量", "图片名"]
        newCsv[0] = self.nameCheck(ren.get("名称"))
        newCsv[2] = ren.get("收件日期")
        for _mchanPin in ren.get("产品列表"):
            s = _mchanPin
            isFangHua = False
            if s.get("类型") == "放大" and s.get("20寸"):
                isFangHua = True

        for _mchanPin in ren.get("产品列表"):
            s = _mchanPin
            newCsv[3] = s.get("类型")
            size = self.sizeCheck(s.get("尺寸"))
            newCsv[5] = size
            newCsv[6] = s.get("数量")
            newCsv[7] = s.get("图片列表")[0]
            fileName = os.path.join(s.get("保存位置"), s.get("图片列表")[0])
            if s.get("类型") == "相册":
                _fengGe = self.xiangCeCheck(size, fileName, isFangHua)
            elif s.get("类型") == "摆台":
                _fengGe = self.baiTaiCheck(size, fileName)
            elif s.get("类型") == "放大":
                _fengGe = self.fangDaCheck(size, fileName)
            elif s.get("类型") == "台历":
                if len(s.get("图片列表")) >= 6:
                    _fengGe = "实木"
                else:
                    _fengGe = self.baiTaiCheck(s.get("尺寸"), fileName)
            else:
                _fengGe = "未知尺寸"
            newCsv[4] = _fengGe
            renCsv.append(newCsv.copy())
        # print(renCsv)

        self.csv_t.append(renCsv)

    def nameCheck(self, txt):
        deltxtlist = ["制作", "不看", "看板", "（刚）", "（", "）", "(", ")", "_", " ", ".", "1", "2", "3", "4", "5", "6", "7",
                      "8", "9", "0"]
        name = txt
        for i in deltxtlist:
            name = name.replace(i, "")
        return name

    # 尺寸
    def sizeCheck(self, size):
        return size.split("-")[0]

    def xiangCeCheck(self, size, name, isFangHua):
        if size == "方10":
            if re.search('薄', name):
                return "超薄"
            elif re.search('水泥', name):
                return "水泥灰"
            elif isFangHua:
                return "芳华"
            else:
                return "普通册"

        elif size == "方8":
            if re.search('蓝', name):
                return "蓝色"
            elif re.search('兰', name):
                return "蓝色"
            elif re.search('粉', name):
                return "粉色"
            elif re.search('水泥', name):
                return "水泥灰"
            elif re.search('灰', name):
                return "399套（灰）"
            else:
                return "普通册"

        elif size == "窄8" or size == "8寸琉璃":
            if re.search('蓝', name):
                return "蓝色"
            elif re.search('兰', name):
                return "蓝色"
            elif re.search('粉', name):
                return "粉色"
            elif re.search('琉璃', name):
                return "琉璃"
            elif re.search('水晶', name):
                return "琉璃"
            else:
                return "普通册"

        elif size == "16寸":
            return "白色"

        elif size == "12寸":
            if re.search('水晶', name):
                return "琉璃"
            elif re.search('琉璃', name):
                return "琉璃"
            else:
                return "普通册"

    # 摆台
    def baiTaiCheck(self, size, name):
        if size == "方10":
            return "板画"
        elif size == "8寸":
            if re.search('灰', name):
                return "399套（灰）"
            elif re.search('绿', name):
                return "初音"
            else:
                return "芳华"
        elif size == "10寸" or size == "大10寸":
            if re.search('水晶', name):
                return "板画"
            if re.search('板画', name):
                return "板画"
            if re.search('版画', name):
                return "板画"
            return "芳华"
        else:
            return "？？？？？？"

    # 放大
    def fangDaCheck(self, size, name):
        if size == "20寸":
            if re.search('灰', name):
                return "399套（灰）"
            elif re.search('绿', name):
                return "初音"
            else:
                return "芳华"
        elif size == "窄30寸":
            return "水泥灰"
        elif size == "32寸":
            return "实木"
        elif size == "24寸":
            return "巧克力"

    # 拆分第一层，用户分类
    def fenRen(self):
        for ren in self._mJson:
            self.user = ren
            self.csvFormat(ren)


if __name__ == '__main__':
    with open("chan_pin_4.17.json", "r", encoding="utf-8") as chanPinJSON:
        chanPin = json.load(chanPinJSON)
    JsonToCsv(chanPin)
    test = ["1 2 3 4 5 6", "", time.strftime("%Y/%m/%d", time.localtime()), "", "", "", ""]
    # a = csvCheck(test)
