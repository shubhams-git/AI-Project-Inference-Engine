import re
import sympy
from sympy.logic.boolalg import Not, And, Or, Implies, Equivalent, to_cnf

class Sentence:
    def __init__(self, sentence):
        self.symbols = []  # All unique symbols
        self.root = []  # Root atomic sentence from which child sentences branch
        self.atomic = {}  # Atomic sentences keyed by custom identifiers

        original = re.split(r"(=>|&|\(|\)|~|\|\||<=>)", sentence)
        self.original = [part.strip() for part in original if part.strip()]

        # Adjust to handle negations correctly
        symbols = re.split(r"=>|&|\(|\)|\|\||<=>|~", sentence)
        self.symbols = [part.strip() for part in symbols if part.strip()]

        self.root = self.__parse(self.original)

    def __parse(self, parts):
        while '(' in parts:
            left_index = parts.index('(')
            right_index = self.__find_matching_parenthesis(parts, left_index)
            inner_expression = self.__parse(parts[left_index + 1:right_index])
            parts = parts[:left_index] + inner_expression + parts[right_index + 1:]

        self.__process_negations(parts)
        self.__process_operations(parts, ['&', '||'])
        self.__process_operations(parts, ['=>'])
        self.__process_operations(parts, ['<=>'])
        return parts

    def __find_matching_parenthesis(self, parts, start_index, direction="forward"):
        depth = 1
        if direction == "forward":
            for index in range(start_index + 1, len(parts)):
                if parts[index] == '(':
                    depth += 1
                elif parts[index] == ')':
                    depth -= 1
                if depth == 0:
                    return index
        elif direction == "backward":
            for index in range(start_index - 1, -1, -1):
                if parts[index] == ')':
                    depth += 1
                elif parts[index] == '(':
                    depth -= 1
                if depth == 0:
                    return index
        raise ValueError("Mismatched parentheses in expression")

    def __process_negations(self, parts):
        index = 0
        while index < len(parts):
            if parts[index] == '~':
                negated_literal = parts[index + 1]
                atom_key = 'atom' + str(len(self.atomic) + 1)
                self.atomic[atom_key] = ['~', negated_literal]
                parts[index:index + 2] = [atom_key]
            else:
                index += 1

    def __process_operations(self, parts, operators):
        index = 0
        while index < len(parts):
            if parts[index] in operators:
                left_operand = parts[index - 1]
                operator = parts[index]
                right_operand = parts[index + 1]
                atomic = [left_operand, operator, right_operand]
                atom_key = 'atom' + str(len(self.atomic) + 1)
                self.atomic[atom_key] = atomic
                parts[index - 1:index + 2] = [atom_key]
                index -= 1
            index += 1

    def solve(self, model):
        evaluations = {symbol.strip(): model[symbol.strip()] for symbol in self.symbols if symbol.strip() in model}
        for atom_key, components in self.atomic.items():
            if len(components) == 2 and components[0].startswith('~'):
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
    
    def to_sympy_expr(self, atom):
        if isinstance(atom, list):
            if len(atom) == 2 and atom[0] == '~':
                return Not(self.to_sympy_expr(atom[1]))
            elif len(atom) == 3:
                left = self.to_sympy_expr(atom[0])
                right = self.to_sympy_expr(atom[2])
                if atom[1] == '&':
                    return And(left, right)
                elif atom[1] == '||':
                    return Or(left, right)
                elif atom[1] == '=>':
                    return Implies(left, right)
                elif atom[1] == '<=>':
                    return Equivalent(left, right)
        elif atom in self.atomic:
            return self.to_sympy_expr(self.atomic[atom])
        else:
            return sympy.Symbol(atom)

    def to_cnf_atomic(self):
        root_expr = self.to_sympy_expr(self.root[0])
        cnf_expr = to_cnf(root_expr, simplify=True)
        return cnf_expr

if __name__ == "__main__":
    # Example usage:
    sentence = Sentence("(a <=> (c => ~d)) & b & (b => a)")
    cnf = sentence.to_cnf_atomic()
    print(f"Original expression: (a <=> (c => ~d)) & b & (b => a)")
    print("Atomic sentences:", sentence.atomic)
    print(f"CNF expression: {cnf}")
