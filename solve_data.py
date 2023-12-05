"""
Author: jason
Date: 2023-11-06 18:24:59
LastEditTime: 2023-11-06 19:46:23
LastEditors: jason
Description: 
"""
class_file_path = "classes.txt"


def Split_strings(strings, key=","):
    string_list = strings.split(key)
    string_list_length = len(string_list)
    return string_list_length, string_list


def dict_former(path):
    dict_ret = {}
    fp = open(path, "r", encoding="utf")
    classes = fp.readlines()
    for i in range(0, len(classes)):
        dict_ret.update({str(i): classes[i].replace("\n", "")})
    # print(dict_ret)
    return dict_ret

def class_dict_former(path=class_file_path):
    dict_ret = {}
    fp = open(path, "r", encoding="utf")
    classes = fp.readlines()
    for i in range(0, len(classes)):
        dict_ret.update({str(i+10): classes[i].replace("\n", "")})
    # print(dict_ret)
    return dict_ret

class_dict = class_dict_former()


def map_garbage_type(code):
    garbage_types = {
        "A": "可回收垃圾",
        "B": "其它垃圾",
        "C": "有害垃圾",
        "D": "厨余垃圾",
        "E": "无垃圾",
    }
    return garbage_types.get(code, "未知类型")


def map_type_code(garbage_type):
    waste_type_mapping = {
        "有害垃圾": "A",
        "可回收垃圾": "B",
        "厨余垃圾": "C",
        "其它垃圾": "D",
        "无垃圾": "E",
    }
    return waste_type_mapping.get(garbage_type)


def map_if_complished(code):
    map_if_complished = {
        "1": "分类已完成",
        "0": "分类未完成",
    }
    return map_if_complished.get(code, "未知分类状态")


def map_item(code:str):
    global class_dict
    return class_dict.get(code, "无垃圾")


def solve_data_1(string_list_length, string_list):
    if string_list_length == 3:
        # 在这里可以处理 string_list 中的数据
        bintype_element = string_list[0]
        item_element = string_list[1]
        num_element = string_list[2]
        # 进行操作，比如将字符串转换为整数
        try:
            bintype_element_str = map_garbage_type(bintype_element)
            item_element_str = map_item(item_element)
            num_element_int = num_element
        except ValueError:
            bintype_element_str = None
            item_element_str = None
            num_element_int = None

        print(f"垃圾类型: {bintype_element_str},垃圾：{item_element_str}")
    else:
        print("错误列表长度")

    return bintype_element_str, item_element_str, num_element_int


def solve_data_2(bin_type_str):
    wait_to_send_code = map_type_code(bin_type_str)
    print(f"要发送的分类代码：{wait_to_send_code}")
    return wait_to_send_code


def solve_data_3(string_list_length, string_list):
    if string_list_length == 1:
        # 在这里可以处理 string_list 中的数据
        complish_element = string_list[0]
        # 进行操作，比如将字符串转换为整数
        try:
            complish_element_str = map_if_complished(complish_element)
        except ValueError:
            complish_element_str = None

        print(f"分类是否完成: {complish_element_str}")
    else:
        print("错误列表长度")

    return complish_element_str


def solve_data_4(string_list_length, string_list):
    if string_list_length == 2:
        # 在这里可以处理 string_list 中的数据
        bintype_element = string_list[0]
        fulled_element = string_list[1]
        # 进行操作，比如将字符串转换为整数
        try:
            bintype_element_str = map_garbage_type(bintype_element)
            fulled_element_int = int(fulled_element)
        except ValueError:
            bintype_element_str = None
            fulled_element_int = None

        print(f"垃圾桶: {bintype_element_str}，满载百分比: {fulled_element_int}")
    else:
        print("错误列表长度")

    return bintype_element_str, fulled_element_int


if __name__ == "__main__":
    # 1
    test_strings1 = "A,07,1"
    # 3
    test_strings3 = "1"
    # 4
    test_strings4 = "B,40"
    str_list_len1, str_list1 = Split_strings(test_strings1)
    print(f"字符串列表长度：{str_list_len1}")
    print(f"字符串列表：{str_list1}")

    str_list_len3, str_list3 = Split_strings(test_strings3)
    print(f"字符串列表长度：{str_list_len3}")
    print(f"字符串列表：{str_list3}")

    str_list_len4, str_list4 = Split_strings(test_strings4)
    print(f"字符串列表长度：{str_list_len4}")
    print(f"字符串列表：{str_list4}")

    bintype_element_str, item_element_str, num_element_int=solve_data_1(str_list_len1, str_list1)
    to_send_code=solve_data_2(bintype_element_str)
    complish_element_str=solve_data_3(str_list_len3, str_list3)
    bintype_element_str, fulled_element_int=solve_data_4(str_list_len4, str_list4)
