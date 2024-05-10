from KnowledgeBase import KnowledgeBase
from itertools import product 

class TruthTable:
    """Implementation of Truth Table Entailment Method"""
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.count = 0  # To keep track of satisfying models

    def generate_truth_assignments(self):
        """Generate all possible truth assignments for the symbols in the knowledge base."""
        return list(product([True, False], repeat=len(self.kb.symbols)))

    def evaluate_knowledge_base(self, assignments):
        """Evaluate the knowledge base against each assignment to find satisfying models."""
        satisfying_models = []
        for assignment in assignments:
            truth_dict = dict(zip(self.kb.symbols, assignment))
            # Use the `solve` method from each Sentence or HornForm object in the knowledge base
            if all(sentence.solve(truth_dict) for sentence in self.kb.sentences):
                satisfying_models.append(truth_dict)
                self.count += 1  # Increment the model count if the KB is satisfied
        return satisfying_models

    def check_query_entailment(self, query, satisfying_models):
        """Check if the query is true in all models that satisfy the KB."""
        for model in satisfying_models:
            if not model.get(query, False):  # Check if the query is true in the model
                return "NO"
        return "YES: " + str(self.count)  # Return "YES" and the count of models if the query is always true

    def solve(self, query):
        """Solves the query using the truth table method by checking entailment."""
        assignments = self.generate_truth_assignments()  # Generate all truth assignments
        models = self.evaluate_knowledge_base(assignments)  # Evaluate these assignments
        result = self.check_query_entailment(query, models)  # Check if the query is entailed
        return result