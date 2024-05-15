import re

class Sentence:
    def __init__(self, sentence):
        self.symbols = []  # All unique symbols
        self.root = []  # Root atomic sentence from which child sentences branch
        self.atomic = {}  # Atomic sentences keyed by custom identifiers

        original = re.split(r"(=>|&|\(|\)|~|\|\||<=>)", sentence)
        self.original = [part.strip() for part in original if part.strip()]

        # Adjust to handle negations correctly
        symbols = re.split(r"=>|&|\(|\)|\|\||<=>", sentence)
        self.symbols = [self.__combine_negation(part.strip()) for part in symbols if part.strip()]

        self.root = self.__parse(self.original)

    def __combine_negation(self, part):
        # Combine '~' with the following literal
        if part.startswith('~'):
            return part
        return part

    def __parse(self, parts):
        while '(' in parts:
            left_index = parts.index('(')
            right_index = self.__find_matching_parenthesis(parts, left_index)
            inner_expression = self.__parse(parts[left_index + 1:right_index])
            parts = parts[:left_index] + inner_expression + parts[right_index + 1:]

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
                if parts[index] == '~':
                    atomic = [parts[index] + parts[index + 1]]
                    atom_key = 'atom' + str(len(self.atomic) + 1)
                    self.atomic[atom_key] = atomic
                    parts[index:index + 2] = [atom_key]
                else:
                    atomic = [parts[index - 1], parts[index], parts[index + 1]]
                    atom_key = 'atom' + str(len(self.atomic) + 1)
                    self.atomic[atom_key] = atomic
                    parts[index - 1:index + 2] = [atom_key]
                    index -= 1
            index += 1

    def solve(self, model):
        evaluations = {symbol.strip(): model[symbol.strip()] for symbol in self.symbols if symbol.strip() in model}
        for atom_key, components in self.atomic.items():
            if components[0] == '~':
                evaluations[atom_key] = not evaluations[components[1].strip()]
            elif components[1] == '&':
                evaluations[atom_key] = evaluations[components[0].strip()] and evaluations[components[2].strip()]
            elif components[1] == '||':
                evaluations[atom_key] = evaluations[components[0].strip()] or evaluations[components[2].strip()]
            elif components[1] == '=>':
                evaluations[atom_key] = not evaluations[components[0].strip()] or evaluations[components[2].strip()]
            elif components[1] == '<=>':
                evaluations[atom_key] = evaluations[components[0].strip()] == evaluations[components[2].strip()]
        final_result = evaluations[self.root[0]]
        return final_result

    def to_cnf(self):
        # Converts the internal representation of the sentence to CNF
        return self.root
