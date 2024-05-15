from KnowledgeBase import KnowledgeBase
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
        # Check if the goal is a fact (unit clause)
        if any(goal in sentence.symbols and len(sentence.root) == 1 for sentence in self.kb.sentences):
            if goal not in self.inferred:
                self.inferred.append(goal)
            return True
        # Explore each rule where goal appears in the head
        for rule in self.kb.sentences:
            if goal in rule.symbols:
                # Recursively attempt to prove each of the premises
                if all(self.bc_recursive(premise) for premise in rule.symbols if premise != goal):
                    if goal not in self.inferred:
                        self.inferred.append(goal)
                    return True
        return False
