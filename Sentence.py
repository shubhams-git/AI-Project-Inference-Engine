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

    def __process_negations(self, parts):
        index = 0
        while index < len(parts):
            if parts[index] == '~':
                negated_literal = '~' + parts[index + 1]
                parts[index:index + 2] = [negated_literal]
                index -= 1
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

    def to_cnf_atomic(self):
        resolved_atoms = {}

        # Iterate over atomic operations and progressively convert to CNF
        for atom_key in sorted(self.atomic.keys()):
            parts = self.atomic[atom_key]
            print(f"\nResolving {atom_key}: {parts}")

            # Substitute resolved atoms with parentheses
            new_parts = []
            for part in parts:
                if part in resolved_atoms:
                    new_parts.extend(['('] + resolved_atoms[part] + [')'])
                else:
                    new_parts.append(part)
            parts = new_parts

            # Eliminate biconditionals
            parts = self.eliminate_biconditionals(parts)
            print(f"After eliminating biconditionals: {parts}")

            # Eliminate implications
            parts = self.eliminate_implications(parts)
            print(f"After eliminating implications: {parts}")

            # Move negations inward
            parts = self.move_negations_inward(parts)
            print(f"After moving negations inward: {parts}")

            # Distribute disjunctions over conjunctions
            parts = self.distribute_disjunctions(parts)
            print(f"After distributing disjunctions: {parts}")

            resolved_atoms[atom_key] = parts

        # Reconstruct the full CNF from the last resolved atomic part
        cnf_expression = resolved_atoms[sorted(resolved_atoms.keys())[-1]]

        # Apply simplification rules once at the end
        print(f"Before final simplification: {cnf_expression}")
        cnf_expression = self.simplify_expression(cnf_expression)
        print(f"After final simplification: {cnf_expression}")

        return cnf_expression

    def eliminate_biconditionals(self, parts):
        result = []
        i = 0
        while i < len(parts):
            if parts[i] == '<=>':
                left = result.pop()
                right = parts[i + 1]
                result += ['(', left, '=>', right, ')', '&', '(', right, '=>', left, ')']
                i += 1
            else:
                result.append(parts[i])
            i += 1
        return result

    def eliminate_implications(self, parts):
        result = []
        i = 0
        while i < len(parts):
            if parts[i] == '=>':
                left = result.pop()
                right = parts[i + 1]
                result += ['~' + left, '||', right]
                i += 1
            else:
                result.append(parts[i])
            i += 1
        return result

    def move_negations_inward(self, parts):
        result = []
        i = 0
        while i < len(parts):
            if parts[i].startswith('~'):
                negation_target = parts[i][1:].strip()
                if negation_target == '(':
                    left_index = i + 1
                    right_index = self.__find_matching_parenthesis(parts, left_index)
                    inner_parts = self.move_negations_inward(parts[left_index + 1:right_index])
                    result += ['('] + inner_parts + [')']
                    i = right_index
                elif negation_target.startswith('~'):
                    # Double negation
                    result.append(negation_target[1:])
                elif negation_target in ['&', '||']:
                    # Distribute negation over conjunction or disjunction
                    left = parts[i + 1]
                    right = parts[i + 3]
                    if negation_target == '&':
                        result += ['(', '~' + left, '||', '~' + right, ')']
                    else:
                        result += ['(', '~' + left, '&', '~' + right, ')']
                    i += 3
                else:
                    result.append(parts[i])
            else:
                result.append(parts[i])
            i += 1
        return result

    def distribute_disjunctions(self, parts):
        def distribute(a, b):
            if isinstance(a, list) and len(a) > 1 and a[0] == '&':
                return ['&'] + [distribute(sub_a, b) for sub_a in a[1:] if sub_a != '&']
            if isinstance(b, list) and len(b) > 1 and b[0] == '&':
                return ['&'] + [distribute(a, sub_b) for sub_b in b[1:] if sub_b != '&']
            return [a, '||', b]

        def split_and_clauses(expression):
            if isinstance(expression, list) and '&' in expression:
                clauses = []
                current_clause = []
                for token in expression:
                    if token == '&':
                        if current_clause:
                            clauses.append(current_clause)
                        current_clause = []
                    else:
                        current_clause.append(token)
                if current_clause:
                    clauses.append(current_clause)
                return clauses
            return [expression]

        def distribute_all(parts):
            if isinstance(parts, list) and '||' in parts:
                index = parts.index('||')
                left = parts[:index]
                right = parts[index + 1:]
                distributed = distribute(left, right)
                if '&' in distributed:
                    return split_and_clauses(distributed)
                return [distributed]
            return [parts]

        while True:
            new_parts = []
            for clause in parts:
                if isinstance(clause, list) and '||' in clause:
                    new_parts.extend(distribute_all(clause))
                else:
                    new_parts.append(clause)
            if new_parts == parts:
                break
            parts = new_parts

        return parts
    
    def simplify_expression(self, parts):
        # Flatten nested expressions
        def flatten(parts):
            stack = []
            for part in parts:
                if part == ')':
                    temp = []
                    while stack and stack[-1] != '(':
                        temp.append(stack.pop())
                    if stack and stack[-1] == '(':
                        stack.pop()  # Remove the matching '('
                    temp.reverse()
                    # If there's only one item inside the parentheses, we don't need the parentheses
                    if len(temp) == 1:
                        stack.append(temp[0])
                    else:
                        # Otherwise, we need to keep the parentheses
                        stack.append('(')
                        stack.extend(temp)
                        stack.append(')')
                else:
                    stack.append(part)
            return stack

        # Remove redundant parentheses for disjunctions
        def remove_redundant_parentheses(parts):
            i = 0
            while i < len(parts):
                if parts[i] == '(':
                    left_index = i
                    right_index = self.__find_matching_parenthesis(parts, left_index)
                    inner_expr = parts[left_index + 1:right_index]
                    if '||' in inner_expr and all(token != '&' for token in inner_expr):
                        parts = parts[:left_index] + inner_expr + parts[right_index + 1:]
                        i = left_index + len(inner_expr) - 1
                    else:
                        i = right_index
                i += 1
            return parts

        # Helper function to recursively simplify expressions inside parentheses
        def recursive_simplify(parts):
            i = 0
            while i < len(parts):
                if parts[i] == '(':
                    left_index = i
                    right_index = self.__find_matching_parenthesis(parts, left_index)
                    inner_expr = recursive_simplify(parts[left_index + 1:right_index])
                    if len(inner_expr) == 1:
                        parts = parts[:left_index] + inner_expr + parts[right_index + 1:]
                    else:
                        parts = parts[:left_index] + ['('] + inner_expr + [')'] + parts[right_index + 1:]
                    i = left_index + len(inner_expr)
                i += 1
            parts = flatten(parts)
            parts = remove_redundant_parentheses(parts)
            return parts

        # Maintain correct structure for conjunctions
        def handle_conjunctions(parts):
            # Remove all parentheses first
            parts = [part for part in parts if part != '(' and part != ')']
            # Add parentheses around expressions with '&'
            new_parts = []
            current_clause = []
            for part in parts:
                if part == '&':
                    if current_clause:
                        new_parts.append('(')
                        new_parts.extend(current_clause)
                        new_parts.append(')')
                        new_parts.append('&')
                        current_clause = []
                else:
                    current_clause.append(part)
            if current_clause:
                new_parts.append('(')
                new_parts.extend(current_clause)
                new_parts.append(')')
            return new_parts

        parts = recursive_simplify(parts)
        parts = handle_conjunctions(parts)
        return parts

# Example usage:
sentence = Sentence("(a => (c => ~d)) & b & (b => a)")
cnf = sentence.to_cnf_atomic()
print(f"Original expression: (a => (c => ~d)) & b & (b => a)")
print(f"CNF expression: {' '.join(cnf)}")
