import json
key_list = []
with open('PicSizeinfo.json','r',encoding='utf8') as js_f:
    my_dict = json.load(js_f)

for key in my_dict.keys():
    for a in my_dict.get(key):
        print(a)