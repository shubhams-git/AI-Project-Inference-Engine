import re

class ResolutionProver:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def resolve(self, clause1, clause2):
        resolved_clauses = []
        literals1 = self.get_literals(clause1)
        literals2 = self.get_literals(clause2)
        for lit1 in literals1:
            for lit2 in literals2:
                if lit1 == self.negate_literal(lit2):
                    resolvent = [l for l in literals1 if l != lit1] + [l for l in literals2 if l != lit2]
                    resolvent = list(set(resolvent))  # Remove duplicates
                    if not self.is_tautology(resolvent):
                        resolved_clauses.append(resolvent)
        return resolved_clauses

    def get_literals(self, clause):
        return re.findall(r'~?\w+', clause)

    def negate_literal(self, literal):
        return literal[1:] if literal.startswith('~') else '~' + literal

    def is_tautology(self, clause):
        literals = set(clause)
        for literal in literals:
            if self.negate_literal(literal) in literals:
                return True
        return False

    def prove(self, query):
        negated_query = self.negate_literal(query)
        self.kb.tell('(' + negated_query + ')')
        clauses = self.kb.get_clauses()

        new_clauses = []
        while True:
            n = len(clauses)
            pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
            for (clause1, clause2) in pairs:
                resolvents = self.resolve(clause1, clause2)
                for resolvent in resolvents:
                    if resolvent == []:  # Empty clause means contradiction
                        return True
                    if resolvent not in new_clauses:
                        new_clauses.append(resolvent)
            if all(new_clause in clauses for new_clause in new_clauses):
                return False
            for new_clause in new_clauses:
                if new_clause not in clauses:
                    clauses.append(new_clause)

        return False
