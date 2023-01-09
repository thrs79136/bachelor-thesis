class Bar:
    def __init__(self):
        self.content = []

    def __str__(self):
        return ', '.join([f'{chord.root.base_name}{chord.extension}' for chord in self.content])
