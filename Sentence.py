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
    
    def eliminate_biconditionals(self, parts):
        result = []
        i = 0
        while i < len(parts):
            if parts[i] == '<=>':
                # Get the full left expression
                left_end = i - 1
                if parts[left_end] == ')':
                    left_start = self.__find_matching_parenthesis(parts, left_end)
                else:
                    left_start = left_end
                left = parts[left_start:left_end + 1]

                # Get the full right expression
                right_start = i + 1
                if parts[right_start] == '(':
                    right_end = self.__find_matching_parenthesis(parts, right_start)
                else:
                    right_end = right_start
                right = parts[right_start:right_end + 1]

                # Transform the biconditional
                transformed = ['('] + left + ['=>'] + right + [')', '&', '('] + right + ['=>'] + left + [')']
                result = result[:left_start] + transformed  # Replace left part with the transformation
                i = right_end  # Move index to the end of the right expression
            else:
                result.append(parts[i])
            i += 1
        return result
    
    def eliminate_implications(self, parts):
        result = []
        i = 0
        while i < len(parts):
            if parts[i] == '=>':
                left_end = i - 1
                if parts[left_end] == ')':
                    left_start = self.__find_matching_parenthesis(parts, left_end, direction="backward")
                else:
                    left_start = left_end
                left = parts[left_start:left_end + 1]

                right_start = i + 1
                if parts[right_start] == '(':
                    right_end = self.__find_matching_parenthesis(parts, right_start)
                else:
                    right_end = right_start
                right = parts[right_start:right_end + 1]

                # Apply negation to the entire left expression
                if left_start != left_end:
                    negated_left = ['~'] + left
                else:
                    negated_left = ['~', '('] + left + [')']

                result = result[:left_start] + negated_left + ['||'] + right
                i = right_end  # Skip over the right expression
            else:
                result.append(parts[i])
            i += 1
        return result


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
            print(f"Before distributing disjunctions: {parts}")
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
    
    def move_negations_inward(self, parts):
        print("move_negations_inward entered with parts:", parts)
        result = []
        i = 0
        while i < len(parts):
            if parts[i] == '~':
                if i + 1 < len(parts) and parts[i + 1] == '(':
                    # Find the matching parenthesis
                    left_index = i + 1
                    right_index = self.__find_matching_parenthesis(parts, left_index)
                    inner_parts = parts[left_index + 1:right_index]                    
                    # Apply De Morgan's Law to the inner parts
                    inner_result = []
                    j = 0
                    while j < len(inner_parts):
                        if inner_parts[j] == '||':
                            inner_result.append('&')
                        elif inner_parts[j] == '&':
                            inner_result.append('||')
                        else:
                            if inner_parts[j].startswith('~'):
                                inner_result.append(inner_parts[j][1:])
                            else:
                                inner_result.append('~' + inner_parts[j])
                        j += 1
                    
                    result.extend(inner_result)
                    i = right_index
                else:
                    # Handle simple negation
                    if parts[i + 1].startswith('~'):
                        result.append(parts[i + 1][1:])
                        i += 1
                    else:
                        result.append('~' + parts[i + 1])
                        i += 1
            else:
                result.append(parts[i])
            i += 1
        print("move_negations_inward result:", result)
        return result
    
    def distribute_disjunctions(self, parts):
        print("~~~~~~distribute_disjunctions entered with parts:", parts)
        
        def distribute(a, b):
            print(f"Distribute called with a: {a}, b: {b}")
            if isinstance(a, list) and '&' in a:
                index = a.index('&')
                left_a = a[:index]
                right_a = a[index + 1:]
                print(f"AND detected in a. Left: {left_a}, Right: {right_a}")
                result = ['&'] + [distribute(left_a + [right_a_part], b) for right_a_part in right_a]
                print(f"Result after distributing over a: {result}")
                return result
            if isinstance(b, list) and '&' in b:
                index = b.index('&')
                left_b = b[:index]
                right_b = b[index + 1:]
                print(f"AND detected in b. Left: {left_b}, Right: {right_b}")
                result = ['&'] + [distribute(a, left_b + [right_b_part]) for right_b_part in right_b]
                print(f"Result after distributing over b: {result}")
                return result
            result = a+['||']+ b
            print(f"Distribute result: {result}")
            return result

        def split_and_clauses(expression):
            print(f"split_and_clauses called with expression: {expression}")
            if isinstance(expression, list) and '&' in expression:
                clauses = []
                current_clause = []
                for token in expression:
                    if token == '&':
                        if current_clause:
                            clauses.extend(current_clause)
                        current_clause = []
                    else:
                        current_clause.extend(token)
                if (current_clause):
                    clauses.append(current_clause)
                print(f"Clauses after splitting: {clauses}")
                return clauses
            return [expression]

        def distribute_all(parts):
            print(f"distribute_all called with parts: {parts}")
            if '||' in parts:
                index = parts.index('||')
                left = parts[:index]
                right = parts[index + 1:]
                print(f"'||' detected. Left: {left}, Right: {right}")
                if '&' in left or '&' in right:
                    distributed = distribute(left, right)
                    if '&' in distributed:
                        result = split_and_clauses(distributed)
                        print(f"Result after splitting clauses: {result}")
                        return result
                    print(f"Distributed without splitting: {distributed}")
                    return [distributed]
                else:
                    return [parts]
            return [parts]

        while True:
            new_parts = []
            for clause in parts:
                if '||' in clause:
                    new_parts.extend(distribute_all(parts))
                else:
                    new_parts.append(clause)
            if new_parts == parts:
                break
            parts = new_parts

        print(f"~~~~~~Final distributed parts: {new_parts}")
        return new_parts


    def simplify_expression(self, parts):
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

        def handle_conjunctions(parts):
            parts = [part for part in parts if part != '(' and part != ')']
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
    
if __name__ == "__main__":
    # Example usage:
    sentence = Sentence("(c => d) => a")
    cnf = sentence.to_cnf_atomic()
    print(f"Original expression: (c => d) => a")
    print(f"CNF expression: {' '.join(cnf)}")
