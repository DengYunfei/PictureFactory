userList = []


class user():

    def __init__(self, info):
        self.products = []
        self.product = {}
        self.name = info.get("name")
        self.files = []

    def mainJson(self):
        pass

    def set_product(self):
        pass



def chachong(user):
    for _user in userList:
        if user.get("name") == _user.name:
            print("找到了")
            return


if __name__ == '__main__':
    info = {"name": "邓云飞", "studio": "埃尔沃克", "date": "2020-11-11", "isOK": False, "outDate": None,
            "products": [{"type": "相册", "style": "初音", "size": "方8", "count": "10", "images": ["", ""]}]}
    chachong(info)
    play_a = user(info)
    userList.append(play_a)

    chachong(info)
