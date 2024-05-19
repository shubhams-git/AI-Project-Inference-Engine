from Sentence import Sentence
from HornForm import HornForm

class KnowledgeBase:
    """
    KnowledgeBase is used to store propositional logic statements and their corresponding symbols.
    """

    def __init__(self, sentences, type):
        """
        Initializes the KnowledgeBase with a list of sentences and the type of sentences (Horn Form or General Sentences).
        
        Args:
            sentences (list of str): List of propositional logic sentences.
            type (str): Type of sentences ('HF' for Horn Form, 'GS' for General Sentences).
        """
        self.sentences = []  # List to store sentences in the knowledge base
        self.symbols = []    # List to store all unique symbols found in the sentences
        if type in ['HF', 'GS']:  # Check if the provided type is valid
            self.type = type
        else:
            raise Exception("Unknown sentence type.")

        # Add each sentence to the knowledge base
        for sentence in sentences:
            self.tell(sentence)

    def tell(self, sentence):
        """
        Adds a sentence to the knowledge base. The sentence is parsed and stored according to its type.
        
        Args:
            sentence (str): A propositional logic sentence.
        """
        # Create and add the sentence of the specified type to the knowledge base
        if self.type == 'HF':
            new = HornForm(sentence)
        elif self.type == 'GS':
            new = Sentence(sentence)
        
        # Append the parsed sentence to the knowledge base
        self.sentences.append(new)
        
        # Add new symbols to the knowledge base if found
        for symbol in new.symbols:
            if symbol not in self.symbols:
                self.symbols.append(symbol)
