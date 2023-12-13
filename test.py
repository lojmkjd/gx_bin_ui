<<<<<<< HEAD
"""
Author: jason
Date: 2023-11-02 15:14:11
LastEditTime: 2023-11-07 08:29:30
LastEditors: jason
Description: 
"""
"""
Author: jason
Date: 2023-11-02 15:14:11
LastEditTime: 2023-11-07 08:27:02
LastEditors: jason
Description: 
"""
import sys
import threading
import time
import random
from QMainwindows import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, QCoreApplication
from solve_data import *
from Display_receive_data import *
from Display_send_data import *


# 设置轮数=per_and_round.txt的数量-1
# 实际轮数=per_and_round.txt的数量-1
# 设置轮数=实际轮数
number_set_all_round = 10


def generate_random_msg1():
    types = ["A", "B", "C", "D", "E"]

    # Randomly choose a type
    trash_type = random.choice(types)

    # If the type is "E", set quantity to -1, otherwise, generate a random quantity
    quantity = -1 if trash_type == "E" else random.randint(10, 20)

    # Append the generated string to msg1_box
    msg1 = f"{trash_type},{quantity},1"

    # For type "E", append an additional entry with quantity 0
    if trash_type == "E":
        msg1 = f"{trash_type},-1,0"

    return msg1


count = 0


def generate_random_msg3():
    global count
    types = ["1", "0"]
    msg3 = random.choice(types)
    # if msg3=="1":
    #     count+=1
    #     if count>1:
    #         msg3="0"
    #         count=0
    #     else:
    #         pass
    # else:
    #     pass
    return msg3


def generate_random_msg4():
    trash_type = random.choice(["A", "B", "C", "D"])
    position = random.randint(10, 99)
    msg4 = f"{trash_type},{position}"
    return msg4


test_strings1 = "E,-1,0"
test_strings3 = "0"
test_strings4 = "B,40"


# 1 显示器从上位机接收信息并储存
first_item_containers = "无垃圾"
second_item_containers = "无垃圾"
bintype_save_map = [[]]
item_save_map = [[]]
num_save_map = [[]]


def receiv_new_litter():
    while 1:
        # 测试用，使用时删除
        test_strings1 = generate_random_msg1()

        if test_strings1 is None:
            test_strings1 = "E,-1,0"

        global first_item_containers, second_item_containers, number_of_completed_round
        global bintype_save_map, item_save_map, num_save_map

        str_list_len1, str_list1 = Split_strings(test_strings1)
        bintype_element_str, item_element_str, num_element_int = solve_data_1(
            str_list_len1, str_list1
        )

        # display_touch_lower_computer.send(test_strings1[0])

        second_item_containers = item_element_str
        if "无垃圾" == first_item_containers:
            if "无垃圾" != second_item_containers:
                bintype_save_map[number_of_completed_round].append(bintype_element_str)
                item_save_map[number_of_completed_round].append(second_item_containers)
                num_save_map[number_of_completed_round].append(num_element_int)
                first_item_containers = second_item_containers
                print(f"物品列表：{item_save_map},长度为：{len(item_save_map)}")
            else:
                first_item_containers = second_item_containers
        else:
            first_item_containers = second_item_containers
        time.sleep(1)


per_and_round = dict_former(path="per_and_round.txt")

# 3 从下位机接收消息，是否完成
# 创建两个相邻的是否完成容器
first_if_complished_container = "分类未完成"
second_if_complished_container = "分类未完成"
number_of_completed_classifications = 0
number_set_per_round = int(per_and_round.get(str(0)))
number_of_completed_round = 0


