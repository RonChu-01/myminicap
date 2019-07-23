# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/7/22.
# Copyright (c) 2019 3KWan.
# Description :

import sys
import time

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QEvent
from PyQt5.QtGui import QPainter, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from airtest.core.android.adb import ADB
from airtest.core.android.minicap import Minicap
from airtest.core.android.minitouch import Minitouch

from demo.airdemo.ui_demo import Ui_Form


class CapWorker(QThread):
    """  获取手机屏幕流  """

    frame_info = pyqtSignal(object)  # 刷新帧画面信号

    def __init__(self):
        super(CapWorker, self).__init__()

    def run(self):
        devices = [d[0] for d in ADB().devices()][0]
        adb = ADB(devices)
        mini_cap_ = Minicap(adb, (360, 640))  # 指定projection，未指定会按照默认的分辨率（图片大，延迟高）
        datas = mini_cap_.get_stream(lazy=True)  # 返回一个可迭代对象，mini_cup返回最新的一帧画面的流

        for data in datas:
            self.frame_info.emit(data)


class TouchWorker(QThread):
    """  Touch交互 """

    def __init__(self):
        super(TouchWorker, self).__init__()

    def run(self):
        devices = [d[0] for d in ADB().devices()][0]
        adb = ADB(devices)
        mini_touch = Minitouch(adb)
        pass


class Window(QWidget, Ui_Form):
    """  demo窗口  """

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.x = 0
        self.y = 0

        v_box = QVBoxLayout(self.widget_display)
        self.display = QLabel()
        self.display.resize(360, 640)
        v_box.addWidget(self.display)

        self.display.installEventFilter(self)  # 安装事件过滤器

        # 获取手机屏幕流线程
        self.frame_thread = CapWorker()
        self.frame_thread.frame_info.connect(self.refresh)
        self.frame_thread.start()

        # 创建mini_touch实例
        devices = [d[0] for d in ADB().devices()][0]
        adb = ADB(devices)
        self.mini_touch = Minitouch(adb)

    def refresh(self, frame):
        """
        刷新ui槽函数
        :param frame:
        :return:
        """
        data = QImage.fromData(frame)
        self.display.setPixmap(QPixmap(data))
        # self.display.setScaledContents(True)  # 不设置自适应貌似图片要清楚蛮多？

    def eventFilter(self, obj, event):
        """
        重写事件过滤
        :param obj:
        :param event:
        :return:
        """
        # 鼠标释放
        if event.type() == QEvent.MouseButtonRelease:
            print("MouseButtonRelease")
            x = event.pos().x() * 3  # 由于屏幕是按照1080 * 1920 等比例缩放，为对应Android手机屏幕坐标系，进行换算
            y = event.pos().y() * 3
            self.mini_touch.swipe((self.x, self.y), (x, y))  # 进行滑动操作
            return True
        # 鼠标点击
        elif event.type() == QEvent.MouseButtonPress:
            print("MouseButtonPress")
            x = event.pos().x() * 3
            y = event.pos().y() * 3
            self.x = x  # 记录当前点击的x坐标
            self.y = y  # 记录当前点击的y坐标
            self.mini_touch.touch((x, y))
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec_())


