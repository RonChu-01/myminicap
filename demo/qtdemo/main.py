# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/7/19.
# Copyright (c) 2019 3KWan.
# Description :

import socket
import threading
from queue import Queue
from qtdemo.banner import Banner


class MinicapStream:
    __instance = None
    __mutex = threading.Lock()

    def __init__(self):
        self.IP = "127.0.0.1"  # 定义IP
        self.PORT = 1313  # 监听的端口
        self.Pid = 0  # 进程ID
        self.banner = Banner()  # 用于存放banner头信息
        # self.minicapSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.minicapSocket = None
        self.ReadImageStreamTask = None
        self.push = None
        self.picture = Queue()

    @staticmethod
    def getBuilder():
        """Return a single instance of TestBuilder object """
        if (MinicapStream.__instance == None):
            MinicapStream.__mutex.acquire()
            if (MinicapStream.__instance == None):
                MinicapStream.__instance = MinicapStream()
            MinicapStream.__mutex.release()
        return MinicapStream.__instance

    def get_d(self):
        print(self.picture.qsize())

    def run(self):
        # 开始执行
        # 启动socket连接
        self.minicapSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        self.minicapSocket.connect((self.IP, self.PORT))
        # return self.ReadImageStream()
        self.ReadImageStreamTask = threading.Thread(target=self.ReadImageStream).start()

    def ReadImageStream(self):
        # 读取图片流到队列

        print("读取图片流到队列")

        readBannerBytes = 0
        bannerLength = 2
        readFrameBytes = 0
        frameBodylength = 0
        dataBody = bytes()

        while True:
            reallen = self.minicapSocket.recv(4096)
            length = len(reallen)
            if not length:
                continue
            cursor = 0
            while cursor < length:
                # just do it
                if readBannerBytes < bannerLength:
                    if readBannerBytes == 0:
                        self.banner.Version = reallen[cursor]
                        # self.banner.Version = bytes_to_int(reallen[cursor])
                    elif readBannerBytes == 1:
                        bannerLength = reallen[cursor]
                        self.banner.Length = bannerLength
                    elif readBannerBytes in [2, 3, 4, 5]:
                        self.banner.Pid += (reallen[cursor] << ((readBannerBytes - 2) * 8)) >> 0
                    elif readBannerBytes in [6, 7, 8, 9]:
                        self.banner.RealWidth += (reallen[cursor] << ((readBannerBytes - 6) * 8)) >> 0
                    elif readBannerBytes in [10, 11, 12, 13]:
                        self.banner.RealHeight += (reallen[cursor] << ((readBannerBytes - 10) * 8)) >> 0
                    elif readBannerBytes in [14, 15, 16, 17]:
                        self.banner.VirtualWidth += (reallen[cursor] << (
                                    (readBannerBytes - 14) * 8)) >> 0
                    elif readBannerBytes in [18, 19, 20, 21]:
                        self.banner.VirtualHeight += (reallen[cursor] << (
                                    (readBannerBytes - 18) * 8)) >> 0
                    elif readBannerBytes == 22:
                        self.banner.Orientation = reallen[cursor] * 90
                    elif readBannerBytes == 23:
                        self.banner.Quirks = reallen[cursor]
                    cursor += 1
                    readBannerBytes += 1
                    if readBannerBytes == bannerLength:
                        print(self.banner.toString())

                elif readFrameBytes < 4:
                    frameBodylength = frameBodylength + ((reallen[cursor] << (readFrameBytes * 8)) >> 0)
                    cursor += 1
                    readFrameBytes += 1
                else:
                    if length - cursor >= frameBodylength:
                        print("--length:{0}-------cursor:{1}---------frameBodylength:{2}------".format(length, cursor, frameBodylength))

                        dataBody = dataBody + reallen[cursor:(cursor + frameBodylength)]
                        print("dataBody[0]", dataBody[0])
                        print(dataBody[1])
                        if dataBody[0] != 0xFF or dataBody[1] != 0xD8:
                            return
                        print(dataBody)
                        self.picture.put(dataBody)
                        # self.save_file('d:/pic.png', dataBody)
                        cursor += frameBodylength
                        frameBodylength = 0
                        readFrameBytes = 0
                        dataBody = bytes()
                    else:
                        dataBody = dataBody + reallen[cursor:length]
                        frameBodylength -= length - cursor
                        readFrameBytes += length - cursor
                        cursor = length


# adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1200x1920@1200x1920/0
# adb forward tcp:1313 localabstract:minicap

    def save_file(self, file_name, data):
        file = open(file_name, "wb")
        file.write(data)
        file.flush()
        file.close()


if __name__ == '__main__':
    a = MinicapStream.getBuilder()
    a.run()
    print("a.picture---------------->", a.picture)