def add_msg():
    while 1:
        start = time.time()
        # receiv_new_litter()
        global first_if_complished_container, second_if_complished_container, number_of_completed_classifications, number_set_per_round, number_of_completed_round, number_set_all_round
        global bintype_save_map, item_save_map, num_save_map
        global per_and_round
        # 接收是否完成
        test_strings3 = generate_random_msg3()

        if test_strings3 is None:
            test_strings3 = "0"

        str_list_len3, str_list3 = Split_strings(test_strings3)
        complish_element_str = solve_data_3(str_list_len3, str_list3)
        second_if_complished_container = complish_element_str

        if number_of_completed_round <= number_set_all_round:
            if "分类未完成" == first_if_complished_container:
                if "分类已完成" == second_if_complished_container:
                    number_of_completed_classifications += 1
                    try:
                        if number_of_completed_classifications >= number_set_per_round:
                            number_of_completed_round += 1
                            number_set_per_round = int(
                                per_and_round.get(str(number_of_completed_round))
                            )
                            number_of_completed_classifications = 0

                            bintype_save_map = [
                                item for item in bintype_save_map if item
                            ]
                            item_save_map = [item for item in item_save_map if item]
                            num_save_map = [item for item in num_save_map if item]

                            bintype_save_map.append([])
                            item_save_map.append([])
                            num_save_map.append([])

                            bintype_element_str = ""
                            item_element_str = ""
                            num_element_int = ""
                            for a in range(
                                int(
                                    per_and_round.get(
                                        str(number_of_completed_round - 1)
                                    )
                                )
                            ):
                                bintype_element_str = (
                                    bintype_element_str
                                    + bintype_save_map[number_of_completed_round - 1][
                                        number_of_completed_classifications + a
                                    ]
                                ) + ","

                                item_element_str = (
                                    item_element_str
                                    + item_save_map[number_of_completed_round - 1][
                                        number_of_completed_classifications + a
                                    ]
                                ) + ","
                                num_element_int = (
                                    num_element_int
                                    + num_save_map[number_of_completed_round - 1][
                                        number_of_completed_classifications + a
                                    ]
                                ) + ","

                            a_new_message = f"序号：{number_of_completed_round} 分类：{bintype_element_str} 物品：{item_element_str} 数量：{num_element_int} 分类状态:OK!"
                            w.msg_to_show = a_new_message
                            w.update_msg()
                            first_if_complished_container = (
                                second_if_complished_container
                            )
                        else:
                            # 测试用，使用时删
                            # first_if_complished_container = "分类未完成"
                            first_if_complished_container = (
                                second_if_complished_container
                            )
                    except:
                        number_of_completed_round -= 1

                else:
                    first_if_complished_container = second_if_complished_container
                    # 测试用，使用时删
                    # first_if_complished_container = "分类未完成"

            else:
                first_if_complished_container = second_if_complished_container
                # 测试用，使用时删
                # first_if_complished_container = "分类未完成"
        else:
            pass

        print(f"垃圾分类历史：{item_save_map}")
        print(f"垃圾分类时间：{round(time.time()-start,2)}s\n")
        time.sleep(1)


# 4
def update_fulled_value():
    while True:
        start = time.time()

        test_strings4 = generate_random_msg4()

        if test_strings4 is not None:
            str_list_len4, str_list4 = Split_strings(test_strings4)
            bintype_element_str, fulled_element_int = solve_data_4(
                str_list_len4, str_list4
            )
            if fulled_element_int in range(10, 99):
                if bintype_element_str == w.recyclable_bin_label.bin_type:
                    w.recyclable_bin_label.updateGoalValue(fulled_element_int)
                elif bintype_element_str == w.not_recyclable_bin_label.bin_type:
                    w.not_recyclable_bin_label.updateGoalValue(fulled_element_int)
                elif bintype_element_str == w.harmful_bin_label.bin_type:
                    w.harmful_bin_label.updateGoalValue(fulled_element_int)
                elif bintype_element_str == w.food_waste_bin_label.bin_type:
                    w.food_waste_bin_label.updateGoalValue(fulled_element_int)
                else:
                    pass
            else:
                pass
        else:
            pass
        print(f"满载检测时间：{round(time.time()-start,2)}s\n")
        time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()

    timer_update_full = threading.Thread(
        target=update_fulled_value, name="满载检测", daemon=True
    )
    timer_update_full.start()

    timer_add_msg = threading.Thread(target=add_msg, name="信息更新", daemon=True)
    timer_add_msg.start()

    timer_receiv_new_litter = threading.Thread(
        target=receiv_new_litter, name="接收新信息", daemon=True
    )
    timer_receiv_new_litter.start()

    sys.exit(app.exec_())
