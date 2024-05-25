from Sentence import Sentence
from KnowledgeBase import KnowledgeBase
import sympy
from sympy.logic.boolalg import to_cnf, Not, Or, And, Implies, Equivalent

class ResolutionProver:
    def __init__(self, kb, query, debug=False):
        """
        Initialize the ResolutionProver with a knowledge base and a query.

        Args:
            kb (KnowledgeBase): The knowledge base consisting of propositional logic sentences.
            query (Sentence): The query sentence to be resolved.
            debug (bool): Flag to enable debug mode for detailed steps.
        """
        self.kb = kb
        self.query = query
        self.debug = debug
        self.step = 0

    def parse_kb(self):
        """
        Parse the knowledge base into a list of CNF clauses.

        Returns:
            list: A list of CNF clauses derived from the knowledge base sentences.
        """
        clauses = []
        for sentence in self.kb.sentences:
            original_expr = sentence.to_sympy_expr(sentence.root[0])
            if not self.is_cnf(original_expr):
                cnf_expr = to_cnf(original_expr, simplify=True)
            else:
                cnf_expr = original_expr

            clauses.extend(self.extract_clauses(cnf_expr))
        return clauses

    def extract_clauses(self, cnf_expr):
        """
        Extract individual clauses from a CNF expression.

        Args:
            cnf_expr (sympy.Expr): The CNF expression.

        Returns:
            list: A list of clauses (each clause is an instance of sympy.Or or a literal).
        """
        if isinstance(cnf_expr, sympy.And):
            clauses = []
            for arg in cnf_expr.args:
                clauses.extend(self.extract_clauses(arg))
            return clauses
        elif isinstance(cnf_expr, sympy.Or):
            return [cnf_expr]
        elif isinstance(cnf_expr, (Implies, Equivalent)):
            return self.extract_clauses(to_cnf(cnf_expr, simplify=True))
        else:
            return [cnf_expr]

    def negate_query(self):
        """
        Negate the query and convert it into CNF.

        Returns:
            list: A list of CNF clauses derived from the negated query.
        """
        query_expr = self.query.to_sympy_expr(self.query.root[0])
        if not self.is_cnf(query_expr):
            query_cnf = to_cnf(query_expr, simplify=True)
        else:
            query_cnf = query_expr

        negated_query_expr = Not(query_cnf)
        negated_query_cnf = to_cnf(negated_query_expr, simplify=True)

        return self.extract_clauses(negated_query_cnf)

    def resolve(self, clause1, clause2):
        """
        Resolve two clauses to find their resolvents.

        Args:
            clause1 (sympy.Expr): The first clause.
            clause2 (sympy.Expr): The second clause.

        Returns:
            tuple: A tuple (is_resolved, resolvents) where is_resolved is True if a contradiction is found,
                   and resolvents is a list of resolvent clauses.
        """
        resolvents = []
        clause1 = set(clause1.args) if isinstance(clause1, sympy.Or) else {clause1}
        clause2 = set(clause2.args) if isinstance(clause2, sympy.Or) else {clause2}

        for literal in clause1:
            complement = Not(literal)
            if complement in clause2:
                if literal in self.resolved_literals or complement in self.resolved_literals:
                    continue
                resolvent = (clause1 - {literal}) | (clause2 - {complement})
                self.resolved_literals.add(literal)
                self.resolved_literals.add(complement)
                self.step += 1
                if self.debug:
                    if len(resolvent) == 0:
                        print(f"{self.step}. Resolve {clause1} with {clause2} -> Contradiction: ∅")
                    else:
                        resolvent_expr = Or(*resolvent) if len(resolvent) > 1 else next(iter(resolvent))
                        print(f"{self.step}. Resolve {clause1} with {clause2} -> Resolvent: {resolvent_expr}")
                if len(resolvent) == 0:
                    return True, []
                resolvent_expr = Or(*resolvent) if len(resolvent) > 1 else next(iter(resolvent))
                resolvents.append(resolvent_expr)
        return False, resolvents

    def solve(self):
        """
        Attempt to resolve the query using the resolution method.

        Returns:
            bool: True if the query is entailed by the knowledge base, False otherwise.
        """
        clauses = self.parse_kb()
        negated_query_clauses = self.negate_query()
        clauses.extend(negated_query_clauses)

        if self.debug:
            print("-" * 40)
            print("Initial clauses [in CNF]:")
            print("-" * 40)
            for clause in clauses:
                print(clause)
            print("-" * 40)

        new = set(negated_query_clauses)
        processed = set()
        self.resolved_literals = set()

        if self.debug:
            print("Starting the Resolution Process")
            print("-" * 40)

        while new:
            found_new_resolvents = False
            clause1 = new.pop()
            for clause2 in clauses:
                if clause1 == clause2 or clause1 in processed or clause2 in processed:
                    continue
                is_resolved, resolvents = self.resolve(clause1, clause2)
                if is_resolved:
                    if self.debug:
                        print("-" * 40)
                        print(f"Since we have derived a contradiction (∅), the query {self.query.original} is entailed by the KB.")
                        print("-" * 40)
                    return True
                for resolvent in resolvents:
                    if resolvent not in clauses and resolvent not in new:
                        if isinstance(resolvent, sympy.Symbol):
                            all_resolved = resolvent in self.resolved_literals or Not(resolvent) in self.resolved_literals
                        else:
                            all_resolved = all(literal in self.resolved_literals or Not(literal) in self.resolved_literals for literal in resolvent.args)
                        
                        if all_resolved:
                            if self.debug:
                                print("-" * 40)
                                print(f"All literals in the resolvent {resolvent} have already been resolved.")
                                print(f"Since we have derived a contradiction (∅), the query {self.query.original} is entailed by the KB.")
                                print("-" * 40)
                            return True
                        new.add(resolvent)
                        found_new_resolvents = True
            if not found_new_resolvents:
                if self.debug:
                    print("-" * 40)
                    print(f"No new clauses were generated. The query {self.query.original} is not proven.")
                    print("-" * 40)
                return False
            clauses.append(clause1)
            processed.add(clause1)
        return False

    def is_cnf(self, expr):
        """
        Check if a given SymPy expression is in CNF form.

        Args:
            expr (sympy.Expr): The SymPy expression to check.

        Returns:
            bool: True if the expression is in CNF, False otherwise.
        """
        if isinstance(expr, sympy.And):
            return all(self.is_cnf(arg) for arg in expr.args)
        if isinstance(expr, sympy.Or):
            return all(not isinstance(arg, sympy.And) for arg in expr.args)
        return not isinstance(expr, (sympy.And, sympy.Or))

if __name__ == "__main__":
    import sys
    debug_mode = "-d" in sys.argv
    kb = KnowledgeBase(["(a <=> (c => ~d)) & b & (b => a)", "c", "~f || g"], 'GS')
    query = Sentence("~d")
    rp = ResolutionProver(kb, query, debug=debug_mode)
    print("YES" if rp.solve() else "NO")
