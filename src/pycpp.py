class StringStream:
    def __init__(self):
        self.parts = []

    def __lshift__(self, other):
        self.parts.append(str(other))
        return self  # Allow chaining

    def __str__(self):
        return ''.join(self.parts)

    def value(self):
        return str(self)