# import socket
# import threading
# from queue import Queue
#
# from itsdangerous.encoding import bytes_to_int, int_to_bytes
#
# from banner import Banner
#
#
# class MinicapStream:
#     __instance = None
#     __mutex = threading.Lock()
#
#     def __init__(self):
#         self.IP = "127.0.0.1"  # 定义IP
#         self.PORT = 1313  # 监听的端口
#         self.Pid = 0  # 进程ID
#         self.banner = Banner()  # 用于存放banner头信息
#         # self.minicapSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         self.minicapSocket = None
#         self.ReadImageStreamTask = None
#         self.push = None
#         self.picture = Queue()
#
#     @staticmethod
#     def getBuilder():
#         """Return a single instance of TestBuilder object """
#         if (MinicapStream.__instance == None):
#             MinicapStream.__mutex.acquire()
#             if (MinicapStream.__instance == None):
#                 MinicapStream.__instance = MinicapStream()
#             MinicapStream.__mutex.release()
#         return MinicapStream.__instance
#
#     def get_d(self):
#         print(self.picture.qsize())
#
#     def run(self):
#         # 开始执行
#         # 启动socket连接
#         self.minicapSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
#         self.minicapSocket.connect((self.IP, self.PORT))
#         # return self.ReadImageStream()
#         self.ReadImageStreamTask = threading.Thread(target=self.ReadImageStream).start()
#
#     def ReadImageStream(self):
#         # 读取图片流到队列
#
#         print("读取图片流到队列")
#
#         readBannerBytes = 0
#         bannerLength = 2
#         readFrameBytes = 0
#         frameBodylength = 0
#         dataBody = ""
#
#         while True:
#             print("start")
#             reallen = self.minicapSocket.recv(4096)
#             print("reallen---->", reallen)
#             length = len(reallen)
#             print("length---->", length)
#             if not length:
#                 continue
#             cursor = 0
#             while cursor < length:
#                 # just do it
#                 if readBannerBytes < bannerLength:
#                     print(readBannerBytes)
#                     if readBannerBytes == 0:
#                         print(reallen[cursor])
#                         self.banner.Version = int_to_bytes(reallen[cursor])
#                         # self.banner.Version = bytes_to_int(reallen[cursor])
#
#                     elif readBannerBytes == 1:
#                         bannerLength = bytes_to_int(reallen[cursor])
#                         print("bannerLength---->", bannerLength)
#                         self.banner.Length = bannerLength
#                     elif readBannerBytes in [2, 3, 4, 5]:
#                         self.banner.Pid += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 2) * 8)) >> 0
#                     elif readBannerBytes in [6, 7, 8, 9]:
#                         self.banner.RealWidth += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 6) * 8)) >> 0
#                     elif readBannerBytes in [10, 11, 12, 13]:
#                         self.banner.RealHeight += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 10) * 8)) >> 0
#                     elif readBannerBytes in [14, 15, 16, 17]:
#                         self.banner.VirtualWidth += (bytes_to_int(reallen[cursor]) << (
#                                     (readBannerBytes - 14) * 8)) >> 0
#                     elif readBannerBytes in [18, 19, 20, 21]:
#                         self.banner.VirtualHeight += (bytes_to_int(reallen[cursor]) << (
#                                     (readBannerBytes - 18) * 8)) >> 0
#                     elif readBannerBytes == 22:
#                         self.banner.Orientation = bytes_to_int(reallen[cursor]) * 90
#                     elif readBannerBytes == 23:
#                         self.banner.Quirks = bytes_to_int(reallen[cursor])
#                     cursor += 1
#                     readBannerBytes += 1
#                     if readBannerBytes == bannerLength:
#                         print(self.banner.toString())
#
#                 elif readFrameBytes < 4:
#                     frameBodylength = frameBodylength + ((bytes_to_int(reallen[cursor]) << (readFrameBytes * 8)) >> 0)
#                     cursor += 1
#                     readFrameBytes += 1
#                 else:
#                     if length - cursor >= frameBodylength:
#                         dataBody = dataBody + reallen[cursor:(cursor + frameBodylength)]
#                         if bytes_to_int(dataBody[0]) != 0xFF or bytes_to_int(dataBody[1]) != 0xD8:
#                             return
#                         self.picture.put(dataBody)
#                         # self.save_file('d:/pic.png', dataBody)
#                         cursor += frameBodylength
#                         frameBodylength = 0
#                         readFrameBytes = 0
#                         dataBody = ""
#                     else:
#                         dataBody = dataBody + reallen[cursor:length]
#                         frameBodylength -= length - cursor
#                         readFrameBytes += length - cursor
#                         cursor = length
#
# # adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1200x1920@1200x1920/0
# # adb forward tcp:1313 localabstract:minicap
#
#     def save_file(self, file_name, data):
#         file = open(file_name, "wb")
#         file.write(data)
#         file.flush()
#         file.close()
#
#
# if __name__ == '__main__':
#     a = MinicapStream.getBuilder()
#     print(id(a))
#     a.run()


