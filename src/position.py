import sys

class BasePosition:
    def __init__(self, index, array):
        self.index=index
        self.array=array
    def peek(self, amount=1):
        next_index = self.index+amount
        if len(self.array)==next_index:
            return None
        return self.array[next_index]
    def consume(self, amount=1):
        res = self.peek(amount)
        self.index+=amount
        return res

class TokenPosition(BasePosition):
    def __init__(self, ln, start, index, source):
        super().__init__(index, source)
        self.ln = ln
        self.start = start
        self._consume = self.consume
        self.consume = self.__consume
    def highlight_line(self):
        return self.array.split("\n")[self.ln-1]
    def __consume(self, amount=1):
        res = self._consume(amount)
        self.start += 1
        if res == "\n":
            self.ln+=1
            self.start = 0
        return res
    def copy(self):
        return TokenPosition(self.ln,
                             self.start,
                             self.index,
                             self.array)
class ParserPosition(BasePosition):
    def __init__(self, index, tokens):
        super().__init__(index, tokens)
    def copy(self):
        return ParserPosition(self.index,
                              self.array)
    def get(self, token):
        next_tk=self.consume()
        if next_tk.token_type == token:
            return next_tk
        print(f"Expected: {token} got {next_tk.token_type}")
        sys.exit()
