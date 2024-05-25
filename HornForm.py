import re

class HornForm:
    def __init__(self, sentence):
        """
        Initializes the HornForm object by parsing a given sentence.

        Args:
            sentence (str): A string representing a Horn clause.
        """
        self.clause = []
        self.symbols = []
        self.head = ""
        self.conjuncts = []
        self.root = []

        self.clause = re.split("(=>|&|\(|\)|~|\|\||<=>)", sentence)
        self.clause = [part for part in self.clause if part not in {"", "(", ")"}]

        if any(op in self.clause for op in {'~', '||', '<=>'}):
            raise Exception("Sentence is not in horn form", self.clause)

        if len(self.clause) == 1:
            self.head = self.clause[0]
        else:
            index = self.clause.index('=>')
            right = self.clause[index + 1:]

            if len(right) > 1:
                raise Exception("Error in horn form format", self.clause)
            self.head = right[0]

            left = self.clause[:index]

            if left[0] == '&' or left[-1] == '&':
                raise Exception("Error in horn form format", self.clause)

            for i in range(len(left) - 1):
                if left[i] == '&' and left[i + 1] == '&':
                    raise Exception("Error in horn form format", self.clause)

            self.conjuncts = [ele for ele in left if ele != '&']
            self.symbols = self.conjuncts.copy()

        if self.head not in self.symbols:
            self.symbols.append(self.head)
        
        self.root = [self.head] + self.conjuncts
