

class LazyList:
    """http://www.logarithmic.net/pfh/blog/01193268742"""
    def __init__(self, iterator):
        self.data = []
        self.iterator = iter(iterator)

    def __getitem__(self, index):
        while len(self.data) <= index:
            try:
                self.data.append(next(self.iterator))
            except StopIteration:
                raise IndexError("list index out of range")
        return self.data[index]

    def __len__(self):
        for x in self.iterator:
            self.data.append(x)
        return len(self.data)
