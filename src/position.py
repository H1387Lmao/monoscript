class BasePosition:
    def __init__(self, index, array):
        self.index=index
        self.array=array
    def peek(self, amount=1):
        next_index = self.index+amount
        if len(self.array)==next_index:
            return None
        return self.array[peek]
    def consume(self, amount=1):
        res = self.peek(amount)
        self.index+=amount
        return res

class TokenPosition(BasePosition):
    def __init__(self, ln, start, index, source):
        self.ln = ln
        self.start = start
        super().__init__(self, index, source)
    def copy(self):
        return TokenPosition(self.ln,
                             self.start,
                             self.index,
                             self.array)
class ParserPosition(BasePosition):
    def __init__(self, index, tokens):
        super().__init__(self, index, tokens)
    def copy(self):
        return ParserPosition(self.index,
                              self.array)
