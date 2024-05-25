from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class BackwardChaining:
    def __init__(self, knowledge_base):
        """
        Initialize the BackwardChaining instance with a given knowledge base.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base containing propositional sentences.
        """
        self.kb = knowledge_base
        self.inferred = []  # List to maintain the order of inferences

    def solve(self, query):
        """
        Use backward chaining to infer the query from the knowledge base.

        Args:
            query (str): The query to be inferred.

        Returns:
            str: "YES" if the query can be inferred, "NO" otherwise.
        """
        if self.bc_recursive(query):
            return "YES: " + ", ".join(self.inferred)
        else:
            return "NO"

    def bc_recursive(self, goal):
        """
        Recursively perform backward chaining to prove the given goal.

        Args:
            goal (str): The goal to be proved.

        Returns:
            bool: True if the goal can be proved, False otherwise.
        """
        if goal in self.inferred:
            return True

        if any(goal == sentence.head and not sentence.conjuncts for sentence in self.kb.sentences if isinstance(sentence, HornForm)):
            if goal not in self.inferred:
                self.inferred.append(goal)
            return True

        for rule in self.kb.sentences:
            if isinstance(rule, HornForm) and rule.head == goal:
                if all(self.bc_recursive(premise) for premise in rule.conjuncts):
                    if goal not in self.inferred:
                        self.inferred.append(goal)
                    return True

        return False
