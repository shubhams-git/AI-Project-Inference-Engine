from Sentence import Sentence

def test_sentence(expression, model):
    try:
        sentence = Sentence(expression)
        print("Parsed expression:", sentence.root)
        print("Atomic sentences:", sentence.atomic)
        result = sentence.solve(model)
        print("Result with model", model, ":", result)
    except Exception as e:
        print(f"Error testing expression '{expression}': {str(e)}")

if __name__ == "__main__":
    # Test various expressions
    expressions = [
        ("~d & (~g <=> ~f)", {'a': True, 'b': True, 'c': True, 'd': True, 'g': False, 'f': True}),
        ("a & b => c", {'a': True, 'b': True, 'c': False}),
        ("a || ~b", {'a': False, 'b': True}),
        ("(a <=> b) & (b => c)", {'a': True, 'b': True, 'c': False}),
    ]

    for expression, model in expressions:
        print(f"Testing expression: {expression}")
        test_sentence(expression, model)
        print("-" * 40)
