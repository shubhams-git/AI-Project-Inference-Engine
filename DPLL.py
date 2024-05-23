from Sentence import Sentence
from sympy.logic.boolalg import to_cnf, Not, And, Or
import sympy

class DPLL:
    def __init__(self, knowledge_base, query, debug=False):
        """Initialize the DPLL solver with a knowledge base, a query, and an optional debug mode."""
        self.kb = knowledge_base
        self.query = query
        self.debug = debug

    def debug_print(self, *args, **kwargs):
        """Print debug messages if debugging is enabled."""
        if self.debug:
            print(*args, **kwargs)
    
    def solve(self):
        """Solve the query using the DPLL algorithm."""
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
        """Parse the knowledge base and convert it to a list of clauses in CNF."""
        clauses = []
        for sentence in self.kb.sentences:
            cnf = to_cnf(sentence.to_sympy_expr(sentence.root[0]))
            clauses.extend(self.extract_clauses(cnf))
        return clauses

    def extract_clauses(self, cnf_expr):
        """Extract clauses from a CNF expression."""
        if isinstance(cnf_expr, sympy.Or):
            return [cnf_expr]
        elif isinstance(cnf_expr, sympy.And):
            return list(cnf_expr.args)
        else:
            return [cnf_expr]

    def negate_query(self):
        """Negate the query and convert it to CNF."""
        query_expr = self.query.to_sympy_expr(self.query.root[0])
        query_cnf = to_cnf(Not(query_expr))
        return self.extract_clauses(query_cnf)

    def dpll(self, clauses, symbols, model):
        """Apply the DPLL algorithm to determine satisfiability."""
        self.debug_print("\nCurrent model:", model)
        self.debug_print("Remaining clauses:")
        for clause in clauses:
            self.debug_print(f"  {clause}")
        self.debug_print("Remaining symbols:", symbols)

        # Base case: check if all clauses are satisfied
        all_satisfied = all(self.evaluate(clause, model) is True for clause in clauses)
        self.debug_print(f"All clauses satisfied check: {all_satisfied}")
        if all_satisfied:
            self.debug_print("All clauses satisfied with current model.")
            return True
        
        # Base case: check if any clause is unsatisfied
        unsat_clauses = [clause for clause in clauses if self.evaluate(clause, model) is False]
        if unsat_clauses:
            self.debug_print(f"Unsatisfied clauses: {unsat_clauses}")
            return False

        # Perform unit propagation
        self.debug_print("\nPerforming unit propagation...")
        unit_clauses = self.find_unit_clauses(clauses)
        self.debug_print(f"Initial unit clauses: {unit_clauses}")
        while unit_clauses:
            unit = unit_clauses.pop()
            literal = unit if isinstance(unit, sympy.Symbol) else next(iter(unit.args))
            if isinstance(literal, Not):
                literal = literal.args[0]

            self.debug_print(f"  Unit clause found: {unit}. Propagating {literal}.")
            model[literal] = True
            clauses = self.simplify(clauses, literal)
            self.debug_print(f"  Updated model: {model}")
            self.debug_print("  Simplified clauses:")
            for clause in clauses:
                self.debug_print(f"    {clause}")

            # Reevaluate after simplification
            all_satisfied = all(self.evaluate(clause, model) is True for clause in clauses)
            self.debug_print(f"All clauses satisfied check after propagation: {all_satisfied}")
            if all_satisfied:
                self.debug_print("All clauses satisfied with current model after propagation.")
                return True
            unsat_clauses = [clause for clause in clauses if self.evaluate(clause, model) is False]
            if unsat_clauses:
                self.debug_print(f"Unsatisfied clauses after propagation: {unsat_clauses}")
                return False

            unit_clauses = self.find_unit_clauses(clauses)
            self.debug_print(f"New unit clauses after propagation: {unit_clauses}")

        if not symbols:
            self.debug_print("No symbols left to process. Returning False.")
            return False

        # Choose a literal and recurse
        P = next(iter(symbols))
        rest = symbols - {P}
        new_model = model.copy()

        self.debug_print(f"\nTrying {P} as True")
        new_model[P] = True
        if self.dpll(clauses, rest, new_model):
            return True

        self.debug_print(f"\nTrying {P} as False")
        new_model = model.copy()
        new_model[P] = False
        return self.dpll(clauses, rest, new_model)

    def find_unit_clauses(self, clauses):
        """Identify unit clauses from the list of clauses."""
        unit_clauses = []
        self.debug_print("\nFinding unit clauses...")
        for clause in clauses:
            if isinstance(clause, sympy.Symbol):
                unit_clauses.append(clause)
            elif isinstance(clause, sympy.Or) and len(clause.args) == 1:
                unit_clauses.append(clause)
            elif isinstance(clause, Not):
                unit_clauses.append(clause)
        self.debug_print(f"All unit clauses found: {unit_clauses}")
        return unit_clauses

    def simplify(self, clauses, literal):
        """Simplify the clause set given a literal assignment."""
        new_clauses = []
        self.debug_print(f"Simplifying clauses with {literal} set to True")
        for clause in clauses:
            if isinstance(clause, sympy.Symbol):
                clause_literals = {clause}
            elif isinstance(clause, sympy.Or):
                clause_literals = set(clause.args)
            else:
                clause_literals = {clause}

            if literal in clause_literals:
                continue

            new_clause_literals = clause_literals - {Not(literal)}
            if new_clause_literals:
                if len(new_clause_literals) == 1:
                    new_clause = new_clause_literals.pop()
                else:
                    new_clause = Or(*new_clause_literals)
                new_clauses.append(new_clause)
            else:
                self.debug_print(f"  Clause {clause} is empty after removing {Not(literal)}.")
        return new_clauses

    def evaluate(self, clause, model):
        """Evaluate a clause under the current model."""
        if isinstance(clause, sympy.Symbol):
            return model.get(clause, None)
        if isinstance(clause, Not):
            return not self.evaluate(clause.args[0], model)
        if isinstance(clause, Or):
            results = [self.evaluate(arg, model) for arg in clause.args]
            if any(result is True for result in results):
                return True
            elif all(result is False for result in results):
                return False
            else:
                return None
        if isinstance(clause, And):
            results = [self.evaluate(arg, model) for arg in clause.args]
            if all(result is True for result in results):
                return True
            elif any(result is False for result in results):
                return False
            else:
                return None
        return None

# Example usage
if __name__ == "__main__":
    import sys
    debug_mode = True  # Ensure debug mode is enabled
    from KnowledgeBase import KnowledgeBase

    # Example usage
    tell = ["a", "a => b", "b => c", "b&c=>d", "d=>e"]
    ask = "e"
    kb = KnowledgeBase(tell, 'GS')
    query = Sentence(ask)
    dpll = DPLL(kb, query, debug=debug_mode)
    print("Example 1: YES" if dpll.solve() else "Example 1: NO")
