from SelectPath import selectPathUI
from PictureSorted import pictureSorted
import os

op = selectPathUI()
op.root.mainloop()
with os.scandir(op.paht) as it:
    for entry in it:
        for item in os.scandir(entry.path):
            if item.is_dir():
                print(item.path)
                pictureSorted(item.path)