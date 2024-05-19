from sympy import symbols, Not, And, Or, Implies, Equivalent, to_cnf

# Define the variables
a, b, c, d = symbols('a b c d')

# Define the expression
expr = Equivalent(a, Implies(c, Not(d)))

# Convert to CNF
cnf_expr = to_cnf(expr, simplify=True)

# Print the CNF expression
print(cnf_expr)
