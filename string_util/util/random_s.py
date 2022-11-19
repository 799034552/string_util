import torch
import numpy as np
import random
def set_random_seed(seed):
  """设置随机种子
  Args:
      seed (_type_): _description_
  """
  torch.manual_seed(seed)  # 为CPU设置随机种子
  np.random.seed(seed)  # Numpy module.
  random.seed(seed)  # Python random module.
  if torch.cuda.is_available():
      # torch.backends.cudnn.benchmark = False
      torch.backends.cudnn.deterministic = True
      torch.cuda.manual_seed(seed)  # 为当前GPU设置随机种子
      torch.cuda.manual_seed_all(seed)  # 为所有GPU设置随机种子