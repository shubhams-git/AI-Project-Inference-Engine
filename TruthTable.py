from itertools import product
from Sentence import Sentence
from CNFConverter import CNFConverter

class TruthTable:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.count = 0

    def generate_truth_assignments(self):
        return list(product([True, False], repeat=len(self.kb.symbols)))

    def evaluate_knowledge_base(self, assignments):
        satisfying_models = []
        for assignment in assignments:
            truth_dict = dict(zip(self.kb.symbols, assignment))
            if all(sentence.solve(truth_dict) for sentence in self.kb.sentences):
                satisfying_models.append(truth_dict)
                self.count += 1
        return satisfying_models

    def check_query_entailment(self, query, satisfying_models):
        for model in satisfying_models:
            if not model.get(query, False):
                return "NO"
        return "YES: " + str(self.count)

    def solve(self, query):
        assignments = self.generate_truth_assignments()
        models = self.evaluate_knowledge_base(assignments)
        result = self.check_query_entailment(query, models)
        return result
