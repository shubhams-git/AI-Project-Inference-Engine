import sys
from FileReader import FileReader
from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from TruthTable import TruthTable
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining
from ResolutionProver import ResolutionProver
from DPLL import DPLL

def main():
    """
    Main entry point for the inference engine.
    Reads the input file and determines which inference method to use.
    """
    if len(sys.argv) < 3:
        print("Enter command in the following format: iengine method filename [-d]")
        print("Methods: TT, FC, BC, RP")
        exit(0)

    debug_mode = "-d" in sys.argv
    filename_index = 2

    try:
        tell, ask = FileReader.read(sys.argv[filename_index])
    except FileNotFoundError:
        print("File not found.")
        sys.exit(0)

    if len(tell) == 0:
        print("No tell found.")
        sys.exit(0)
    if not ask:
        print("No ask found.")
        sys.exit(0)

    method = sys.argv[1]
    kb = KnowledgeBase(tell, 'GS')

    if method == 'TT':
        tt = TruthTable(kb)
        query = Sentence(ask)
        print(tt.solve(query))
    elif method == 'FC':
        try:
            kb = KnowledgeBase(tell, 'HF')
            fc = ForwardChaining(kb)
            print(fc.solve(ask))
        except Exception as e:
            print(f"Error: {e}. Ensure the knowledge base contains only Horn-form sentences.")
    elif method == 'BC':
        try:
            kb = KnowledgeBase(tell, 'HF')
            bc = BackwardChaining(kb)
            print(bc.solve(ask))
        except Exception as e:
            print(f"Error: {e}. Ensure the knowledge base contains only Horn-form sentences.")
    elif method == 'RP':
        query = Sentence(ask)
        rp = ResolutionProver(kb, query, debug=debug_mode)
        print("YES" if rp.solve() else "NO")
    elif method == 'DPLL':
        query = Sentence(ask)
        dpll = DPLL(kb, query, debug=debug_mode)
        print("YES" if dpll.solve() else "NO")
    else:
        print("Unknown method entered.")

if __name__ == "__main__":
    main()
