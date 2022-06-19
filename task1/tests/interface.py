class StackDataStructure:
    stack = []

    def size(self):
        return len(self.stack)

    def empty(self):
        if len(self.stack) == 0:
            return True
        return False

    def push(self, element):
        if element is None:
            raise Exception('NullElementException')
        self.stack.append(element)

    def pop(self):
        if len(self.stack) == 0:
            raise Exception('EmptyStackException')
        return self.stack.pop()

    def peek(self):
        if len(self.stack) == 0:
            raise Exception('EmptyStackException')
        return self.stack[-1]
