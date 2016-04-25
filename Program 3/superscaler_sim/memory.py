class Memory:
  def __init__(self, instructions):
    self.instructions = instructions
  def __getitem__(self, i):
    return self.instructions[(i - 96) / 4]
  def __setitem__(self, i, val):
    self.instructions[(i - 96) / 4] = val