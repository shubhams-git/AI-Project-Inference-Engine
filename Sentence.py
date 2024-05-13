import re   # for regular expressions
class Sentence:
    """
    Enhanced implementation to handle negation (~), disjunction (||), and biconditional (<=>)
    within a general knowledge base's propositional logic sentences.
    """

    def __init__(self, sentence):
        self.symbols = []  # All unique symbols
        self.root = []  # Root atomic sentence from which child sentences branch
        self.atomic = {}  # Atomic sentences keyed by custom identifiers

        # Regular expression to split on the logical operators while keeping them
        original = re.split("(=>|&|\(|\)|~|\|\||<=>)", sentence)
        print("Original parts (after regex split but before cleaning):", original)
        # Cleaning empty strings and spaces
        self.original = [part for part in original if part.strip()]
        print("Original parts (after cleaning):", self.original)

        # Extracting symbols, ignoring logical operators
        symbols = re.split("=>|&|\(|\)|~|\|\||<=>", sentence)
        self.symbols = [part for part in symbols if part.strip()]
        print("Symbols extracted:", self.symbols)

        # Process the sentence to build its atomic structure
        self.root = self.__parse(self.original)
        print("Final root after parsing:", self.root)
        print("All atomic sentences created:", self.atomic)

    def __parse(self, parts):
        print("Parsing parts:", parts)
        # Handle nested expressions first by processing parenthesis blocks
        while '(' in parts:
            left_index = parts.index('(')
            right_index = self.__find_matching_parenthesis(parts, left_index)
            inner_expression = self.__parse(parts[left_index + 1:right_index])
            parts = parts[:left_index] + inner_expression + parts[right_index + 1:]
            print("Parts after processing parentheses:", parts)

        # Process all operations in order of precedence
        self.__process_operations(parts, ['~'])
        self.__process_operations(parts, ['&', '||'])
        self.__process_operations(parts, ['=>'])
        self.__process_operations(parts, ['<=>'])
        return parts

    def __find_matching_parenthesis(self, parts, start_index):
        depth = 1
        for index in range(start_index + 1, len(parts)):
            if parts[index] == '(':
                depth += 1
            elif parts[index] == ')':
                depth -= 1
            if depth == 0:
                return index
        raise ValueError("Mismatched parentheses in expression")

    def __process_operations(self, parts, operators):
        index = 0
        while index < len(parts):
            if parts[index] in operators:
                if parts[index] == '~':  # Unary negation
                    # Bind negation to the next logical part, even if it's an atomic expression
                    right = index + 1
                    if right < len(parts) and parts[right].startswith('atom'):
                        while right + 1 < len(parts) and parts[right + 1] not in operators:
                            right += 1
                    atomic = [parts[index], parts[index + 1]]
                    index = right
                    atom_key = 'atom' + str(len(self.atomic) + 1)
                    self.atomic[atom_key] = atomic
                    # Replace the expression with a reference to the atomic
                    parts[index - 1:index + 1] = [atom_key]  # Use index - 1 to index to replace correctly
                    index = index - 1  # Adjust index to continue after the newly created atom
                else:  # Binary operators
                    left = index - 1
                    right = index + 1
                    # Extend the right index to encompass the full atomic expression if applicable
                    if right < len(parts) and parts[right].startswith('atom'):
                        while right + 1 < len(parts) and parts[right + 1] not in operators:
                            right += 1

                    atomic = [parts[left], parts[index], parts[right]]
                    index = right  # Move index past the right operand
                    atom_key = 'atom' + str(len(self.atomic) + 1)
                    self.atomic[atom_key] = atomic
                    # Replace the expression with a reference to the atomic
                    parts[left:right + 1] = [atom_key]
                    index = left + 1  # Reset index to continue after the newly created atom
            else:
                index += 1



    def solve(self, model):
        print("Solving with model:", model)
        evaluations = {symbol: model[symbol] for symbol in self.symbols if symbol in model}
        for atom_key, components in self.atomic.items():
            print(f"Evaluating atomic {atom_key}: {components}")
            if components[0] == '~':
                evaluations[atom_key] = not evaluations[components[1]]
            elif components[1] == '&':
                evaluations[atom_key] = evaluations[components[0]] and evaluations[components[2]]
            elif components[1] == '||':
                evaluations[atom_key] = evaluations[components[0]] or evaluations[components[2]]
            elif components[1] == '=>':
                evaluations[atom_key] = not evaluations[components[0]] or evaluations[components[2]]
            elif components[1] == '<=>':
                evaluations[atom_key] = evaluations[components[0]] == evaluations[components[2]]
        final_result = evaluations[self.root[0]]
        print("Final result of the expression:", final_result)
        return final_result