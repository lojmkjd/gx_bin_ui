"""
Author: jason
Date: 2023-11-02 15:14:11
LastEditTime: 2023-11-03 08:35:29
LastEditors: jason
Description: 
"""
import sys
import time
from QVideo import Video
from QWaterLabelPair import WaterLabelPair
from PyQt5.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QSplitter,
    QScrollArea,
    QApplication,
    QGridLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt,QTimer,pyqtSignal
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):

    update_msg_signal = pyqtSignal()

    def __init__(self, max_messages=5, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.max_messages = max_messages
        self.message_labels = []
        self.msg_to_show=""
        
        self.init_ui()

    def init_ui(self):
        # 初始化标题信息和位置
        self.setWindowTitle("信息窗")
        self.resize(1024, 600)
        self.move(-10, -20)

        # 创建垂直分割器并将垂直分割器设置为中心控件
        self.V_splitter = QSplitter(Qt.Vertical)
        self.setCentralWidget(self.V_splitter)

        # 创建水平分割器并将水平分割器加入到垂直分割器中
        self.H_splitter = QSplitter(Qt.Horizontal)
        self.V_splitter.addWidget(self.H_splitter)

        # 创建视频控件并将视频控件加入到水平分割器中
        self.video_widget = Video()
        self.H_splitter.addWidget(self.video_widget)

        # 创建垃圾桶满载提示控件
        self.recyclable_bin_label = WaterLabelPair(
            bin_type="可回收垃圾", bin_type_label_color="green"
        )
        self.not_recyclable_bin_label = WaterLabelPair(
            bin_type="其它垃圾", bin_type_label_color="blue"
        )
        self.harmful_bin_label = WaterLabelPair(
            bin_type="有害垃圾", bin_type_label_color="red"
        )
        self.food_waste_bin_label = WaterLabelPair(
            bin_type="厨余垃圾", bin_type_label_color="greg"
        )

        # 创建标题控件
        self.bin_full_title_label = QLabel()
        self.bin_full_title_label.setText("满载信息")
        font = QFont("Arial", 12)
        self.bin_full_title_label.setFont(font)
        self.bin_full_title_label.setStyleSheet("color: black")
        self.bin_full_title_label.setAlignment(Qt.AlignCenter)

        # 创建垂直布局并将垃圾桶满载提示控件加入进去
        self.bin_full_label_widget = QWidget()
        self.bin_full_label_widget_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.bin_full_label_widget.setLayout(self.bin_full_label_widget_layout)
        self.bin_full_label_widget_layout.addWidget(self.bin_full_title_label)
        self.bin_full_label_widget_layout.addLayout(self.grid_layout)
        self.grid_layout.addWidget(self.recyclable_bin_label, 0, 0)
        self.grid_layout.addWidget(self.not_recyclable_bin_label, 0, 1)
        self.grid_layout.addWidget(self.harmful_bin_label, 1, 0)
        self.grid_layout.addWidget(self.food_waste_bin_label, 1, 1)

        # 将上面创建的垂直布局加入到水平分割器中
        self.H_splitter.addWidget(self.bin_full_label_widget)

        # 创建滚动字幕标题并加入到垂直分割器中
        self.scroll_title=self.create_label("分类信息栏")
        self.scroll_title.setAlignment(Qt.AlignCenter)
        self.V_splitter.addWidget(self.scroll_title)

        # 设置滚动字幕控件为垂直分布
        self.scrollarea = QScrollArea()
        self.scroll_content = QWidget()
        self.scrollarea.setWidget(self.scroll_content)
        self.msg_layout = QVBoxLayout(self.scroll_content)
        self.V_splitter.addWidget(self.scroll_content)
        
        # 创建空白信息
        for _ in range(self.max_messages):
            blank_label=self.create_label(text="")
            self.message_labels.append(blank_label)
            self.msg_layout.addWidget(blank_label)

        # 设置垂直分割器的比例
        self.V_splitter.setStretchFactor(0, 1)
        self.V_splitter.setStretchFactor(2, 4)
        self.update_msg_signal.connect(self.add_new_msg)

    def create_label(self, text=None):
        label = QLabel()
        label.setText(text)
        font = QFont("Arial", 12)
        label.setFont(font)
        label.setStyleSheet(f"color: black")

        return label

    def add_new_msg(self):
        if len(self.message_labels) >= self.max_messages:
            # 移除最旧的信息
            self.message_labels[0].setVisible(False)
            self.message_labels.pop(0)

        msg_label = self.create_label(text=self.msg_to_show)
        self.message_labels.append(msg_label)
        self.scroll_content.layout().addWidget(msg_label)

    def update_msg(self):
        self.update_msg_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    print(type(w))
    sys.exit(app.exec_())
