from collections import deque
from pdb import set_trace as bp

class CacheMissError(BaseException):
  def __init__(self, address):
    self.address = address
  def __str__(self):
    return repr(address)
    
class Cache:
  def __init__(self, memory):
    self.sets = [Set(), Set(), Set(), Set()]
    self.missed = deque()
    self.memory = memory
  
  def __str__(self):
    out = ''
    for i, k in enumerate(self.sets):
      out += '\tSet %d: LRU=%d' % (i, k.lru) + '\n'
      for j, l in enumerate(k.entries):
        out += '\tEntry %d: [(%d, %d, %d,)<%s,%s>]' % (j, l.v, l.d, l.tag, bin(l.words[0]), bin(l.words[1])) + '\n'
    return out
    
  def memoryRead(self): #call once a cycle
    if len(self.missed) != 0:
      #get word from memory
      self.loadWord(self.missed.pop())
      
  def getWord(self, address):
    #bp()
    #calculate wo
    wo = (address >> 2) & 1
    #calculate index
    index = (address >> 3) & 3
    #calculate the tag
    tag = address >> 5
    set = self.sets[index]
    for i, entry in enumerate(set.entries):
      if entry.v == 1 and entry.tag == tag:
      #if it is in cache return the word
        set.lru = i ^ 1
        return entry.words[wo]
    else:
    #if not in cache, throw a cache miss exception
      
      self.missed.appendleft(address)
      raise CacheMissError(address)
    
    
  def loadWord(self, address):
    #calculate wo
    wo = (address >> 2) & 1
    #calculate index
    index = (address >> 3) & 3
    #calculate the tag
    tag = address >> 5
    #go into memery and find the address
    #if wo == 0, also fetch address + 4
    if wo == 0:
      words = [self.memory[address], self.memory[address + 4]]
    #else fetch address - 4
    else:
      words = [self.memory[address - 4], self.memory[address]]
    #put into LRU entry in the corresponding set
    set = self.sets[index]
    entry = set.entries[set.lru]
    if entry.d == 1:
      #find data address
      wbAddress = 0
      wbAddress += (entry.tag << 5)
      wbAddress += (index << 3)
      self.memory[wbAddress] = entry.words[0]
      self.memory[wbAddress + 4] = entry.words[1]
    entry.v = 1
    entry.tag = tag
    entry.words = words
    #flip LRU bit on that entry
    set.lru = set.lru ^ 1
  
  def storeWord(self, address, value):
    #calculate wo
    wo = (address >> 2) & 1
    #calculate index
    index = (address >> 3) & 3
    #calculate the tag
    tag = address >> 5
    set = self.sets[index]
    
    for i, entry in enumerate(set.entries):
      if entry.v and entry.tag == tag:
        set.lru = i ^ 1
        break
    else:
      self.missed.appendleft(address)
      raise CacheMissError(address)
    #update the value
    entry.words[wo] = value
    #set the valid and dirty bits
    entry.v = 1
    entry.d = 1
    
  def writeToMemory(self):
    #loop through all of cache
    for i, set in enumerate(self.sets):
      for j, entry in enumerate(set.entries):
        if entry.d and entry.v:
          #calculate address
          address = 0
          address += entry.tag << 5
          address += i << 3 #index
          #write data back
          self.memory[address] = entry.words[0]
          self.memory[address + 4] = entry.words[1]
          #set dirty bit back to zero
          entry.d = 0
class Set:
  def __init__(self):
    self.lru = 0
    self.entries = [Entry(), Entry()]

class Entry:
  def __init__(self):
    self.v = 0
    self.d = 0
    self.tag = 0
    self.words = [0, 0]