from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from CNFConverter import CNFConverter

class ForwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        # Initialize agenda with sentences that are unit clauses (facts)
        self.agenda = [symbol for sentence in self.kb.sentences for symbol in sentence.symbols if len(sentence.root) == 1]
        self.inferred = []

    def solve(self, query):
        while self.agenda:
            p = self.agenda.pop(0)
            if p not in self.inferred:
                self.inferred.append(p)
            if p == query:
                return "YES: " + ", ".join(self.inferred)
            # Check if new inferences can be made based on the newly added fact
            new_agenda_items = []
            for rule in self.kb.sentences:
                if p in rule.symbols:
                    # Check if all premises are already inferred
                    if all(premise in self.inferred for premise in rule.symbols if premise != p):
                        for head in rule.symbols:
                            if head not in self.inferred and head not in new_agenda_items:
                                new_agenda_items.append(head)
            self.agenda.extend(new_agenda_items)
        return "NO"
