from SelectPath import selectPathUI
from PictureSorted import pictureSorted
import os

invalidDirectory = ['未知尺寸', "@P$%#", '窄8', '方8', '方10', '16寸竖版', '相框', '琉璃', '琉璃-封面']
op = selectPathUI()
op.root.mainloop()
with os.scandir(op.paht) as it:
    for entry in it:
        print('entry:'.split(), entry.path)
        if entry.path.split('\\')[-1] in invalidDirectory:
            continue
        if not  entry.is_dir():
            continue
        for item in os.scandir(entry.path):
            if item.is_dir():
                print(item.path)
                pictureSorted(item.path)
