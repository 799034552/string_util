import torch
import numpy as np
import os
import glob
import shutil



def get_last_num(path, name):
    pass

def save_data(path, name, data):

    """保存数据为一个个单独的文件

    Args:
        path (_type_): 保存路径
        name (_type_): 保存文件名
        data (dict): 保存的数据, 字典格式
    """
    if (not os.path.isdir(path)):
        os.makedirs(path)
    file_names = glob.glob(os.path.join(path, f"{name}*.pt"))
    last_num = 0
    if (len(file_names)):
        for file_name in file_names:
            last_num = max(last_num, int(file_name.split('_')[-1].split('.')[0]))
        last_num += 1
    torch.save(data, os.path.join(path, f"{name}_{last_num}.pt"))

# 与save_data匹配的dataset
class dataset():
    def __init__(self, path, name, map_location = "cpu") -> None:
        """与save_data匹配的dataset

        Args:
            path (_type_): 路径
            name (_type_): 名称
            map_location: 直接加载的位置，"cuda:0"
        """
        self.map_location = map_location
        self.file_names = glob.glob(os.path.join(path, f"{name}*.pt"))
        self.file_names = sorted(self.file_names,key=lambda file_name:int(file_name.split('_')[-1].split('.')[0]))
    def __len__(self):
        return len(self.file_names)
        pass
    def __getitem__(self, index):
        return torch.load(self.file_names[index], map_location=self.map_location)
        pass




