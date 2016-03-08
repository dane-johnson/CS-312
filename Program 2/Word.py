class Word:
	word = 0;
	def __init__(self, word):
		self.word = word
		
class Instruction(Word):
	addr = 0;
	def __init__(self, word, addr):
		self.word = word
		self.addr = addr
	def __getitem__(self, index):
		return {
			'op'    : ((self.word & 0b11111100000000000000000000000000) >> 26),
			'rs'    : ((self.word & 0b00000011111000000000000000000000) >> 21),
			'rt'    : ((self.word & 0b00000000000111110000000000000000) >> 16),
			'rd'    : ((self.word & 0b00000000000000001111100000000000) >> 11),
			'sa'    : ((self.word & 0b00000000000000000000011111000000) >> 6),
			'func'  :  (self.word & 0b00000000000000000000000000111111),
			'immed' :  (self.word & 0b00000000000000001111111111111111),
			'addr'  :  (self.word & 0b00000011111111111111111111111111)
		}[index]
		