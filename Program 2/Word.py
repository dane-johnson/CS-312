class Word:
	word = 0;
	def __init__(self, word):
		self.word = word
		
class IncorrectIdentifierException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return self.value + " is not an identifier"
		
class Instruction(Word):
	addr = 0;
	def __init__(self, word, addr):
		self.word = word
		self.addr = addr
	@classmethod
	def convert6BitSignedToUnsigned(cls, num):
		negBitMask  = 0b100000
		flipBitMask = 0b111111
		if (negBitMask & num) > 0:
			num = num ^ flipBitMask
			num = num + 1
			num = num * -1
		return num
	@classmethod
	def convert5BitSignedToUnsigned(cls, num):
		negBitMask  = 0b10000
		flipBitMask = 0b11111
		if (negBitMask & num) > 0:
			num = num ^ flipBitMask
			num = num + 1
			num = num * -1
		return num
	@classmethod
	def convert16BitSignedToUnsigned(cls, num):
		negBitMask  = 0x8000
		flipBitMask = 0xFFFF
		if (negBitMask & num) > 0:
			num = num ^ flipBitMask
			num = num + 1
			num = num * -1
		return num
			
	def __getitem__(self, index):
		if   index == 'op': return (self.word & 0b11111100000000000000000000000000) >> 26
		elif index == 'rs': return Instruction.convert5BitSignedToUnsigned((self.word & 0b00000011111000000000000000000000) >> 21)
		elif index == 'rt': return Instruction.convert5BitSignedToUnsigned((self.word & 0b00000000000111110000000000000000) >> 16)
		elif index == 'rd': return Instruction.convert5BitSignedToUnsigned((self.word & 0b00000000000000001111100000000000) >> 11)
		elif index == 'sa': return Instruction.convert6BitSignedToUnsigned((self.word & 0b00000000000000000000011111000000) >> 6)
		elif index == 'func': return self.word & 0b00000000000000000000000000111111
		elif index == 'immed': return Instruction.convert16BitSignedToUnsigned(self.word & 0b00000000000000001111111111111111)
		elif index == 'addr' :  return self.word & 0b00000011111111111111111111111111
		else: raise IncorrectIdentifierException(index)
		