from itertools import product
from Sentence import Sentence

class TruthTable:
    def __init__(self, knowledge_base):
        """
        Initializes the TruthTable with a given knowledge base.
        
        :param knowledge_base: The knowledge base containing propositional logic sentences.
        """
        self.kb = knowledge_base
        self.count = 0

    def generate_truth_assignments(self):
        """
        Generates all possible truth assignments for the symbols in the knowledge base.
        
        :return: A list of tuples, each representing a possible truth assignment.
        """
        return list(product([True, False], repeat=len(self.kb.symbols)))

    def evaluate_knowledge_base(self, assignments):
        """
        Evaluates the knowledge base against all possible truth assignments.
        
        :param assignments: A list of all possible truth assignments.
        :return: A list of truth assignments that satisfy the knowledge base.
        """
        satisfying_models = []
        for assignment in assignments:
            truth_dict = dict(zip(self.kb.symbols, assignment))
            if all(sentence.solve(truth_dict) for sentence in self.kb.sentences):
                satisfying_models.append(truth_dict)
                self.count += 1
        return satisfying_models

    def check_query_entailment(self, query, satisfying_models):
        """
        Checks if the query is entailed by the knowledge base using the satisfying models.
        
        :param query: The query sentence to be checked.
        :param satisfying_models: A list of models that satisfy the knowledge base.
        :return: "YES" if the query is entailed, otherwise "NO".
        """
        query_expr = query.to_sympy_expr(query.root[0])
        for model in satisfying_models:
            # Check if all symbols in the query are in the model
            if all(symbol in model for symbol in query.symbols):
                if not query.solve(model):
                    return "NO"
            else:
                return "NO"
        return "YES: " + str(self.count)

    def solve(self, query):
        """
        Solves the query using the truth table method.
        
        :param query: The query sentence to be solved.
        :return: The result of the query entailment check.
        """
        assignments = self.generate_truth_assignments()
        models = self.evaluate_knowledge_base(assignments)
        result = self.check_query_entailment(query, models)
        return result

# Example usage
if __name__ == "__main__":
    from KnowledgeBase import KnowledgeBase
    from FileReader import FileReader
    tell, ask = FileReader.read("test.txt")
    kb = KnowledgeBase(tell, 'GS')
    query = Sentence(ask)
    tt = TruthTable(kb)
    print(tt.solve(query))
