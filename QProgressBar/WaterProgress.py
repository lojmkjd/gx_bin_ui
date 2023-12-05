'''
Author: jason
Date: 2023-09-19 16:46:00
LastEditTime: 2023-10-03 21:58:37
LastEditors: jason
Description: 
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

try:
    from PyQt5.QtCore import QTimer
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
    from PyQt5.QtGui import QColor
except ImportError:
    from PySide2.QtCore import QTimer
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
    from PyQt5.QtGui import QColor

from Lib.DWaterProgress import DWaterProgress


class WaterProgressWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(WaterProgressWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        self.progress = DWaterProgress(self)
        self.progress.setFixedSize(100, 100)
        self.progress.setValue(0)
        self.progress.start()

        layout.addWidget(self.progress)

        self.timer = QTimer(self, timeout=self.updateProgress)
        self.timer.start(50)

    def updateProgress(self):
        value = self.progress.value()
        if value == 100:
            self.progress.setValue(0)
        else:
            self.progress.setValue(value + 1)


if __name__ == '__main__':
    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = WaterProgressWindow()
    w.show()
    sys.exit(app.exec_())
