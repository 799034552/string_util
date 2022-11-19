import yaml

class _Dict():
    def __init__(self, arg) -> None:
        for k, v in arg.items():
            if isinstance(v, dict):
                self.__dict__[k] = _Dict(v)
                # self.update(_dict[k], v)
            else:
                self.__dict__[k] = v
                
    def update(self, arg):
        _dict = self.__dict__
        for k, v in arg.items():
            if isinstance(v, dict):
                if(k in _dict and isinstance(_dict[k], _Dict)):
                  _dict[k].update(v)
                else:
                  _dict[k] = _Dict(v)
                # self.update(_dict[k], v)
            else:
                _dict[k] = v


    def print(self, deep=0):
      for k, v in self.__dict__.items():
        print("".join([" " for _ in range(deep)]),end="")
        if (not isinstance(v, _Dict)):
          print(f"{k}: {v}")
        else:
          print(f"{k}:")
          v.print(deep+1)

class _Config():
    def __init__(self, yaml_path):
        self.update(self._parse_yaml(yaml_path))

    def update(self,arg, _dict=None):
        """将arg字典添加到_dict中,_dict默认为本地__dict__

        Args:
            arg (_type_): _description_
            _dict (_type_, optional): _description_. Defaults to None.
        """
        if _dict is None:
            _dict = self.__dict__
        for k, v in arg.items():
            if isinstance(v, dict):
                if(k in _dict and isinstance(_dict[k], _Dict)):
                  _dict[k].update(v)
                else:
                  _dict[k] = _Dict(v)
                # self.update(_dict[k], v)
            else:
                _dict[k] = v

    
    def _parse_yaml(self, path, encoding='utf8'):
        """解析yaml文件

        Args:
            path (_type_): 路径
        """
        # 打开文件
        with open(path,encoding=encoding) as a_yaml_file:
            # 解析yaml
            parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
            return parsed_yaml_file
    def print(self, deep=0):
        for k, v in self.__dict__.items():
            print("".join([" " for _ in range(deep)]),end="")
            if (not isinstance(v, _Dict)):
                print(f"{k}: {v}")
            else:
                print(f"{k}:")
                v.print(deep+1)






