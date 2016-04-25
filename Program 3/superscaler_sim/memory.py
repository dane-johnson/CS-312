class Memory:
  def __init__(self, instructions):
    self.instructions = instructions
  def __get__(self, i):
    return self.instructions[(i - 96) / 4]
  def __set__(self, i, val):
    self.instructions[(i - 96) / 4] = val