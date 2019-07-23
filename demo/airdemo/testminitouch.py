# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/7/22.
# Copyright (c) 2019 3KWan.
# Description :

import time

from airtest.core.android.adb import ADB
from airtest.core.android.minitouch import Minitouch

devices = [d[0] for d in ADB().devices()][0]
adb = ADB(devices)
mini_touch = Minitouch(adb)

# mini_touch.setup_server()
# mini_touch.setup_client()
mini_touch.touch((900, 1800))
mini_touch.swipe((1200, 200), (-200, 200), duration=0.8, steps=6)
time.sleep(1)
mini_touch.swipe((-200, 200), (1200, 200), duration=0.8, steps=6)




