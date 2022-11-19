# 一个自己的库

# dataHandle
## 保存数据
```py
from string_util.dataHandle import save_data

save_data(路径，文件名前缀，保存的数据)
会自动检索路径中有该文件前缀的数据，并且每次调用创建一个后缀文件，比如说
citysacpe_0.pt
citysacpe_1.pt
```
## 读取数据
```py
from string_util.dataHandle import dataset

dataset(路径，文件名前缀)
读取上面保存文件时保存的文件，符合pytorch dataset的定义 
```
# get_config
读取yml文件
```py
from string_util import CONFIG
cfg = CONFIG("./haha.yml")
print(cfg.epoch_time)
```
显示内容
```py
cfg.print()
cfg.haha.print()
```
结合argparse使用
```py
from string_util import CONFIG
import argparse
cfg = CONFIG("./haha.yml")
parser = argparse.ArgumentParser(description='choose work')
parser.add_argument('-m', type=str,
                    default="train")
cfg.update(parser.parse_args().__dict__)
cfg.print()
```
# time
获取程序运行时间
```py
from string_util import TIME
import time

TIME.re_time(0, "训练开始", groud="train")
time.sleep(1)
TIME.re_time(1, "训练结束", groud="train")
TIME.show_time()
```
