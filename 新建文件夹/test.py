from PIL import Image

def check_Pic(img):
    try:
        if 'icc_profile' not in img.info:
            # txt = "%s没有icc信息" % img.filename
            # img.transform_colorspace('RGB')
            return img.filename

    except:
        return False


# 获取图片的宽高数据
def get_pic_size(img):
    size = (img.width, img.height)
    return size
    return "未知尺寸", str(sized[0]) + "x" + str(sized[1])


with Image.open("MainCityMap.jpg") as img_pillow:
    print(img_pillow.info)
    # pic_size = get_pic_size(img_pillow)  # 获得图片宽高    返回值：元组(宽，高)
    # pic_type = get_pic_type(pic_size)  # 获得细分品类    返回值：元组(类型，尺寸)
    # icc_info = check_Pic(img_pillow)
    # print("icc_info:",type(icc_info))
    # with Image.open("MainCityMap-icc.jpg") as img_icc:
    #     print(img_pillow.info)
    img_pillow.save("New_MainCityMap.jpg", 'jpeg', icc_profile=img_pillow.info.get('icc_profile'))