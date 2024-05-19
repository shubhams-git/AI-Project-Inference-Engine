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
            return "YES: " + ", ".join(self.inferred)  # Maintain the order of inferences
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
        # Check if the goal has already been inferred
        if goal in self.inferred:
            return True

        # Check if the goal is a fact (unit clause) in the knowledge base
        if any(goal == sentence.head and not sentence.conjuncts for sentence in self.kb.sentences if isinstance(sentence, HornForm)):
            if goal not in self.inferred:
                self.inferred.append(goal)
            return True

        # Explore each rule where the goal is the head
        for rule in self.kb.sentences:
            if isinstance(rule, HornForm) and rule.head == goal:
                # Recursively attempt to prove each of the premises (conjuncts)
                if all(self.bc_recursive(premise) for premise in rule.conjuncts):
                    if goal not in self.inferred:
                        self.inferred.append(goal)
                    return True

        # Return False if the goal cannot be proved
        return False
