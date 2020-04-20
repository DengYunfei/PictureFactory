from SelectPath import selectPathUI
from PictureSorted import pictureSorted
import os
import re

# invalidDirectory = ['未知尺寸', "@P$%#", '窄8', '方8', '方10', '16寸竖版', '相框', '琉璃', '琉璃-封面']
op = selectPathUI()
op.root.mainloop()  #显示获取路径窗体
with os.scandir(op.paht) as it:
    for entry in it:
        # print('entry:'.split(), entry.path)
        if re.search('分拣', entry.path):
            # 快速跳出分拣目录
            continue
        if not entry.is_dir():
            #该层文件视为无效，跳过
            continue
        for item in os.scandir(entry.path):
            #影楼文件夹
            if item.is_dir():
                #客人文件夹
                # print(item.path)
                pictureSorted(item.path)    #调用风格输入方法
