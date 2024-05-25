from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class ForwardChaining:
    def __init__(self, knowledge_base):
        """
        Initialize the ForwardChaining instance.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base containing propositional sentences.
        """
        self.kb = knowledge_base
        self.agenda = [(sentence.head, len(sentence.conjuncts)) 
                       for sentence in self.kb.sentences 
                       if isinstance(sentence, HornForm) and not sentence.conjuncts]
        self.inferred = []

    def solve(self, query):
        """
        Use forward chaining to infer the query from the knowledge base.

        Args:
            query (str): The query symbol to be inferred.

        Returns:
            str: "YES: [inferred symbols]" if the query is entailed, otherwise "NO".
        """
        while self.agenda:
            p, _ = self.agenda.pop(0)
            if p not in self.inferred:
                self.inferred.append(p)

            if p == query:
                return "YES: " + ", ".join(self.inferred)

            new_agenda_items = []
            for rule in self.kb.sentences:
                if isinstance(rule, HornForm) and p in rule.conjuncts:
                    if all(premise in self.inferred for premise in rule.conjuncts):
                        if rule.head not in self.inferred and rule.head not in [item[0] for item in new_agenda_items]:
                            new_agenda_items.append((rule.head, len(rule.conjuncts)))

            self.agenda.extend(new_agenda_items)
            self.agenda.sort(key=lambda x: x[1])
        
        return "NO"
