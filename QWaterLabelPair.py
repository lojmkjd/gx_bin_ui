'''
Author: jason
Date: 2023-09-22 16:56:36
LastEditTime: 2023-11-02 15:26:23
LastEditors: jason
Description: 
'''
import sys
sys.path.append("QProgressBar")


from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout,QLabel
from PyQt5.QtGui import QFont
from QProgressBar.Lib.DWaterProgress import DWaterProgress
try:
    from PyQt5.QtCore import (
        QTimer,
    )
except ImportError:
    from PySide2.QtCore import (
        QTimer,
    )

WATER_FRONT = """<svg xmlns="http://www.w3.org/2000/svg" width="383" height="115" viewBox="0 0 383 115">
  <path fill="#01C4FF" fill-rule="evenodd" d="M383,115 L383,14.1688789 C380.269872,14.0716143 377.092672,13.5814974 373.063461,12.4722672 C368.696509,11.2699114 362.241136,10.1727531 357.649256,10.1227411 C347.007291,10.0071963 342.744795,10.6014761 332.930121,12.0276784 C326.157898,13.0120512 317.51313,12.4953762 311.375303,10.33762 C305.58601,8.30230681 299.587109,8.09191178 293.164466,8.16675723 C284.09108,8.27264456 276.303198,11.8021073 267.219716,11.3406179 C260.695053,11.0091595 256.565913,8.56512814 248.546835,8.86450991 C241.871757,9.11387975 235.569934,13.1896798 228.881972,13.3297132 C219.538394,13.525622 215.498041,10.7384053 208.282229,8.42337018 C201.688974,6.30769299 190.725982,6.45048568 185.454442,8.65549452 C170.142255,15.0597811 162.05946,9.31703167 150.536236,5.36712375 C147.826999,4.43862637 144.672431,3.20971247 141.663406,2.90998579 C135.153716,2.26155522 129.812539,3.9788615 123.613779,5.46231888 C115.747555,7.3451819 106.643181,6.73503633 99.4869089,3.84572629 C96.4124243,2.60474055 93.6255416,0.951587506 90.1882469,0.261077932 C79.652131,-1.85528907 69.7970674,9.59778831 58.8051757,9.35186757 C49.4744806,9.14319709 42.6942497,2.4740197 33.3934986,1.93078665 C20.5224457,1.17888312 19.3845731,15.343297 0,13.8463882 L0,115 L383,115 Z"/>
</svg>
"""
WATER_BACK = """<svg xmlns="http://www.w3.org/2000/svg" width="383" height="115" viewBox="0 0 383 115">
  <path fill="#007DFF" fill-rule="evenodd" d="M383,115 L383,14.1688789 C380.269872,14.0716143 377.092672,13.5814974 373.063461,12.4722672 C368.696509,11.2699114 362.241136,10.1727531 357.649256,10.1227411 C347.007291,10.0071963 342.744795,10.6014761 332.930121,12.0276784 C326.157898,13.0120512 317.51313,12.4953762 311.375303,10.33762 C305.58601,8.30230681 299.587109,8.09191178 293.164466,8.16675723 C284.09108,8.27264456 276.303198,11.8021073 267.219716,11.3406179 C260.695053,11.0091595 256.565913,8.56512814 248.546835,8.86450991 C241.871757,9.11387975 235.569934,13.1896798 228.881972,13.3297132 C219.538394,13.525622 215.498041,10.7384053 208.282229,8.42337018 C201.688974,6.30769299 190.725982,6.45048568 185.454442,8.65549452 C170.142255,15.0597811 162.05946,9.31703167 150.536236,5.36712375 C147.826999,4.43862637 144.672431,3.20971247 141.663406,2.90998579 C135.153716,2.26155522 129.812539,3.9788615 123.613779,5.46231888 C115.747555,7.3451819 106.643181,6.73503633 99.4869089,3.84572629 C96.4124243,2.60474055 93.6255416,0.951587506 90.1882469,0.261077932 C79.652131,-1.85528907 69.7970674,9.59778831 58.8051757,9.35186757 C49.4744806,9.14319709 42.6942497,2.4740197 33.3934986,1.93078665 C20.5224457,1.17888312 19.3845731,15.343297 0,13.8463882 L0,115 L383,115 Z"/>
</svg>
"""
class WaterLabelPair(QWidget):
    def __init__(self,bin_type=None,bin_type_label_color=None):
        super(WaterLabelPair, self).__init__()
        self.goal_value=0

        # 定义布局
        layout=QVBoxLayout(self)

        # 设置文字内容
        self.bin_type=bin_type

        # 创建文字控件
        self.bin_type_label = QLabel()
        self.bin_type_label.setText(bin_type)
        font = QFont("Arial", 20)
        self.bin_type_label.setFont(font)
        self.bin_type_label.setStyleSheet(f"color: {bin_type_label_color}")
        self.bin_type_label.setAlignment(Qt.AlignCenter)

        # 创建进度瓶控件
        self.progress = DWaterProgress(self)
        self.progress.setFixedSize(70, 70)
        self.progress.setValue(0)
        self.progress.start()

        # 创建状态显示控件
        self.bin_full_label = QLabel()
        self.bin_full_label.setText("未满载")
        font = QFont("Arial", 20)
        self.bin_full_label.setFont(font)
        self.bin_full_label.setStyleSheet("color: green")
        self.bin_full_label.setAlignment(Qt.AlignCenter)

        # 添加垃圾桶类型进入布局
        layout.addWidget(self.bin_type_label)

        # 创建横向布局
        H_layout=QHBoxLayout()
        H_layout.addWidget(self.progress)
        H_layout.addWidget(self.bin_full_label)

        # 添加横向布局进入主布局
        layout.addLayout(H_layout)

        # 设定刷新事件和刷新时间
        self.timer = QTimer(self, timeout=self.updateProgress)
        self.timer.start(50)

    def updateProgress(self):
        value = self.progress.value()
        goal_value = self.goal_value
        
        if value == 100:
            self.progress.setValue(0)
        
        if value < goal_value:
            self.progress.setValue(value + 1)
        elif value > goal_value:
            self.progress.setValue(value - 4)
        
        if value > 75:
            self.bin_full_label.setStyleSheet("color: red")
            self.bin_full_label.setText("满载!")
        else:
            self.bin_full_label.setStyleSheet("color: green")
            self.bin_full_label.setText("未满载")



    def updateGoalValue(self,goal_value):
        self.goal_value=goal_value

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = WaterLabelPair(bin_type="可回收垃圾",bin_type_label_color="green")
    w.show()
    print(type(w))
    QTimer.singleShot(2000,lambda:(w.updateGoalValue(80)))
    sys.exit(app.exec_())
