from Sentence import Sentence
from HornForm import HornForm

class KnowledgeBase:
    """
    KnowledgeBase is used to store propositional logic statements and their corresponding symbols.
    """

    def __init__(self, sentences, type):
        """
        Initializes the KnowledgeBase with a list of sentences and the type of sentences.

        Args:
            sentences (list of str): List of propositional logic sentences.
            type (str): Type of sentences ('HF' for Horn Form, 'GS' for General Sentences).
        """
        self.sentences = []
        self.symbols = []
        if type in ['HF', 'GS']:
            self.type = type
        else:
            raise Exception("Unknown sentence type.")

        for sentence in sentences:
            self.tell(sentence)

    def tell(self, sentence):
        """
        Adds a sentence to the knowledge base. The sentence is parsed and stored according to its type.

        Args:
            sentence (str): A propositional logic sentence.
        """
        if self.type == 'HF':
            new = HornForm(sentence)
        elif self.type == 'GS':
            new = Sentence(sentence)
        
        self.sentences.append(new)
        
        for symbol in new.symbols:
            if symbol not in self.symbols:
                self.symbols.append(symbol)
