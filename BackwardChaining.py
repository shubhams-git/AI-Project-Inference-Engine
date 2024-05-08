from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class BackwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.inferred = []  # Changed to a list to maintain the order of inferences

    def solve(self, query):
        """ Uses backward chaining to infer the query from the knowledge base. """
        if self.bc_recursive(query):
            return "YES: " + ", ".join(self.inferred)  # Maintain the order as elements were added
        else:
            return "NO"

    def bc_recursive(self, goal):
        if goal in self.inferred:
            return True
        # Check if the goal is a fact (unit clause)
        if any(goal == sentence.head and not sentence.conjuncts for sentence in self.kb.sentences if isinstance(sentence, HornForm)):
            if goal not in self.inferred:  # Only add if not already inferred
                self.inferred.append(goal)
            return True
        # Explore each rule where goal is the head
        for rule in self.kb.sentences:
            if isinstance(rule, HornForm) and rule.head == goal:
                # Recursively attempt to prove each of the premises
                if all(self.bc_recursive(premise) for premise in rule.conjuncts):
                    if goal not in self.inferred:  # Only add if not already inferred
                        self.inferred.append(goal)
                    return True
        return False
