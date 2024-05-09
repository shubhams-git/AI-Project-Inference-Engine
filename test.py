import unittest
from Sentence import Sentence 

class TestSentenceModule(unittest.TestCase):

    def test_negation(self):
        sentence = Sentence("~p")
        model = {'p': False}
        result = sentence.solve(model)
        self.assertTrue(result)

    def test_complex_expression(self):
        sentence = Sentence("~p & (q => r) || (s <=> ~t)")
        model = {'p': False, 'q': True, 'r': True, 's': False, 't': True}
        result = sentence.solve(model)
        self.assertTrue(result)

    def test_parentheses_handling(self):
        sentence = Sentence("p & (q || (r => s))")
        model = {'p': True, 'q': False, 'r': False, 's': True}
        result = sentence.solve(model)
        self.assertTrue(result)

    def test_biconditional(self):
        sentence = Sentence("p <=> q")
        model = {'p': True, 'q': True}
        result = sentence.solve(model)
        sentence.display()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
