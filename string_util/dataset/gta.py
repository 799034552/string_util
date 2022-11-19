import scipy.io as io
from PIL import Image
from glob import glob
import os
from einops import rearrange
import numpy as np
import torch

class GTA_dataset():
    def __init__(self,
                path,
                split="train",
                img_size = (1914, 1052),
                mean=[0.5, 0.5, 0.5], 
                std=[1, 1, 1],
                ignore_index=250):

        if not (split == "train" or split == "test" or split == "val"):
            assert("split only train/test/val")
        splits = io.loadmat(os.path.join(path, 'split.mat'))
        ids = None
        if (split == "train"):
            ids = splits["trainIds"][:,0]
        elif (split == "test"):
            ids = splits["testIds"][:,0]
        elif (split == "val"):
            ids = splits["valIds"][:,0]
        ids = [str(i).zfill(5)+".png" for i in ids]
        self.img_paths = [os.path.join(path, "images", item) for item in ids]
        self.lbl_paths = [os.path.join(path, "labels", item) for item in ids]
        self.img_size = img_size
        self.mean = mean
        self.std = std
        self.ignore_index = ignore_index
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
        self.n_classes = 19
        self.valid_classes = [7, 8, 11, 12, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33,]
        self.class_names = ["road","sidewalk","building","wall","fence","pole","traffic_light",
            "traffic_sign","vegetation","terrain","sky","person","rider","car","truck","bus","train",
            "motorcycle","bicycle",]
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


        
