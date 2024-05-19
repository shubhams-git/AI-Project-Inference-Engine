import re
import sympy
from sympy.logic.boolalg import Not, And, Or, Implies, Equivalent, to_cnf

class Sentence:
    def __init__(self, sentence):
        """
        Initializes the Sentence object by parsing the input propositional logic sentence.

        Args:
            sentence (str): The propositional logic sentence to be parsed.
        """
        self.symbols = []  # List to store all unique symbols in the sentence.
        self.root = []  # Root atomic sentence from which child sentences branch.
        self.atomic = {}  # Dictionary to store atomic sentences keyed by custom identifiers.

        # Split the original sentence into components and remove whitespace.
        original = re.split(r"(=>|&|\(|\)|~|\|\||<=>)", sentence)
        self.original = [part.strip() for part in original if part.strip()]

        # Extract symbols while handling negations correctly.
        symbols = re.split(r"=>|&|\(|\)|\|\||<=>|~", sentence)
        self.symbols = [part.strip() for part in symbols if part.strip()]

        # Parse the sentence to create a structured representation.
        self.root = self.__parse(self.original)

    def __parse(self, parts):
        """
        Parses the components of the sentence to create a structured representation.

        Args:
            parts (list): List of components to be parsed.

        Returns:
            list: Parsed components.
        """
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
        """
        Finds the matching parenthesis for a given starting index.

        Args:
            parts (list): List of components containing parentheses.
            start_index (int): The starting index of the parenthesis.
            direction (str): Direction to search for the matching parenthesis ('forward' or 'backward').

        Returns:
            int: The index of the matching parenthesis.

        Raises:
            ValueError: If mismatched parentheses are found.
        """
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
        """
        Processes negations in the sentence components.

        Args:
            parts (list): List of components to be processed.
        """
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
        """
        Processes logical operations in the sentence components.

        Args:
            parts (list): List of components to be processed.
            operators (list): List of operators to process.
        """
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
        """
        Evaluates the truth value of the sentence based on the given model.

        Args:
            model (dict): Dictionary containing the truth values of symbols.

        Returns:
            bool: The truth value of the sentence.
        """
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
        """
        Converts the atomic sentence to a SymPy expression.

        Args:
            atom: Atomic sentence to be converted.

        Returns:
            sympy.Expr: The corresponding SymPy expression.
        """
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
        """
        Converts the root sentence to its CNF (Conjunctive Normal Form) representation.

        Returns:
            sympy.Expr: The CNF representation of the root sentence.
        """
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
