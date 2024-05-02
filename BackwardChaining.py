from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class BackwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.inferred = set()

    def solve(self, query):
        """ Uses backward chaining to infer the query from the knowledge base. """
        if self.bc_recursive(query):
            return "YES: " + ", ".join(sorted(self.inferred))
        else:
            return "NO"

    def bc_recursive(self, goal):
        if goal in self.inferred:
            return True
        if any(goal == sentence.head and not sentence.conjuncts for sentence in self.kb.sentences if isinstance(sentence, HornForm)):
            self.inferred.add(goal)
            return True
        for rule in self.kb.sentences:
            if isinstance(rule, HornForm) and rule.head == goal:
                if all(self.bc_recursive(premise) for premise in rule.conjuncts):
                    self.inferred.add(goal)
                    return True
        return False
