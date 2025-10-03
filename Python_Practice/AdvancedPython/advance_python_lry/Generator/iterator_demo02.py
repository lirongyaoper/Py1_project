class Square:
    def __init__(self,count):
        self.count = count
        self.current = 0
    def __iter__(self):
        return self
    def __next__(self):
        result = self.current**2
        self.current += 1
        if self.current >= self.count:
            raise StopIteration
        return result
