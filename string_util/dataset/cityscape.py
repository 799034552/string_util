from PIL import Image
from glob import glob
import os
from .util import get_dirs
from einops import rearrange
import numpy as np
import torch
class Cityscape_dataset():
    def __init__(self,
                path,
                split="train",
                img_size=(2048,1024),
                mean=[0.485, 0.456, 0.406], 
                std=[0.229, 0.224, 0.225],
                n_class = 19,
                ignore_index=250):
        if not (split == "train" or split == "test" or split == "val"):
            assert("split only train/test/val")
        citys = get_dirs(os.path.join(path, f"leftImg8bit/{split}"), True)
        img_paths = []
        lbl_paths = []
        for city in citys:
            imgs_one_city = glob(os.path.join(path, f"leftImg8bit/{split}/{city}/*"))
            imgs_one_city = sorted(imgs_one_city)
            img_paths += imgs_one_city
            for img in imgs_one_city:
                suffix = "_".join(os.path.basename(img).split("_")[:-1]) + "_gtFine_labelIds.png"
                lbl_paths.append(os.path.join(path, f"gtFine/{split}/{city}/{suffix}"))
        self.img_paths = img_paths
        self.lbl_paths = lbl_paths
        self.img_size = img_size
        self.mean = mean
        self.std = std
        self.ignore_index = ignore_index
        self.n_class = n_class
        self._init()

    def __len__(self):
        return len(self.lbl_paths)

    def __getitem__(self, index):
        img = Image.open(self.img_paths[index])
        lbl = Image.open(self.lbl_paths[index])
        img = img.resize(self.img_size, Image.BILINEAR)
        lbl = lbl.resize(self.img_size, Image.NEAREST)
        img = np.array(img, dtype=np.uint8)
        lbl = np.array(lbl, dtype=np.uint8)
        lbl = self.encode_segmap(lbl) # 将官方label的index变为我们关心的
        # 归一化
        img = img / 255.0
        img = img - self.mean
        img = img / self.std
        img = rearrange(img, "h w c -> c h w")
        # 转为tensor
        img = torch.from_numpy(img).float()
        lbl = torch.from_numpy(lbl).long()
        return img, lbl
    
    def _init(self):
        """定义不变常量
        """
        # self.n_classes = 19
        if self.n_classes == 19:
            self.valid_classes = [7, 8, 11, 12, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33,]
            self.class_names = ["road","sidewalk","building","wall",
                "fence","pole","traffic_light","traffic_sign","vegetation",
                "terrain","sky","person","rider","car",
                "truck","bus","train","motorcycle","bicycle",
            ]
            # self.to19 = dict(zip(range(19), range(19)))
        elif self.n_classes == 16:
            self.valid_classes = [7, 8, 11, 12, 13, 17, 19, 20, 21, 23, 24, 25, 26, 28, 32, 33,]
            self.class_names = ["road","sidewalk","building","wall",
                "fence","pole","traffic_light","traffic_sign","vegetation",
                "sky","person","rider","car","bus",
                "motorcycle","bicycle",
            ]
            # self.to19 = dict(zip(range(16), [0,1,2,3,4,5,6,7,8,10,11,12,13,15,17,18]))
        elif self.n_classes == 13:
            self.valid_classes = [7, 8, 11, 19, 20, 21, 23, 24, 25, 26, 28, 32, 33,]
            self.class_names = ["road","sidewalk","building","traffic_light",
                "traffic_sign","vegetation","sky","person","rider",
                "car","bus","motorcycle","bicycle",
            ]
        # self.to19 = dict(zip(range(13), [0,1,2,6,7,8,10,11,12,13,15,17,18]))
        # self.ignore_index = 255
        self.class_map = dict(zip(self.valid_classes, range(self.n_classes)))
    
    def encode_segmap(self, mask):
        """将label官方index转为想要的

        Args:
            mask (_type_): _description_

        Returns:
            _type_: _description_
        """
        label_copy = self.ignore_index * np.ones_like(mask, dtype=np.uint8)
        for k, v in list(self.class_map.items()):
            label_copy[mask == k] = v
        return label_copy
        
