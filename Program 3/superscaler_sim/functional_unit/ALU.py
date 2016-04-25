from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED

from collections import deque

class PreALU(UnitBuffer): #standard FIFO queue
  def __init__(self):
    self.queue = deque()
  def __len__(self):
    return len(self.queue)
    
class PostALU(UnitBuffer): #one entry
  def __init__(self):
    self.entry = None
  def __len__(self):
    if self.entry == None: return 0
    return 1
    
class ALU(FunctionalUnit):
  def __init__(self, hazard, preAlu = None, postAlu = None):
    FunctionalUnit.__init__(self)
    self.preAlu = preAlu
    self.postAlu = postAlu
    self.hazard = hazard
  
  def execute(self):
    if len(self.preAlu) == 0:
      self.state = STALLED
    else:
      self.state = READY
    if self.state == STALLED:
      return
    
    curr = last.queue.pop() #should be a dictionary, popping clears the entry
    out = {} #blank dictionary
    op = curr['op']
    operands = curr['operands']
    
    #just pass the instruction on at least
   
    out['dest'] = curr['dest']
    
    out['instruction'] = curr['instruction']

    if op == 'add' or op == 'addi':
      out['data'] = operands[0] + operands[1] #add the operands
    elif op == 'sub':
      out['data'] = operands[0] - operands[1] #subtract the operands
    elif op == 'and':
      out['data'] = operands[0] & operands[1] #and the operands
    elif op == 'or':
      out['data'] = operands[0] | operands[1] #or the operands
    elif op == 'movz':
      if operand[0] == 0: #check and be sure equal to zero
        out['data'] = operands[1] #move the data
      else: self.hazard.complete(curr['instruction']) #do not move the data
    elif op == 'sll':
      out['data'] = operands[0] << operands[1] #should be the shift amount
    elif op == 'srl':
      out['data'] = operands[0] >> operands[1] #should be the shift amount
    elif op == 'mul':
      out['data'] = operands[0] * operands[1] #multiply the operands
    
    postAlu.entry = out #send the computed data to the post-alu buffer