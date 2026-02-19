class IntegerSet:
    def __init__(self, max_size, elements=None):
        if elements is None:
            elements = []
        self.max_size = max_size
        self.elements = elements

    def __str__(self):
        return f"{self.elements}"

    def __repr__(self):
        return f"IntegerSet(max_size={self.max_size}, elements={self.elements})"