=======
"""
Author: jason
Date: 2023-11-02 15:14:11
LastEditTime: 2023-11-07 08:29:30
LastEditors: jason
Description: 
"""
"""
Author: jason
Date: 2023-11-02 15:14:11
LastEditTime: 2023-11-07 08:27:02
LastEditors: jason
Description: 
"""
import sys
import threading
import time
import random
from QMainwindows import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, QCoreApplication
from solve_data import *
from Display_receive_data import *
from Display_send_data import *


# 设置轮数=per_and_round.txt的数量-1
# 实际轮数=per_and_round.txt的数量-1
# 设置轮数=实际轮数
number_set_all_round = 10


def generate_random_msg1():
    types = ["A", "B", "C", "D", "E"]

    # Randomly choose a type
    trash_type = random.choice(types)

    # If the type is "E", set quantity to -1, otherwise, generate a random quantity
    quantity = -1 if trash_type == "E" else random.randint(10, 20)

    # Append the generated string to msg1_box
    msg1 = f"{trash_type},{quantity},1"

    # For type "E", append an additional entry with quantity 0
    if trash_type == "E":
        msg1 = f"{trash_type},-1,0"

    return msg1


count = 0


def generate_random_msg3():
    global count
    types = ["1", "0"]
    msg3 = random.choice(types)
    # if msg3=="1":
    #     count+=1
    #     if count>1:
    #         msg3="0"
    #         count=0
    #     else:
    #         pass
    # else:
    #     pass
    return msg3


def generate_random_msg4():
    trash_type = random.choice(["A", "B", "C", "D"])
    position = random.randint(10, 99)
    msg4 = f"{trash_type},{position}"
    return msg4


test_strings1 = "E,-1,0"
test_strings3 = "0"
test_strings4 = "B,40"


# 1 显示器从上位机接收信息并储存
first_item_containers = "无垃圾"
second_item_containers = "无垃圾"
bintype_save_map = [[]]
item_save_map = [[]]
num_save_map = [[]]


def receiv_new_litter():
    while 1:
        # 测试用，使用时删除
        test_strings1 = generate_random_msg1()

        if test_strings1 is None:
            test_strings1 = "E,-1,0"

        global first_item_containers, second_item_containers, number_of_completed_round
        global bintype_save_map, item_save_map, num_save_map

        str_list_len1, str_list1 = Split_strings(test_strings1)
        bintype_element_str, item_element_str, num_element_int = solve_data_1(
            str_list_len1, str_list1
        )

        # display_touch_lower_computer.send(test_strings1[0])

        second_item_containers = item_element_str
        if "无垃圾" == first_item_containers:
            if "无垃圾" != second_item_containers:
                bintype_save_map[number_of_completed_round].append(bintype_element_str)
                item_save_map[number_of_completed_round].append(second_item_containers)
                num_save_map[number_of_completed_round].append(num_element_int)
                first_item_containers = second_item_containers
                print(f"物品列表：{item_save_map},长度为：{len(item_save_map)}")
            else:
                first_item_containers = second_item_containers
        else:
            first_item_containers = second_item_containers
        time.sleep(1)


per_and_round = dict_former(path="per_and_round.txt")

# 3 从下位机接收消息，是否完成
# 创建两个相邻的是否完成容器
first_if_complished_container = "分类未完成"
second_if_complished_container = "分类未完成"
number_of_completed_classifications = 0
number_set_per_round = int(per_and_round.get(str(0)))
number_of_completed_round = 0


