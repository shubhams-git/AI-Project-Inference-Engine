from Sentence import Sentence

def test_sentence(expression):
    try:
        sentence = Sentence(expression)
        print("Parsed expression:", sentence.root)
        print("Atomic sentences:", sentence.atomic)
    except Exception as e:
        print(f"Error testing expression '{expression}': {str(e)}")

def test_cnf_conversion(expression):
    try:
        sentence = Sentence(expression)
    except Exception as e:
        print(f"Error converting expression '{expression}' to CNF: {str(e)}")

if __name__ == "__main__":
    expression = "((a&b=>c)&(b=>c)) & (b=>a) & c"    
    print(f"Testing expression: {expression}")
    test_sentence(expression)
    print("-" * 40)
