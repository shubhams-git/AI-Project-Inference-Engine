from Sentence import Sentence

def test_sentence(expression, model):
    try:
        sentence = Sentence(expression)
        print("Parsed expression:", sentence.root)
        print("Atomic sentences:", sentence.atomic)
    except Exception as e:
        print(f"Error testing expression '{expression}': {str(e)}")

def test_cnf_conversion(expression):
    try:
        sentence = Sentence(expression)
        print("\nConverting to CNF...")
        cnf_expression = sentence.to_cnf_atomic()
        print("Original expression:", expression)
        print("CNF expression:", " ".join(cnf_expression))
    except Exception as e:
        print(f"Error converting expression '{expression}' to CNF: {str(e)}")

if __name__ == "__main__":
    expression = "(a => (c => ~d)) & b & (b => a)"
    model = {'a': True, 'b': True, 'c': True, 'd': True}
    
    print(f"Testing expression: {expression}")
    test_sentence(expression, model)
    print("-" * 40)

    # Test CNF conversion
    print("\nTesting CNF Conversion")
    test_cnf_conversion(expression)
    print("-" * 40)
