"""
Author: jason
Date: 2023-10-18 22:10:40
LastEditTime: 2023-10-19 12:00:19
LastEditors: jason
Description: 通过求和方式生成的串口协议
"""
import struct
import serial


class SerialDataHandler:
    def __init__(self, port, baud_rate, timeout):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def open_serial_port(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            # print("串口成功打开")
            return True
        except serial.SerialException as e:
            print("无法打开串口:", e)
            return False

    def close_serial_port(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
                # print("串口成功关闭")
            except serial.SerialException as e:
                print("无法关闭串口:", e)

    def send_data(self, header: str, length: str, data: str, format: str):
        if not self.ser or not self.ser.is_open:
            print("串口未打开")
            return
        try:
            # str转bytes
            header = bytes(header, encoding="utf-8")
            length = bytes(length, encoding="utf-8")
            data = bytes(data, encoding="utf-8")
            # 使用正确的校验和方法计算尾部
            calculated_tail = (sum(header + length + data) % 0xFF).to_bytes(1, "big")
            to_send = struct.pack(format, header, length, data, calculated_tail)
            # print(header)
            # print(length)
            # print(len(data))
            # print(calculated_tail)
            # print(to_send)
            self.ser.write(to_send)
            data = data.decode("utf-8")
            # print(
            #     f"数据发送成功: {data}\n帧头: {header}, 长度为：{length}, 数据为：{data}, 帧尾是: {calculated_tail}"
            # )
            print(
                f"发送数据为：{data}"
            )
        except serial.SerialException as e:
            print("无法发送数据:", e)

    def receive_data(self, header: str, total_length: str, format: str):
        if not self.ser or not self.ser.is_open:
            return None
        try:
            received_data = self.ser.read(int(total_length))
            # 测试代码使用
            # simulated_data = b"E7\xb2\xbb\xbf\xc9\xbb\xd8\xca\xd5,75\x00\x00\x00B"
            # simulated_data =b'B61,\xc8\xab\xb2\xbf\xcd\xea\xb3\xc9\x00\x00\xf2'
            # 1
            # simulated_data=b'15D,7,1k'
            # 2
            # simulated_data=b'21A\xa4'
            # 3
            # simulated_data=b'311\x95'
            # 4
            # simulated_data=b'44B,75C'

            # received_data = simulated_data
            # print(len(received_data))
            # print(type(total_length), total_length)
            # print(type(int(total_length)), int(total_length))
            # print(received_data[0])
            # print(ord(header))

            if len(received_data) != int(total_length) or received_data[0] != ord(
                header
            ):
                return None
            unpacked_data = struct.unpack(format, received_data)
            (
                received_header,
                received_length,
                received_data,
                received_tail,
            ) = unpacked_data

            # print(received_data)

            sum_data = received_header + received_length + received_data
            # print(sum_data)
            # print(sum(sum_data))

            calculated_tail = (sum(sum_data) % 0xFF).to_bytes(1, "big")
            # print(calculated_tail)
            # print(received_tail)

            if received_tail == calculated_tail:
                return received_data.decode("utf-8")
            else:
                return None
        except serial.SerialException as e:
            print("无法接收数据:", e)
            return None


# 测试代码
if __name__ == "__main__":
    # 使用适当的设置创建 SerialDataHandler 类的实例
    data_handler = SerialDataHandler("COM12", 9600, 1)

    # 打开串口
    if data_handler.open_serial_port():
        try:
            # 根据您的协议定义格式（应与您在 send_data 中使用的格式匹配）
            header = "A"
            data = "你好!"
            length = len(data)
            length_str_length = len(str(length))
            data_format = f"c{length_str_length}s{length*2}sc"

            tail = (
                sum(
                    bytes(header, encoding="utf-8")
                    + bytes(str(length), encoding="utf-8")
                    + bytes(data, encoding="utf-8")
                )
                % 0xFF
            ).to_bytes(1, "big")

            print(bytes(str(length), encoding="utf-8"))

            # 模拟接收到的数据（您可以用来自串口的实际数据替换这部分）
            simulated_data = struct.pack(
                data_format,
                bytes(header, encoding="utf-8"),
                bytes(str(length), encoding="utf-8"),
                bytes(data, encoding="utf-8"),
                tail,
            )

            # 打印接收到的数据（仅用于测试目的）
            print(f"模拟接收到的数据: {simulated_data}")

            # 调用 receive_data 方法以解包模拟数据
            result = data_handler.receive_data(
                "A", str(length * 2 + length_str_length + 2), data_format
            )

            # 检查结果是否有效并打印它
            if result is not None:
                received_data = result
                print(f"接收到的数据: {received_data}")
            else:
                print("接收到的数据无效。")

        finally:
            # 关闭串口
            data_handler.close_serial_port()
    else:
        print("无法打开串口。")
