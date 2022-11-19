from string_util import TIME
import time

TIME.re_time(0, "训练开始", groud="train")
time.sleep(1)
TIME.re_time(1, "训练结束", groud="train")
TIME.show_time()
