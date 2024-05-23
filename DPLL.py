from Sentence import Sentence
from sympy.logic.boolalg import to_cnf, Not, And, Or
import sympy

class DPLL:
    def __init__(self, knowledge_base, query, debug=False):
        self.kb = knowledge_base
        self.query = query
        self.debug = debug

    def debug_print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def solve(self):
        self.debug_print("Starting DPLL algorithm...")
        clauses = self.parse_kb()
        self.debug_print("Initial clauses from knowledge base:")
        for clause in clauses:
            self.debug_print(f"  {clause}")

        negated_query_clauses = self.negate_query()
        self.debug_print("\nNegated query clauses:")
        for clause in negated_query_clauses:
            self.debug_print(f"  {clause}")

        clauses.extend(negated_query_clauses)
        symbols = set()
        for clause in clauses:
            symbols.update(clause.free_symbols)

        self.debug_print("\nSymbols in the clauses:", symbols)
        result = self.dpll(clauses, symbols, {})
        self.debug_print("\nDPLL result:", "SATISFIABLE" if result else "UNSATISFIABLE")
        return result

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

    def dpll(self, clauses, symbols, model):
        self.debug_print("\nCurrent model:", model)
        self.debug_print("Remaining clauses:")
        for clause in clauses:
            self.debug_print(f"  {clause}")
        self.debug_print("Remaining symbols:", symbols)

        # Base case: all clauses are satisfied
        if all(self.evaluate(clause, model) for clause in clauses):
            self.debug_print("All clauses satisfied with current model.")
            return True
        # Base case: any clause is unsatisfied
        if any(self.evaluate(clause, model) is False for clause in clauses):
            self.debug_print("Some clauses are unsatisfied with current model.")
            return False

        # Perform unit propagation
        unit_clauses = [clause for clause in clauses if len(clause.args) == 1]
        while unit_clauses:
            unit = unit_clauses.pop()
            literal = list(unit.args)[0]
            self.debug_print(f"Performing unit propagation on {literal}")
            model[literal] = True
            clauses = self.simplify(clauses, literal)
            if all(self.evaluate(clause, model) for clause in clauses):
                return True
            if any(self.evaluate(clause, model) is False for clause in clauses):
                return False
            unit_clauses = [clause for clause in clauses if len(clause.args) == 1]

        if not symbols:
            return False

        # Choose a literal and recurse
        P = symbols.pop()
        rest = symbols.copy()
        new_model = model.copy()

        self.debug_print(f"Trying {P} as True")
        new_model[P] = True
        if self.dpll(clauses, rest, new_model):
            return True

        self.debug_print(f"Trying {P} as False")
        new_model[P] = False
        return self.dpll(clauses, rest, new_model)

    def simplify(self, clauses, literal):
        new_clauses = []
        for clause in clauses:
            if literal in clause.args:
                continue
            new_clause = [l for l in clause.args if l != ~literal]
            if new_clause:
                new_clauses.append(Or(*new_clause))
        return new_clauses

    def evaluate(self, clause, model):
        if isinstance(clause, sympy.Symbol):
            return model.get(clause, None)
        if isinstance(clause, Not):
            result = not self.evaluate(clause.args[0], model)
            self.debug_print(f"Evaluating NOT {clause.args[0]}: {result}")
            return result
        if isinstance(clause, Or):
            result = any(self.evaluate(arg, model) for arg in clause.args)
            self.debug_print(f"Evaluating OR {clause.args}: {result}")
            return result
        if isinstance(clause, And):
            result = all(self.evaluate(arg, model) for arg in clause.args)
            self.debug_print(f"Evaluating AND {clause.args}: {result}")
            return result
        return None

# Example usage
if __name__ == "__main__":
    import sys
    debug_mode = "-d" in sys.argv
    from KnowledgeBase import KnowledgeBase

    # Example 1: Original example
    tell = ["a", "a => b", "b => c"]
    ask = "c"
    kb = KnowledgeBase(tell, 'GS')
    query = Sentence(ask)
    dpll = DPLL(kb, query, debug=debug_mode)
    print("Example 1: YES" if dpll.solve() else "Example 1: NO")

    # Example 2: Simple unsatisfiable case
    tell = ["a", "b", "c", "~a || ~b || ~c"]
    ask = "d"
    kb = KnowledgeBase(tell, 'GS')
    query = Sentence(ask)
    dpll = DPLL(kb, query, debug=debug_mode)
    print("Example 2: YES" if dpll.solve() else "Example 2: NO")

    # Example 3: Another satisfiable case
    tell = ["a => b", "b => c", "a"]
    ask = "c"
    kb = KnowledgeBase(tell, 'GS')
    query = Sentence(ask)
    dpll = DPLL(kb, query, debug=debug_mode)
    print("Example 3: YES" if dpll.solve() else "Example 3: NO")

    # Example 4: Case with multiple implications
    tell = ["a => b", "b => c", "c => d", "d => e", "a"]
    ask = "e"
    kb = KnowledgeBase(tell, 'GS')
    query = Sentence(ask)
    dpll = DPLL(kb, query, debug=debug_mode)
    print("Example 4: YES" if dpll.solve() else "Example 4: NO")

    # Example 5: Case with contradictory clauses
    tell = ["p2=> p3", "p3 => p1", "c => e", "b&e => f", "f&g => h", "p2&p1&p3 => ~d", "p1&p3 => c", "a", "b", "p2"]
    ask = "~d"
    kb = KnowledgeBase(tell, 'GS')
    query = Sentence(ask)
    dpll = DPLL(kb, query, debug=debug_mode)
    print("Example 5: YES" if dpll.solve() else "Example 5: NO")