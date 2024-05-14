from Sentence import Sentence
from CNFConverter import CNFConverter

class ForwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.agenda = [(sentence.head, len(sentence.conjuncts)) for sentence in self.kb.sentences if not sentence.conjuncts]
        self.inferred = []

    def solve(self, query):
        while self.agenda:
            p, _ = self.agenda.pop(0)
            if p not in self.inferred:
                self.inferred.append(p)
            if p == query:
                return "YES: " + ", ".join(self.inferred)
            new_agenda_items = []
            for rule in self.kb.sentences:
                if p in rule.conjuncts and all(premise in self.inferred for premise in rule.conjuncts):
                    if rule.head not in self.inferred and rule.head not in [item[0] for item in new_agenda_items]:
                        new_agenda_items.append((rule.head, len(rule.conjuncts)))
            self.agenda.extend(new_agenda_items)
            self.agenda.sort(key=lambda x: x[1])
        return "NO"
