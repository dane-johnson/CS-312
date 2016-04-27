from superscaler_sim.word import Word
from superscaler_sim.output import findDataAddress
class Memory:
  def __init__(self, instructions):
    dataAddr = findDataAddress(instructions)
    self.instructions = instructions
    for i, instruction in enumerate(instructions):
      if i < dataAddr:
        continue
      else:
        self.instructions[i] = Word.convert32BitUnsignedToSigned(instruction)
  def __getitem__(self, i):
    return self.instructions[(i - 96) / 4]
  def __setitem__(self, i, val):
    self.instructions[(i - 96) / 4] = val