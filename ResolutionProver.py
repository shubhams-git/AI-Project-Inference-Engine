from Sentence import Sentence
from KnowledgeBase import KnowledgeBase
import sympy
from sympy.logic.boolalg import to_cnf, Not, Or

class ResolutionProver:
    def __init__(self, kb, query):
        """
        Initialize the ResolutionProver with a knowledge base and a query.
        
        :param kb: The knowledge base consisting of propositional logic sentences.
        :param query: The query sentence to be resolved.
        """
        self.kb = kb
        self.query = query
        self.step = 0

    def parse_kb(self):
        """
        Parse the knowledge base into a list of CNF clauses.
        
        :return: A list of CNF clauses derived from the knowledge base sentences.
        """
        clauses = []
        for sentence in self.kb.sentences:
            cnf = sentence.to_cnf_atomic()
            clauses.extend(self.extract_clauses(cnf))
        return clauses

    def extract_clauses(self, cnf_expr):
        """
        Extract individual clauses from a CNF expression.
        
        :param cnf_expr: The CNF expression.
        :return: A list of clauses (each clause is an instance of sympy.Or or a literal).
        """
        if isinstance(cnf_expr, sympy.Or):
            return [cnf_expr]
        elif isinstance(cnf_expr, sympy.And):
            return list(cnf_expr.args)
        else:
            return [cnf_expr]

    def negate_query(self):
        """
        Negate the query and convert it into CNF.
        
        :return: A list of CNF clauses derived from the negated query.
        """
        query_cnf = to_cnf(Not(self.query.to_cnf_atomic()))
        return self.extract_clauses(query_cnf)

    def resolve(self, clause1, clause2):
        """
        Resolve two clauses to find their resolvents.
        
        :param clause1: The first clause (a set of literals).
        :param clause2: The second clause (a set of literals).
        :return: A tuple (is_resolved, resolvents) where is_resolved is True if a contradiction is found,
                 and resolvents is a list of resolvent clauses.
        """
        resolvents = []
        clause1 = set(clause1.args) if isinstance(clause1, sympy.Or) else {clause1}
        clause2 = set(clause2.args) if isinstance(clause2, sympy.Or) else {clause2}
        
        for literal in clause1:
            complement = Not(literal)
            if complement in clause2:
                resolvent = (clause1 - {literal}) | (clause2 - {complement})
                self.step += 1
                if len(resolvent) == 0:
                    print(f"{self.step}. Resolve {clause1} with {clause2} -> Contradiction: ∅")
                    return True, []
                else:
                    resolvent_expr = Or(*resolvent) if len(resolvent) > 1 else next(iter(resolvent))
                    print(f"{self.step}. Resolve {clause1} with {clause2} -> Resolvent: {resolvent_expr}")
                    resolvents.append(resolvent_expr)
        return False, resolvents

    def solve(self):
        """
        Attempt to resolve the query using the resolution method.
        
        :return: True if the query is entailed by the knowledge base, False otherwise.
        """
        clauses = self.parse_kb()
        negated_query_clauses = self.negate_query()
        clauses.extend(negated_query_clauses)
        
        print("Initial clauses in CNF:")
        for clause in clauses:
            print(clause)
        
        new = set(negated_query_clauses)
        while new:
            found_new_resolvents = False
            clause1 = new.pop()
            for clause2 in clauses:
                if clause1 == clause2:
                    continue
                is_resolved, resolvents = self.resolve(clause1, clause2)
                if is_resolved:
                    print(f"Since we have derived a contradiction (∅), the query {self.query.original} is entailed by the KB.")
                    return True
                if resolvents:
                    found_new_resolvents = True
                    new.update(resolvents)
            if not found_new_resolvents:
                print("No new clauses were generated. The query is not proven.")
                return False
            clauses.append(clause1)
            new.update(negated_query_clauses)

# Example usage
if __name__ == "__main__":
    kb = KnowledgeBase(["p2=>p3", "p3=>p1", "c=>e", "b&e=>f", "f&g=>h", "p2&p1&p3=>d", "p1&p3=>c", "a", "b", "p2"], 'GS')
    query = Sentence("d")
    rp = ResolutionProver(kb, query)
    print("YES" if rp.solve() else "NO")
