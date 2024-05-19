import sys
from FileReader import FileReader
from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from TruthTable import TruthTable
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining
from ResolutionProver import ResolutionProver

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Enter command in following format: iengine method filename")
        print("Methods: TT, FC, BC, RP")
        exit(0)

    try:
        tell, ask = FileReader.read(sys.argv[2])
    except:
        print("File not found.")
        sys.exit(0)

    if len(tell) == 0:
        print("No tell found.")
        sys.exit(0)
    if not ask:
        print("No ask found.")
        sys.exit(0)

    method = sys.argv[1]
    if method == 'TT':
        kb = KnowledgeBase(tell, 'GS')
        tt = TruthTable(kb)
        print(tt.solve(ask))
    elif method == 'FC':
        kb = KnowledgeBase(tell, 'HF')
        fc = ForwardChaining(kb)
        print(fc.solve(ask))
    elif method == 'BC':
        kb = KnowledgeBase(tell, 'HF')
        bc = BackwardChaining(kb)
        print(bc.solve(ask))
    elif method == 'RP':
        kb = KnowledgeBase(tell, 'GS')
        query = Sentence(ask)
        rp = ResolutionProver(kb, query)
        print(rp.solve())
    else:
        print("Unknown method entered.")
