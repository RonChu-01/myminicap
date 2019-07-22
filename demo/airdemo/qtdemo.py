# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/7/22.
# Copyright (c) 2019 3KWan.
# Description :

import sys
import time

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from airtest.core.android.adb import ADB
from airtest.core.android.minicap import Minicap

from demo.airdemo.ui_demo import Ui_Form


class Worker(QThread):
    """  获取手机屏幕流  """

    frame_info = pyqtSignal(object)  # 刷新帧画面信号

    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        devices = [d[0] for d in ADB().devices()][0]
        adb = ADB(devices)
        mini_cap_ = Minicap(adb)
        datas = mini_cap_.get_stream(lazy=True)

        for data in datas:
            self.frame_info.emit(data)


class Window(QWidget, Ui_Form):
    """  demo窗口  """

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.frame = None

        v_box = QVBoxLayout(self.widget_display)
        self.display = QLabel()
        self.display.resize(350, 550)
        v_box.addWidget(self.display)

        self.frame_thread = Worker()
        self.frame_thread.frame_info.connect(self.refresh)
        self.frame_thread.start()

    def refresh(self, frame):
        """
        刷新ui槽函数
        :param frame:
        :return:
        """
        data = QImage.fromData(frame)
        self.display.setPixmap(QPixmap(data))
        self.display.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec_())


