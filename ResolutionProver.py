from Sentence import Sentence
from KnowledgeBase import KnowledgeBase
import sympy
from sympy.logic.boolalg import to_cnf, Not, Or

class ResolutionProver:
    def __init__(self, kb, query):
        self.kb = kb
        self.query = query

    def parse_kb(self):
        clauses = []
        for sentence in self.kb.sentences:
            cnf = sentence.to_cnf_atomic()
            clauses.extend(self.extract_clauses(cnf))
        return clauses

    def extract_clauses(self, cnf_expr):
        if isinstance(cnf_expr, sympy.Or):
            return [cnf_expr]
        elif isinstance(cnf_expr, sympy.And):
            return list(cnf_expr.args)
        else:
            return [cnf_expr]

    def negate_query(self):
        query_cnf = to_cnf(Not(self.query.to_cnf_atomic()))
        return self.extract_clauses(query_cnf)

    def resolve(self, clause1, clause2):
        resolvents = []
        clause1 = set(clause1.args) if isinstance(clause1, sympy.Or) else {clause1}
        clause2 = set(clause2.args) if isinstance(clause2, sympy.Or) else {clause2}
        
        for literal in clause1:
            complement = Not(literal)
            if complement in clause2:
                resolvent = (clause1 - {literal}) | (clause2 - {complement})
                if len(resolvent) == 0:
                    print(f"Resolved to empty clause: {clause1} and {clause2}")
                    return True, []
                resolvents.append(Or(*resolvent) if len(resolvent) > 1 else next(iter(resolvent)))
        return False, resolvents

    def solve(self):
        clauses = self.parse_kb()
        clauses.extend(self.negate_query())
        
        print("Initial clauses:")
        for clause in clauses:
            print(clause)
        
        new = set()
        while True:
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
            found_new_resolvents = False
            for (clause1, clause2) in pairs:
                is_resolved, resolvents = self.resolve(clause1, clause2)
                if is_resolved:
                    print("The query is proven.")
                    return True
                if resolvents:
                    found_new_resolvents = True
                    new.update(resolvents)
                    print(f"New resolvent from {clause1} and {clause2}: {resolvents}")
            if not found_new_resolvents:
                print("No new clauses were generated. The query is not proven.")
                return False
            clauses.extend(new)
            new.clear()

# Example usage
if __name__ == "__main__":
    kb = KnowledgeBase(["p2=>p3", "p3=>p1", "c=>e", "b&e=>f", "f&g=>h", "p2&p1&p3=>d", "p1&p3=>c", "a", "b", "p2"], 'GS')
    query = Sentence("d")
    rp = ResolutionProver(kb, query)
    print("YES" if rp.solve() else "NO")

