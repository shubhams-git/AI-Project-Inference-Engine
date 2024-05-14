from Sentence import Sentence
from CNFConverter import CNFConverter

class BackwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.inferred = []

    def solve(self, query):
        if self.bc_recursive(query):
            return "YES: " + ", ".join(self.inferred)
        else:
            return "NO"

    def bc_recursive(self, goal):
        if goal in self.inferred:
            return True
        if any(goal == sentence.head and not sentence.conjuncts for sentence in self.kb.sentences):
            if goal not in self.inferred:
                self.inferred.append(goal)
            return True
        for rule in self.kb.sentences:
            if rule.head == goal:
                if all(self.bc_recursive(premise) for premise in rule.conjuncts):
                    if goal not in self.inferred:
                        self.inferred.append(goal)
                    return True
        return False
