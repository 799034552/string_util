import os

def get_dirs(path, is_base_name=False):
    """获取指定目录下的文件并排序

    Args:
        path (_type_): _description_
    """
    dirs = os.listdir(path)
    dirs = sorted(dirs)
    dirs = [os.path.join(path,item) for item in dirs]
    dirs = [item for item in dirs if os.path.isdir(item)]
    if is_base_name:
        dirs = [os.path.basename(item) for item in dirs]
    return dirs
    

