'''
Author: jason
Date: 2023-11-04 18:14:20
LastEditTime: 2023-11-24 18:07:43
LastEditors: jason
Description: 
'''
"""
Author: jason
Date: 2023-11-04 18:14:20
LastEditTime: 2023-11-04 18:14:23
LastEditors: jason
Description: 
"""
from serial_lib import *


class display_receive_data:
    def __init__(self, receive_port, receive_header, receive_data_eg) -> None:
        self.handler = SerialDataHandler(port=receive_port, baud_rate=9600, timeout=1)
        self.header = receive_header
        self.data_eg = receive_data_eg
        self.length = len(self.data_eg)
        self.length_str_length = len(str(self.length))
        self.unpack_data_format = f"c{self.length_str_length}s{self.length}sc"
        self.result = None

    def receive(self):
        if self.handler.open_serial_port():
            try:
                self.result = self.handler.receive_data(
                    self.header,
                    str(self.length + self.length_str_length + 2),
                    self.unpack_data_format,
                )

            finally:
                # 关闭串口
                self.handler.close_serial_port()

        else:
            print("无法打开串口。")


# 测试代码
if __name__ == "__main__":
    # 1
    # display_receive_from_upper_computer = display_receive_data(
    #     receive_port="COM3", receive_header="1", receive_data_eg="A,10,1"
    # )
    # 接收串口使用方法：
    # 串口号（字符）
    # 帧头（字符）
    # 示例（字符）
    # display_receive_from_upper_computer.receive()
    # 调用接收：
    # r = display_receive_from_upper_computer.result
    # 调用方法 .result

    # print(
    #     type(r),
    #     r,
    # )

    # 2
    # display_receive_from_upper_computer = display_receive_data(
    #     receive_port="COM12", receive_header="2", receive_data_eg="A"
    # )
    # display_receive_from_upper_computer.receive()
    # r = display_receive_from_upper_computer.result
    # print(
    #     type(r),
    #     r,
    # )

    # 3
    # display_receive_from_upper_computer = display_receive_data(
    #     receive_port="COM12", receive_header="3", receive_data_eg="1"
    # )
    # display_receive_from_upper_computer.receive()
    # r = display_receive_from_upper_computer.result
    # print(
    #     type(r),
    #     r,
    # )

    # 4
    display_receive_from_upper_computer = display_receive_data(
        receive_port="COM13", receive_header="4", receive_data_eg="A,00"
    )
    while 1:
        display_receive_from_upper_computer.receive()
        r = display_receive_from_upper_computer.result
        if r is not None:
            print(
                "收取成功",
                type(r),
                r,
            )
        else:
            print("收取失败")