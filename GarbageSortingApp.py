"""
Author: jason
Date: 2023-12-13 13:00:59
LastEditTime: 2023-12-13 13:45:06
LastEditors: jason
Description: 
"""
import sys
import threading
import time
import random
from QMainwindows import MainWindow
from PyQt5.QtWidgets import QApplication
from solve_data import *
from Display_receive_data import *
from Display_send_data import *


class GarbageSortingApp:
    def __init__(self, number_set_all_round, dict_path):
        self.first_item_containers = "无垃圾"
        self.second_item_containers = "无垃圾"
        self.first_if_complished_container = "分类未完成"
        self.second_if_complished_container = "分类未完成"
        self.bintype_save_map = [[]]
        self.item_save_map = [[]]
        self.num_save_map = [[]]
        self.number_of_completed_round = 0
        self.number_of_completed_classifications = 0
        self.number_set_all_round = number_set_all_round
        self.per_and_round = dict_former(path=dict_path)
        self.number_set_per_round = int(self.per_and_round.get(str(0)))

    def generate_random_msg1(self):
        types = ["A", "B", "C", "D", "E"]

        trash_type = random.choice(types)

        quantity = -1 if trash_type == "E" else random.randint(10, 20)

        msg1 = f"{trash_type},{quantity},1"

        if trash_type == "E":
            msg1 = f"{trash_type},-1,0"

        return msg1

    def generate_random_msg3(self):
        types = ["1", "0"]
        msg3 = random.choice(types)

        return msg3

    def generate_random_msg4(self):
        trash_type = random.choice(["A", "B", "C", "D"])
        position = random.randint(10, 99)
        msg4 = f"{trash_type},{position}"
        return msg4

    def receive_new_litter(self):
        test_strings1 = self.generate_random_msg1() or "E,-1,0"
        str_list_len1, str_list1 = Split_strings(test_strings1)
        bintype_element_str, item_element_str, num_element_int = solve_data_1(str_list_len1, str_list1)

        if "无垃圾" != item_element_str or "无垃圾" != self.first_item_containers:
            self.second_item_containers = item_element_str

            self.bintype_save_map[self.number_of_completed_round].append(bintype_element_str)
            self.item_save_map[self.number_of_completed_round].append(self.second_item_containers)
            self.num_save_map[self.number_of_completed_round].append(num_element_int)
            self.first_item_containers = self.second_item_containers
            print(f"物品列表：{self.item_save_map},长度为：{len(self.item_save_map)}")

    def process_completion(self):
        self.number_of_completed_classifications += 1
        try:
            if self.number_of_completed_classifications >= self.number_set_per_round:
                self.number_of_completed_round += 1
                self.number_set_per_round = int(self.per_and_round.get(str(self.number_of_completed_round)))
                self.number_of_completed_classifications = 0

                self.item_save_map = [item for item in self.item_save_map if item]

                self.bintype_save_map.append([])
                self.item_save_map.append([])
                self.num_save_map.append([])

                bintype_element_str = ""
                item_element_str = ""
                num_element_int = ""
                for a in range(int(self.per_and_round.get(str(self.number_of_completed_round - 1)))):
                    bintype_element_str += self.bintype_save_map[self.number_of_completed_round - 1][self.number_of_completed_classifications + a] + ","
                    item_element_str += self.item_save_map[self.number_of_completed_round - 1][self.number_of_completed_classifications + a] + ","
                    num_element_int += self.num_save_map[self.number_of_completed_round - 1][self.number_of_completed_classifications + a] + ","

                a_new_message = f"序号：{self.number_of_completed_round} 分类：{bintype_element_str} 物品：{item_element_str} 数量：{num_element_int} 分类状态：OK！"
                self.w.msg_to_show = a_new_message
                self.w.update_msg()
                self.first_if_complished_container = self.second_if_complished_container
            else:
                self.first_if_complished_container = self.second_if_complished_container
        except:
            self.number_of_completed_round -= 1


    def add_msg(self):
        while True:
            start = time.time()
            self.receive_new_litter()
            test_strings3 = self.generate_random_msg3() or "0"
            str_list_len3, str_list3 = Split_strings(test_strings3)
            self.second_if_complished_container = solve_data_3(str_list_len3, str_list3)

            if self.number_of_completed_round <= self.number_set_all_round:
                if "分类未完成" == self.first_if_complished_container:
                    if "分类已完成" == self.second_if_complished_container:
                        self.process_completion()
                    else:
                        self.first_if_complished_container = self.second_if_complished_container
                else:
                    self.first_if_complished_container = self.second_if_complished_container
            else:
                pass

            print(f"垃圾分类历史：{self.item_save_map}")
            print(f"垃圾分类时间：{round(time.time() - start, 2)}s\n")
            time.sleep(1)

    def update_fulled_value(self):
        while True:
            start = time.time()

            test_strings4 = self.generate_random_msg4()

            if test_strings4:
                str_list_len4, str_list4 = Split_strings(test_strings4)
                bintype_element_str, fulled_element_int = solve_data_4(str_list_len4, str_list4)

                if 10 <= fulled_element_int < 99:
                    bin_labels = [
                        self.w.recyclable_bin_label,
                        self.w.not_recyclable_bin_label,
                        self.w.harmful_bin_label,
                        self.w.food_waste_bin_label,
                    ]

                    for label in bin_labels:
                        if bintype_element_str == label.bin_type:
                            label.updateGoalValue(fulled_element_int)
                            break
                    else:
                        pass  # 如果没有找到匹配的标签
                else:
                    pass  # fulled_element_int 不在范围内
            else:
                pass  # test_strings4 为 None

            print(f"满载检测时间：{round(time.time() - start, 2)}s\n")
            time.sleep(1)


    def run_app(self):
        app = QApplication(sys.argv)
        self.w = MainWindow()
        self.w.show()

        timer_update_full = threading.Thread(
            target=self.update_fulled_value, name="满载检测", daemon=True
        )
        timer_update_full.start()

        timer_add_msg = threading.Thread(target=self.add_msg, name="信息更新", daemon=True)
        timer_add_msg.start()

        sys.exit(app.exec_())


if __name__ == "__main__":
    garbage_app = GarbageSortingApp(4, "per_and_round.txt")
    garbage_app.run_app()
