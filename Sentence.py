import re

class Sentence:
    """General Sentence Structure for a General Knowledge Base.
       Formats passed propositional logic in text to a structure that can be
       solved using models.
    """
    def __init__(self, sentence):
        self.symbols = []   # Symbols within the sentence
        self.root = []      # Root atomic sentence which child atomic sentences branch from
        self.atomic = {}    # Dictionary of atomic sentences within sentence, keys are used to link atomic sentences

        # Separate connectives and symbols
        original = re.split(r"(=>|&|\(|\)|~|\|\||<=>)", sentence)
        # Remove empty strings from the list
        original = [item for item in original if item.strip()]
        self.original = original
        # Use regular expressions to extract symbols from sentence
        self.symbols = list(set(re.findall(r"[a-zA-Z]+", sentence)))  # Only match alphabetic characters
        # Extract atomic sentences from the original sentence
        self.root = self.__parse(self.original)  # Final atomic sentence is the root sentence

    def __parse(self, sentence):
        """Recursively parse sentences to handle precedence and associativity of logical operators."""
        # Handle parentheses first (highest precedence)
        while '(' in sentence:
            left_index = sentence.index('(')
            right_index = self.__find_matching_paren(sentence, left_index)
            # Extract and parse the content within the parentheses
            section = sentence[left_index + 1:right_index]
            parsed_section = self.__parse(section)
            # Replace the section in the original sentence with the parsed result
            sentence = sentence[:left_index] + parsed_section + sentence[right_index + 1:]

        # Process all operators by precedence
        sentence = self.__process_negation(sentence)
        sentence = self.__process_binary_operators(sentence, ['&', '||'])
        sentence = self.__process_binary_operators(sentence, ['=>', '<=>'])
        
        return sentence

    def __find_matching_paren(self, sentence, open_index):
        """Find the matching parenthesis in the sentence."""
        depth = 0
        for i in range(open_index, len(sentence)):
            if sentence[i] == '(':
                depth += 1
            elif sentence[i] == ')':
                depth -= 1
            if depth == 0:
                return i
        raise ValueError("Unmatched parenthesis in expression.")
    
    def __process_negation(self, sentence):
        """Process negation, which has the highest precedence after parentheses."""
        i = 0
        while i < len(sentence):
            if sentence[i] == '~':
                # Ensure there are no leading or trailing spaces
                target = sentence[i + 1].strip()
                atom_key = f"atom{len(self.atomic)+1}"
                self.atomic[atom_key] = ['~', target]
                sentence = sentence[:i] + [atom_key] + sentence[i + 2:]
            i += 1
        return sentence
    
    def __process_binary_operators(self, sentence, operators):
        """Process binary operators (AND, OR, IMPLIES, BICONDITIONAL) based on the specified list of operators."""
        i = 0
        while i < len(sentence):
            if sentence[i] in operators:
                left = sentence[i - 1].strip()  # Ensure no spaces for accurate matching
                right = sentence[i + 1].strip()  # Ensure no spaces for accurate matching
                atom_key = f"atom{len(self.atomic) + 1}"
                self.atomic[atom_key] = [left, sentence[i], right]
                sentence = sentence[:i - 1] + [atom_key] + sentence[i + 2:]
                i = 0  # Reset index to start to ensure full re-evaluation after changes
            else:
                i += 1
        return sentence


    def solve(self, model):
        """Evaluate the truth value of the sentence using a given model (assignment of truth values to symbols)."""
        bool_pairs = {symbol: model[symbol] for symbol in self.symbols if symbol in model}
        
        for key, expression in self.atomic.items():
            if expression[0] == '~':
                bool_pairs[key] = not bool_pairs[expression[1]]
            else:
                left, operator, right = expression
                left_val = bool_pairs[left]
                right_val = bool_pairs[right]
                if operator == '&':
                    bool_pairs[key] = left_val and right_val
                elif operator == '||':
                    bool_pairs[key] = left_val or right_val
                elif operator == '=>':
                    bool_pairs[key] = not left_val or right_val
                elif operator == '<=>':
                    bool_pairs[key] = left_val == right_val

        return bool_pairs[self.root[0]]  # Return the evaluation of the root sentence
    
    def display(self):
        """Utility method to display the internal state of the sentence."""
        print("Original Input Expression:")
        print(" ".join(self.original))

        print("\nExtracted Symbols:")
        print(", ".join(sorted(self.symbols)))

        print("\nAtomic Sentences Breakdown:")
        for key, value in self.atomic.items():
            if value[0] == '~':  # Handling negation specially as it's unary
                print(f"{key}: Negation of ({value[1]})")
            else:
                # Joining the parts of the atomic sentence for display
                expression = " ".join(value)
                print(f"{key}: ({expression})")

        print("\nRoot of Expression Tree:")
        # Display the root element which ties all atomic sentences together at the top level
        print(self.root if self.root else "No root. Check expression parsing.")