def add_msg():
    while 1:
        start = time.time()
        # receiv_new_litter()
        global first_if_complished_container, second_if_complished_container, number_of_completed_classifications, number_set_per_round, number_of_completed_round, number_set_all_round
        global bintype_save_map, item_save_map, num_save_map
        global per_and_round
        # 接收是否完成
        test_strings3 = generate_random_msg3()

        if test_strings3 is None:
            test_strings3 = "0"

        str_list_len3, str_list3 = Split_strings(test_strings3)
        complish_element_str = solve_data_3(str_list_len3, str_list3)
        second_if_complished_container = complish_element_str

        if number_of_completed_round <= number_set_all_round:
            if "分类未完成" == first_if_complished_container:
                if "分类已完成" == second_if_complished_container:
                    number_of_completed_classifications += 1
                    try:
                        if number_of_completed_classifications >= number_set_per_round:
                            number_of_completed_round += 1
                            number_set_per_round = int(
                                per_and_round.get(str(number_of_completed_round))
                            )
                            number_of_completed_classifications = 0

                            bintype_save_map = [
                                item for item in bintype_save_map if item
                            ]
                            item_save_map = [item for item in item_save_map if item]
                            num_save_map = [item for item in num_save_map if item]

                            bintype_save_map.append([])
                            item_save_map.append([])
                            num_save_map.append([])

                            bintype_element_str = ""
                            item_element_str = ""
                            num_element_int = ""
                            for a in range(
                                int(
                                    per_and_round.get(
                                        str(number_of_completed_round - 1)
                                    )
                                )
                            ):
                                bintype_element_str = (
                                    bintype_element_str
                                    + bintype_save_map[number_of_completed_round - 1][
                                        number_of_completed_classifications + a
                                    ]
                                ) + ","

                                item_element_str = (
                                    item_element_str
                                    + item_save_map[number_of_completed_round - 1][
                                        number_of_completed_classifications + a
                                    ]
                                ) + ","
                                num_element_int = (
                                    num_element_int
                                    + num_save_map[number_of_completed_round - 1][
                                        number_of_completed_classifications + a
                                    ]
                                ) + ","

                            a_new_message = f"序号：{number_of_completed_round} 分类：{bintype_element_str} 物品：{item_element_str} 数量：{num_element_int} 分类状态:OK!"
                            w.msg_to_show = a_new_message
                            w.update_msg()
                            first_if_complished_container = (
                                second_if_complished_container
                            )
                        else:
                            # 测试用，使用时删
                            # first_if_complished_container = "分类未完成"
                            first_if_complished_container = (
                                second_if_complished_container
                            )
                    except:
                        number_of_completed_round -= 1

                else:
                    first_if_complished_container = second_if_complished_container
                    # 测试用，使用时删
                    # first_if_complished_container = "分类未完成"

            else:
                first_if_complished_container = second_if_complished_container
                # 测试用，使用时删
                # first_if_complished_container = "分类未完成"
        else:
            pass

        print(f"垃圾分类历史：{item_save_map}")
        print(f"垃圾分类时间：{round(time.time()-start,2)}s\n")
        time.sleep(1)


# 4
def update_fulled_value():
    while True:
        start = time.time()

        test_strings4 = generate_random_msg4()

        if test_strings4 is not None:
            str_list_len4, str_list4 = Split_strings(test_strings4)
            bintype_element_str, fulled_element_int = solve_data_4(
                str_list_len4, str_list4
            )
            if fulled_element_int in range(10, 99):
                if bintype_element_str == w.recyclable_bin_label.bin_type:
                    w.recyclable_bin_label.updateGoalValue(fulled_element_int)
                elif bintype_element_str == w.not_recyclable_bin_label.bin_type:
                    w.not_recyclable_bin_label.updateGoalValue(fulled_element_int)
                elif bintype_element_str == w.harmful_bin_label.bin_type:
                    w.harmful_bin_label.updateGoalValue(fulled_element_int)
                elif bintype_element_str == w.food_waste_bin_label.bin_type:
                    w.food_waste_bin_label.updateGoalValue(fulled_element_int)
                else:
                    pass
            else:
                pass
        else:
            pass
        print(f"满载检测时间：{round(time.time()-start,2)}s\n")
        time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()

    timer_update_full = threading.Thread(
        target=update_fulled_value, name="满载检测", daemon=True
    )
    timer_update_full.start()

    timer_add_msg = threading.Thread(target=add_msg, name="信息更新", daemon=True)
    timer_add_msg.start()

    timer_receiv_new_litter = threading.Thread(
        target=receiv_new_litter, name="接收新信息", daemon=True
    )
    timer_receiv_new_litter.start()

    sys.exit(app.exec_())
>>>>>>> 0b937a5bc434ac36c6acade789aec87fe957a9f0
