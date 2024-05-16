import re

class HornForm:
    def __init__(self, sentence):
        self.clause = []
        self.symbols = []
        self.head = ""
        self.conjuncts = []
        self.root = []

        # Separate connectives and symbols
        self.clause = re.split("(=>|&|\(|\)|~|\|\||<=>)", sentence)
        while("" in self.clause):
            self.clause.remove("")
        while("(" in self.clause):
            self.clause.remove("(")
        while(")" in self.clause):
            self.clause.remove(")")
        if ('~' or '||' or '<=>') in self.clause:
            raise Exception("Sentence is not in horn form ", self.clause)

        if len(self.clause) == 1:
            self.head = self.clause[0]
        else:
            index = self.clause.index('=>')
            right = self.clause[index+1:]
            if (len(right) > 1):
                raise Exception("Error horn form format", self.clause)
            self.head = right[0]
            left = self.clause[:index]
            if (left[0] or left[-1]) == '&':
                raise Exception("Error horn form format", self.clause)
            for i in range(len(left)-1):
                if left[i] == left[i+1]:
                    raise Exception("Error horn form format", self.clause)
            for ele in left:
                if ele != '&':
                    self.conjuncts.append(ele)
            self.symbols = self.conjuncts.copy()
        if self.head not in self.symbols:
            self.symbols.append(self.head)
        self.root = [self.head] + self.conjuncts
