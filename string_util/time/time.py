import time

class _TIME():
  def __init__(self) -> None:
    self.timer_counter = {}
  def re_time(self, index, name=None, groud="default_time"):
    if (groud not in self.timer_counter):
      self.timer_counter[groud] = []
    assert(index <= len(self.timer_counter[groud]))
    if (index == len(self.timer_counter[groud])):
      self.timer_counter[groud].append([0,None,name])
    self.timer_counter[groud][index][1] = time.time()
    if (index != 0):
      self.timer_counter[groud][index][0] += self.timer_counter[groud][index][1] - self.timer_counter[groud][index - 1][1]
  def show_time(self):
    for groud in self.timer_counter:
      print(groud, ":{")
      for i in range(1, len(self.timer_counter[groud])):
        if (self.timer_counter[groud][i][2] is not None):
          print(f"  {self.timer_counter[groud][i][2]}: ",end="")
        else:
          print(f"  {i}: ",end="")
        print("%.3f s" % self.timer_counter[groud][i][0])
      print("}")



TIME = _TIME()