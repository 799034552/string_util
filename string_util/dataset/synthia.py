import scipy.io as io
from PIL import Image
from glob import glob
import os
from einops import rearrange
import numpy as np
import imageio
import torch

class Synthia_dataset():
    def __init__(self,
                path,
                split="train",
                img_size = (1280, 760),
                mean=[0.5, 0.5, 0.5], 
                std=[1, 1, 1],
                ignore_index=250):

        if not (split == "train" or split == "test" or split == "val"):
            assert("split only train/test/val")
        ids = glob(os.path.join(path, f"RGB/*"))
        ids = [os.path.basename(item) for item in ids]
        ids = sorted(ids)
        self.img_paths = [os.path.join(path, "RGB", item) for item in ids]
        self.lbl_paths = [os.path.join(path, "GT/LABELS", item) for item in ids]
        self.img_size = img_size
        self.mean = mean
        self.std = std
        self.ignore_index = ignore_index
        self._init()
    def __len__(self):
        return len(self.lbl_paths)
    
    def __getitem__(self, index):
        img = Image.open(self.img_paths[index])

        lbl = np.asarray(imageio.imread(self.lbl_paths[index], format='PNG-FI'))[:,:,0]
        lbl = Image.fromarray(lbl)

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
        return img, lbl, self.img_paths[index]
    def _init(self):
        self.n_classes = 16
        self.valid_classes = [3,4,2,21,5,7,15,9,6,1,10,17,8,19,12,11,]
        self.class_names = ["Road","Sidewalk","Building","Wall",
            "Fence","Pole","Traffic_light","Traffic_sign","Vegetation",
            "sky","Pedestrian","Rider","Car","Bus",
            "Motorcycle","Bicycle",
        ]
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


        
