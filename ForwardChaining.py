from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class ForwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        # Initialize agenda with sentences that can be considered as facts (unit clauses)
        self.agenda = [sentence.head for sentence in self.kb.sentences if isinstance(sentence, HornForm) and not sentence.conjuncts]
        self.inferred = set(self.agenda)  # Start with these as already inferred

    def solve(self, query):
        """ Uses forward chaining to infer the query from the knowledge base. """
        while self.agenda:
            p = self.agenda.pop(0)
            if p == query:
                return "YES: " + ", ".join(sorted(self.inferred))
            self.inferred.add(p)
            for rule in self.kb.sentences:
                if isinstance(rule, HornForm) and p in rule.conjuncts and all(premise in self.inferred for premise in rule.conjuncts):
                    if rule.head not in self.inferred:
                        self.agenda.append(rule.head)
                        self.inferred.add(rule.head)
                        if rule.head == query:
                            return "YES: " + ", ".join(sorted(self.inferred))
        return "NO"
