class CNFConverter:
    @staticmethod
    def convert_to_cnf(sentence):
        sentence = CNFConverter.eliminate_biconditionals_and_implications(sentence)
        sentence = CNFConverter.move_negations_inward(sentence)
        sentence = CNFConverter.distribute_disjunctions_over_conjunctions(sentence)
        cnf_clauses = CNFConverter.flatten_to_clauses(sentence.root)
        print(f"CNF Clauses: {cnf_clauses}")
        return cnf_clauses

    @staticmethod
    def eliminate_biconditionals_and_implications(sentence):
        def replace_biconditionals_and_implications(parts):
            result = []
            i = 0
            while i < len(parts):
                if parts[i] == '<=>':
                    a = result.pop()
                    b = parts[i + 1]
                    result.append(['(', a, '=>', b, ')', '&', '(', b, '=>', a, ')'])
                    i += 1
                elif parts[i] == '=>':
                    a = result.pop()
                    b = parts[i + 1]
                    result.append(['(', '~', a, '||', b, ')'])
                    i += 1
                else:
                    result.append(parts[i])
                i += 1
            return result

        parts = CNFConverter.flatten(sentence.root)
        sentence.root = replace_biconditionals_and_implications(parts)
        return sentence

    @staticmethod
    def move_negations_inward(sentence):
        def move_negations(parts):
            result = []
            i = 0
            while i < len(parts):
                if parts[i] == '~':
                    if parts[i + 1] == '(':
                        result.extend(CNFConverter.apply_de_morgans(parts[i:i + 4]))
                        i += 3
                    else:
                        result.extend(CNFConverter.apply_de_morgans(parts[i:i + 2]))
                        i += 1
                else:
                    result.append(parts[i])
                i += 1
            return result

        parts = CNFConverter.flatten(sentence.root)
        sentence.root = move_negations(parts)
        return sentence

    @staticmethod
    def distribute_disjunctions_over_conjunctions(sentence):
        def distribute(parts):
            i = 0
            while i < len(parts):
                if parts[i] == '||' and isinstance(parts[i-1], list) and isinstance(parts[i+1], list):
                    left = parts[i-1]
                    right = parts[i+1]
                    parts = parts[:i-1] + CNFConverter.distribute_lists(left, right) + parts[i+2:]
                    i = 0  # restart as we have modified the list
                else:
                    i += 1
            return parts

        parts = CNFConverter.flatten(sentence.root)
        sentence.root = distribute(parts)
        return sentence

    @staticmethod
    def distribute_lists(left, right):
        distributed = []
        for l in left:
            for r in right:
                distributed.append(['(', l, '||', r, ')'])
        return distributed

    @staticmethod
    def apply_de_morgans(parts):
        result = []
        if parts[0] == '~' and parts[1] == '(':
            if parts[3] == '&':
                result.append('(')
                result.append('~' + parts[2])
                result.append('||')
                result.append('~' + parts[4])
                result.append(')')
            elif parts[3] == '||':
                result.append('(')
                result.append('~' + parts[2])
                result.append('&')
                result.append('~' + parts[4])
                result.append(')')
        elif parts[0] == '~':
            result.append(parts[0] + parts[1])
        return result

    @staticmethod
    def flatten(parts):
        result = []
        for part in parts:
            if isinstance(part, list):
                result.extend(CNFConverter.flatten(part))
            else:
                result.append(part)
        return result

    @staticmethod
    def flatten_to_clauses(parts):
        clauses = []
        current_clause = []
        for part in parts:
            if part == '&':
                clauses.append(current_clause)
                current_clause = []
            elif part != '(' and part != ')':
                current_clause.append(part)
        if current_clause:
            clauses.append(current_clause)
        return clauses

    @staticmethod
    def expand_atomic(sentence, atomic_sentences):
        def expand(parts):
            expanded = []
            for part in parts:
                if part in atomic_sentences:
                    expanded.extend(expand(atomic_sentences[part]))
                else:
                    expanded.append(part)
            return expanded

        sentence.root = expand(sentence.root)
        return sentence
