'''
Author: jason
Date: 2023-11-04 17:33:52
LastEditTime: 2023-11-24 17:18:38
LastEditors: jason
Description: 
'''
"""
Author: jason
Date: 2023-11-04 17:33:52
LastEditTime: 2023-11-04 18:11:42
LastEditors: jason
Description: 
"""
from serial_lib import *


class display_send_data:
    def __init__(self, send_port: str, send_header: str) -> None:
        self.handler = SerialDataHandler(port=send_port, baud_rate=9600, timeout=1)
        self.header = send_header
        self.data = "hello world!"
        self.length = len(self.data)
        self.length_str_length = len(str(self.length))
        self.data_format = f"c{self.length_str_length}s{self.length}sc"
        self.tail = (
            sum(
                bytes(self.header, encoding="utf-8")
                + bytes(str(self.length), encoding="utf-8")
                + bytes(self.data, encoding="utf-8")
            )
            % 0xFF
        ).to_bytes(1, "big")

    def set_data(self, in_data: str):
        self.data = in_data

    def set_data_format(self):
        self.length = len(self.data)
        self.length_str_length = len(str(self.length))
        self.data_format = f"c{self.length_str_length}s{self.length}sc"

    def send(self, data: str):
        if self.handler.open_serial_port():
            try:
                self.set_data(data)
                self.set_data_format()

                self.tail = (
                    sum(
                        bytes(self.header, encoding="utf-8")
                        + bytes(str(self.length), encoding="utf-8")
                        + bytes(self.data, encoding="utf-8")
                    )
                    % 0xFF
                ).to_bytes(1, "big")

                self.handler.send_data(
                    header=self.header,
                    length=str(self.length),
                    data=self.data,
                    format=self.data_format,
                )
            finally:
                # 关闭串口
                self.handler.close_serial_port()
        else:
            print("无法打开串口。")


# 测试代码
if __name__ == "__main__":
    # display_touch_lower_computer = display_send_data(send_port="COM12", send_header="2")
    # 发送使用方法：
    # 串口号（字符）
    # 帧头（字符）
    # display_touch_lower_computer.send("A")
    # 发送调用
    # 内容（字符串）

    # display_touch_lower_computer = display_send_data(send_port="COM3", send_header="1")
    # display_touch_lower_computer.send("D,7,1")

    display_touch_lower_computer = display_send_data(send_port="COM12", send_header="3")
    display_touch_lower_computer.send("1")

    # display_touch_lower_computer = display_send_data(send_port="COM12", send_header="4")
    # display_touch_lower_computer.send("A,75")
