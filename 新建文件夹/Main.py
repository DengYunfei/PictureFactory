import PIL as Image
import os
import numpy as np

str = '摇'

ascii = np.fromstring(str, dtype=np.uint8)

print(ascii)
# 遍历指定路径下所有jpg文件
path = "text"
for root, dir, files in os.walk(path):
    for file in files:
        print(file.split(".")[0],ord(file.split(".")[0]))
