class Memeory:
  def __init__(self, instructions):
    self.instructions = instructions
  def __get__(self, i):
    return self.instructions[(i - 96) / 4]