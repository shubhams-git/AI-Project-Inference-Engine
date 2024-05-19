import re

class HornForm:
    def __init__(self, sentence):
        """
        Initializes the HornForm object by parsing a given sentence.

        :param sentence: A string representing a Horn clause.
        """
        self.clause = []        # List to hold parts of the clause
        self.symbols = []       # List of unique symbols in the clause
        self.head = ""          # Head of the Horn clause
        self.conjuncts = []     # Conjunctive parts of the Horn clause
        self.root = []          # Root of the Horn clause

        # Split the sentence into parts using the specified delimiters
        self.clause = re.split("(=>|&|\(|\)|~|\|\||<=>)", sentence)
        
        # Remove any empty strings and parentheses from the list
        self.clause = [part for part in self.clause if part not in {"", "(", ")"}]

        # Check for invalid symbols indicating the sentence is not in Horn form
        if any(op in self.clause for op in {'~', '||', '<=>'}):
            raise Exception("Sentence is not in horn form", self.clause)

        # If the clause is a single symbol, set it as the head
        if len(self.clause) == 1:
            self.head = self.clause[0]
        else:
            # Find the index of the implication operator
            index = self.clause.index('=>')
            right = self.clause[index + 1:]

            # Ensure there is only one symbol on the right side of the implication
            if len(right) > 1:
                raise Exception("Error in horn form format", self.clause)
            self.head = right[0]

            left = self.clause[:index]

            # Check for improper formatting with the conjunction operator
            if left[0] == '&' or left[-1] == '&':
                raise Exception("Error in horn form format", self.clause)

            # Ensure no consecutive conjunction operators
            for i in range(len(left) - 1):
                if left[i] == '&' and left[i + 1] == '&':
                    raise Exception("Error in horn form format", self.clause)

            # Add all valid conjuncts to the conjuncts list
            self.conjuncts = [ele for ele in left if ele != '&']

            self.symbols = self.conjuncts.copy()

        # Add the head to the list of symbols if it is not already present
        if self.head not in self.symbols:
            self.symbols.append(self.head)

        # Set the root of the Horn clause
        self.root = [self.head] + self.conjuncts
