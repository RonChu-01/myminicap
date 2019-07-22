# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/7/20.
# Copyright (c) 2019 3KWan.
# Description :

import os
import time

from threading import Thread

from airtest.core.android.adb import ADB
from airtest.core.android.minicap import Minicap
from airtest.core.android.minitouch import Minitouch


def save_file(file_name, data):
    file = open(file_name, "wb")
    file.write(data)
    file.flush()
    file.close()

# start_time = time.perf_counter()
# devices = [d[0] for d in ADB().devices()][0]
# adb = ADB(devices)
# mini_cap_ = Minicap(adb)

# print(mini_cap_.get_display_info())
# pic_data = mini_cap_.get_frame()
# save_path = os.path.join(os.getcwd(), "pic.jpg")
# save_file(save_path, pic_data)
# end_time = time.perf_counter()
# used_time = end_time - start_time
# print(used_time)


def worker():
    datas = mini_cap_.get_stream(lazy=True)
    # start_time = time.perf_counter()
    # for data in datas:
    #     start_time = time.perf_counter()
    #     save_file(save_path, data)
    #     print(data)
    #     # break
    #     end_time = time.perf_counter()
    #     used_time = end_time - start_time
    #     print(used_time)


devices = [d[0] for d in ADB().devices()][0]
adb = ADB(devices)
mini_cap_ = Minicap(adb)

save_path = os.path.join(os.getcwd(), "pic.jpg")
t = Thread(target=worker)
t.start()
# datas = mini_cap_.get_stream(lazy=True)

# start_time = time.perf_counter()

# for data in datas:
#     # save_file(save_path, data)
#     print(data)
#     break

# end_time = time.perf_counter()
# used_time = end_time - start_time
# print(used_time)
