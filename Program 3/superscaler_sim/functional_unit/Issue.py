from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED

from superscaler_sim.word import Instruction

from collections import deque

class PreIssue(UnitBuffer):
  def __init__(self):
    self.buffer = deque()
  def __len__(self):
    return len(self.buffer)
 
class Issue(FunctionalUnit):
  @staticmethod
  def buildInstruction(word):
    #define some helper functions
    def shift(curr, instuction):
      curr['operands'] = (instruction['rt'], instruction['sa'])
      curr['dest'] = instruction['rd']
      return curr
    def math(curr, instruction):
      curr['operands'] = (instruction['rt'], instruction['rs'])
      curr['dest'] = instruction['rd']
      return curr
    instuction = Instruction(word)
    curr = {}
    curr['instruction'] = word
    op = instruction['op']
    if op == 0b100000 :# R Type, many cases
      func = instruction['func']
      if   func == 0b000000: # SLL
        curr['op'] = 'sll'
        return shift(curr, instruction)
      elif func == 0b000010:  # SRL
        curr['op'] == 'srl'
        return shift(curr, instruction)
      elif func == 0b100000: # ADD
        curr['op'] = 'add'
        return math(curr, instruction)
      elif func == 0b100010: # SUB
        curr['op'] = 'sub'
        return math(curr, instruction)
      elif func == 0b100100: # AND
        curr['op'] = 'and'
        return math(curr, instruction)
      elif func == 0b100101: # OR
        curr['op'] = 'or'
        return math(curr, instruction)
      else: # MOVZ
        curr['op'] = 'movz'
        return math(curr, instruction)
    elif op == 0b111100: #MUL
      curr['op'] = 'mul'
    elif op == 0b101000:	#ADDI
      curr['op'] = 'addi'
      curr['dest'] = instruction['rd']
      curr['operands'] = (instruction['rs'], instruction['immed')
      return curr
    elif op == 0b100011:	#LW
      curr['op'] = 'lw'
      curr['dest'] = instruction['rt']
      curr['addr'] = instruction['rs'] + instruction['immed']
      return curr
    else:	#SW
      curr['op'] = 'sw'
      curr['data'] = registers[instruction['rt']]
      curr['addr'] = instruction['rs'] + instruction['immed']
      return curr

  def __init__(self, hazard, registers, preIssue = None, preMem = None, preAlu = None):
    FunctionalUnit.__init__(self)
    self.preIssue = preIssue
    self.preMem = preMem
    self.preAlu = preAlu
    self.hazard = hazard
    self.registers = registers
  
  def execute(self):
    #set issued instructions = 0
    nIssued = 0
    #go into a for loop that simply iterates twice
    for i in range(2):
      #go into a for loop over the stack
      for instruction in reversed(self.preIssue.buffer):
        #if issued instructions == 2 > break outer loop
        if nIssued == 2: break
        #peek at the next instruction, determine op code, registers, construct the instruction
        curr = Issue.buildInstruction(instruction)
        #Check for structural hazards, WAW hazards, WAR hazards, RAW hazards, previous sw issued 
        if curr['op'] == 'lw' or curr['op'] == 'sw' and len(self.preMem) >= 4:
          #preMem full
          self.hazard.noIssued.append(curr)
          continue
        elif len(self.preAlu) >= 4:
          #preAlu full
          self.hazard.noIssued.append(curr)
          continue
        if self.hazard.checkAll(curr):
          hazard.noIssued.append(curr)
          continue
        else
          #No problems, issue the instruction
          if curr['op'] == 'lw' or curr['op'] == 'sw':
            self.preMem.queue.appendleft(curr)
          else:
            self.preAlu.queue.appendleft(curr)
          hazard.active.append(curr)
          nIssued += 1
      else:
        #exited normally, continue before we hit the break
        continue
      break