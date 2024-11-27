import selenium
import requests
import os


def get_name(num):
    names = {}
    count = 1606563775
    for i in range(1, num + 1):
        url = f"https://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={count}"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data_b = response.content
            data = data_b.decode("utf-8")
            data_core_eval = eval(data.split("(", 1)[1].rsplit(")", 1)[0])[str(count)]
            name = data_core_eval[-2]
            names[str(count)] = name
        else:
            print(f"Error: {response.status_code}")
            break
        count += 1
    print(type(names))
    names0 = [[x, y] for x, y in names.items()]
    names1 = [x for x in names.keys()]
    names2 = [x for x in names.values()]
    return names, names0, names1, names2


def save_name(names, names0, names1, names2):
    # print(names, names0, names1, names2)
    try:
        os.mkdir("../names_folder")
    except FileExistsError:
        print("已存在文件")
    with open("../names_folder/names.txt", "w", encoding="utf-8") as f:
        for key, value in names.items():
            f.write(f"{key}:{value}\n")
    print("names:保存成功")

    with open("../names_folder/names0.txt", "w", encoding="utf-8") as f:
        f.writelines(names0)
        print("names0:保存成功")

    with open("../names_folder/names1.txt", "w", encoding="utf-8") as f:
        f.writelines(names1)
        print("names1:保存成功")

    with open("../names_folder/names2.txt", "w", encoding="utf-8") as f:
        f.writelines(names2)
        print("names2:保存成功")


a, b, c, d = get_name(100)
save_name(a, b, c, d)
