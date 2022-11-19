from string_util.dataset.synthia import Synthia_dataset
from tqdm import tqdm
import torch
synthia_data_load = Synthia_dataset("./datasets/RAND_CITYSCAPES", split="train", mean=[0,0,0])
for i in tqdm(range(2290, synthia_data_load.__len__())):
    img ,lbl,path = synthia_data_load.__getitem__(i)
    if ("0002294.png" in path):
        print(img.shape)
        print(lbl.shape)
        print(torch.sum(img))
        print(torch.sum(lbl))
        exit()

