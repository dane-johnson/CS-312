class CacheMissError(Exeption):
  def __init__(self, address):
    self.address = address
  def __str__(self):
    return repr(address)
    
class Cache:
  def __init__(self, memory):
    self.sets = [Set(), Set(), Set(), Set()]
    self.missed = []
    
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
    
    entry = sets[index].entry[set[index].lru]
    if entry.v = 1:
      return entry[wo]
    else:
      missed = address
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