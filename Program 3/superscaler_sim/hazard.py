from superscaler_sim.word import Instruction

from pdb import set_trace as bp

class HazardUnit:
  def __init__(self, preIssue):
    self.active = []
    self.noIssued = []
    self.preIssue = preIssue
  def __len__(self):
    return len(self.active) + len(self.noIssued)
  def purgeNoIssued(self):
    self.noIssued = []
  def complete(self, instruction):
    try:
      for i in self.active:
        if i['instruction'] == instruction:
          self.active.remove(i)
          break
    except ValueError:
      pass #shouldnt happen, but also not a problem if it does
  def checkWAW(self, curr):
    if not 'dest' in curr.keys():
      #not writing, all good 
      return False
    all = self.active + self.noIssued
    for i in all:
      try:
        if i['dest'] == curr['dest']:
          return True
      except KeyError:
        #doesnt have a dest, its okay just keep checking
        continue
    return False
  def checkRAW(self, curr):
    if not 'operands' in curr.keys():
      #instuction has no operands, just execute
      return False
    operands = curr['operands']
    all = self.active + self.noIssued
    for i in all:
      try:
        for j in operands:
          if j == i['dest']:
            #operand not ready
            return True
      except KeyError:
        #doesnt have a dest, its okay just keep checking
        continue
    return False
  def checkWAR(self, curr):
    if not 'dest' in curr.keys():
      #we aren't writing, don't sweat it
      return False
    all = self.active + self.noIssued
    for i in self.noIssued:
      try:
        operands = i['operands']
        for j in operands:
          if curr['dest'] == j:
            #hazards, don't execute
            return True
      except KeyError:
        #no operands in this one, no problem
        continue
    return False
  def checkLoads(self, curr):
    if 'lw' != curr['op']:
      #not a load word, no problem
      return False
    all = self.noIssued
    for i in all:
      if i['op'] == 'sw':
        return True
    return False
  def checkStores(self, curr):
    if 'sw' != curr['op']:
      #not a store
      return False
    for i in self.noIssued:
      if i['op'] == 'sw' or i['op'] == 'lw':
        return True
    return False
  def checkAll(self, curr):
    #bp()
    return self.checkWAW(curr) or self.checkRAW(curr) or self.checkWAR(curr) or self.checkLoads(curr) or self.checkStores(curr)
  
  def checkBranch(self, operands):
    all = self.noIssued + self.active
    for i in all:
      try:
        for j in operands:
          if j == i['dest']:
            return False
      except KeyError:
        continue
    return True