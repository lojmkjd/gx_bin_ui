"""
Author: jason
Date: 2023-11-04 19:57:08
LastEditTime: 2023-11-04 19:59:11
LastEditors: jason
Description: 
"""
import struct


if __name__ == "__main__":
    # 根据您的协议定义格式（应与您在 send_data 中使用的格式匹配）
    header = "E"
    data = "不可回收,75"
    # print(bytes(data, encoding="utf-8"))
    length = len(data)
    length_str_length = len(str(length))
    data_format = f"c{length_str_length}s{length*2}sc"

    sum_tail = (
        bytes(header, encoding="utf-8")
        + bytes(str(length), encoding="utf-8")
        + bytes(data, encoding="utf-8")
    )

    # print(sum(sum_tail))

    tail = (
        sum(
            bytes(header, encoding="utf-8")
            + bytes(str(length), encoding="utf-8")
            + bytes(data, encoding="utf-8")
        )
        % 0xFF
    ).to_bytes(1, "big")

    # print(bytes(str(length), encoding="utf-8"))

    # 模拟接收到的数据（您可以用来自串口的实际数据替换这部分）
    simulated_data = struct.pack(
        data_format,
        bytes(header, encoding="utf-8"),
        bytes(str(length), encoding="utf-8"),
        bytes(data, encoding="utf-8"),
        tail,
    )

    print(simulated_data)
