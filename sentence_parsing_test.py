from Sentence import Sentence

def test_sentence(expression, model):
    try:
        sentence = Sentence(expression)
        # result = sentence.solve(model)
        # print(f"Expression: {expression}, Model: {model}, Result: {result}")
    except Exception as e:
        print(f"Error testing expression '{expression}': {str(e)}")

if __name__ == "__main__":
    # Test various expressions
    expressions = [
        # ("p & q => r", {'p': True, 'q': True, 'r': False}),    # Test implication
        # ("p & ~q", {'p': True, 'q': False}),                  # Test conjunction with negation
        # ("p || q", {'p': False, 'q': True}),                  # Test disjunction
        # ("p <=> q", {'p': True, 'q': True}),                  # Test biconditional (true scenario)
        # ("p <=> q", {'p': False, 'q': True}),                 # Test biconditional (false scenario)
        # ("~p || q", {'p': True, 'q': True}),                  # Test negation with disjunction
        # ("(p & q) => (r || s)", {'p': True, 'q': True, 'r': False, 's': True}),  # Nested operators
        ("~d & (~g => ~f)", {'a': True, 'b': True, 'c': True, 'd': True}),     # Complex implication
    ]

    for expression, model in expressions:
        test_sentence(expression, model)
