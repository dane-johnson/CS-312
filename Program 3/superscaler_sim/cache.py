from collections import deque

class CacheMissError(BaseException):
  def __init__(self, address):
    self.address = address
  def __str__(self):
    return repr(address)
    
class Cache:
  def __init__(self, memory):
    self.sets = [Set(), Set(), Set(), Set()]
    self.missed = deque()
    
  def memoryRead(self): #call once a cycle
    if len(missed) != 0:
      #get word from memory
      self.loadWord(missed.pop())
      
  def getWord(self, address):
    #calculate wo
    wo = (address >> 2) & 1
    #calculate index
    index = (address >> 3) & 3
    #calculate the tag
    tag = address >> 5
    set = self.sets[index]
    entry = set.entries[set.lru]
    if entry.v == 1:
    #if it is in cache return the word
      return entry[wo]
    else:
    #if not in cache, throw a cache miss exception
      missed.appendleft(address)
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
      words = [memory[address], memory[address + 4]]
    #else fetch address - 4
    else:
      words = [memory[address - 4], memory[address]]
    #put into LRU entry in the corresponding set
    set = self.sets[index]
    entry = set.entries[set.lru]
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
    entry = set.entries[set.lru]
    
    if not entry.v or entry.tag != tag:
      #cache miss 
      missed.appendleft(address)
      raise CacheMissError(address)
    else:
      #update the value
      entry.words[wo] = value
      #set the valid and dirty bits
      entry.v = 1
      entry.d = 1
      #update the lru
      set.lru ^ 1
    
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
          memory[address] = entry.words[0]
          memory[address + 4] = entry.words[1]
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