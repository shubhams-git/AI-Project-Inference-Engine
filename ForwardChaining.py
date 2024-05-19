from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class ForwardChaining:
    def __init__(self, knowledge_base):
        """
        Initialize the ForwardChaining instance.
        
        :param knowledge_base: An instance of the KnowledgeBase containing sentences.
        """
        self.kb = knowledge_base
        self.agenda = [(sentence.head, len(sentence.conjuncts)) 
                       for sentence in self.kb.sentences 
                       if isinstance(sentence, HornForm) and not sentence.conjuncts]
        self.inferred = []  # List to maintain the order of inferred symbols

    def solve(self, query):
        """
        Use forward chaining to infer the query from the knowledge base.
        
        :param query: The query symbol to be inferred.
        :return: "YES: [inferred symbols]" if the query is entailed, otherwise "NO".
        """
        while self.agenda:
            p, _ = self.agenda.pop(0)  # Get the next fact from the agenda
            if p not in self.inferred:  # Avoid duplicates
                self.inferred.append(p)

            if p == query:  # If the query is found in inferred symbols
                return "YES: " + ", ".join(self.inferred)

            # Check for new inferences based on the newly inferred fact
            new_agenda_items = []
            for rule in self.kb.sentences:
                if isinstance(rule, HornForm) and p in rule.conjuncts:
                    if all(premise in self.inferred for premise in rule.conjuncts):
                        if rule.head not in self.inferred and rule.head not in [item[0] for item in new_agenda_items]:
                            new_agenda_items.append((rule.head, len(rule.conjuncts)))

            # Update agenda with new items and sort to maintain priority
            self.agenda.extend(new_agenda_items)
            self.agenda.sort(key=lambda x: x[1])
        
        return "NO"  # If the query cannot be inferred
