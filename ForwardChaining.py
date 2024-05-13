from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class ForwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        # Initialize agenda with sentences that can be considered as facts (unit clauses)
        self.agenda = [(sentence.head, len(sentence.conjuncts)) for sentence in self.kb.sentences if isinstance(sentence, HornForm) and not sentence.conjuncts]
        self.inferred = []  # Changed to a list to maintain the order of inference

    def solve(self, query):
        """ Uses forward chaining to infer the query from the knowledge base. """
        while self.agenda:
            p, _ = self.agenda.pop(0)
            if p not in self.inferred:  # Check if not already inferred to avoid duplicates in the list
                self.inferred.append(p)
            
            if p == query:
                return "YES: " + ", ".join(self.inferred)  # Output the inferred in the order they were added
            
            # Check if new inferences can be made based on the newly added fact
            new_agenda_items = []
            for rule in self.kb.sentences:
                if isinstance(rule, HornForm) and p in rule.conjuncts and all(premise in self.inferred for premise in rule.conjuncts):
                    if rule.head not in self.inferred and rule.head not in [item[0] for item in new_agenda_items]:
                        new_agenda_items.append((rule.head, len(rule.conjuncts)))
            
            # Add new items and sort agenda to maintain priority
            self.agenda.extend(new_agenda_items)
            self.agenda.sort(key=lambda x: x[1])
        
        return "NO"
