class CNFConverter:
    @staticmethod
    def convert_to_cnf(sentence):
        sentence = CNFConverter.eliminate_biconditionals_and_implications(sentence)
        sentence = CNFConverter.move_negations_inward(sentence)
        sentence = CNFConverter.distribute_disjunctions_over_conjunctions(sentence)
        return sentence

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
            while '&' in parts:
                i = parts.index('&')
                left = parts[:i]
                right = parts[i + 1:]
                parts = CNFConverter.distribute(left, right)
            return parts

        parts = CNFConverter.flatten(sentence.root)
        sentence.root = distribute(parts)
        return sentence

    @staticmethod
    def apply_de_morgans(parts):
        result = []
        if parts[0] == '~' and parts[1] == '(':
            if parts[3] == '&':
                result.append('(')
                result.append('~')
                result.append(parts[2])
                result.append('||')
                result.append('~')
                result.append(parts[4])
                result.append(')')
            elif parts[3] == '||':
                result.append('(')
                result.append('~')
                result.append(parts[2])
                result.append('&')
                result.append('~')
                result.append(parts[4])
                result.append(')')
        elif parts[0] == '~':
            result.append(parts[0])
            result.append(parts[1])
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
    def distribute(left, right):
        if '&' in right:
            right_index = right.index('&')
            return ['(', *CNFConverter.distribute(left, right[:right_index]), '&', *CNFConverter.distribute(left, right[right_index + 1:]), ')']
        elif '&' in left:
            left_index = left.index('&')
            return ['(', *CNFConverter.distribute(left[:left_index], right), '&', *CNFConverter.distribute(left[left_index + 1:], right), ')']
        else:
            return ['(', *left, '||', *right, ')']
