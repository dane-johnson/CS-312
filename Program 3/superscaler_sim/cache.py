class CacheMissError(Exeption):
  def __init__(self, address):
    self.address = address
  def __str__(self):
    return repr(address)
    
class Cache:
  def __init__(self, memory):
    self.sets = [Set(), Set(), Set(), Set()]
    self.missed = -1
  def getWord(self, address):
    if missed != -1:
      pass
      #get word from memory
    raise CacheMissError(address)
    #if it is in cache return the word
    #if not in cache, throw a cache miss exception
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
      words = (memory[address], memory[address + 4])
    #else fetch address - 4
    else:
      words = (memory[address - 4], memory[address])
    #put into LRU entry in the corresponding set
    #flip LRU bit on that entry
    
    
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