from CNFConverter import CNFConverter
from Sentence import Sentence

class ResolutionProver:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def solve(self, query):
        kb_cnf = []
        for sentence in self.kb.sentences:
            CNFConverter.expand_atomic(sentence, sentence.atomic)
            cnf_clauses = CNFConverter.convert_to_cnf(sentence)
            kb_cnf.extend(cnf_clauses)

        negated_query = Sentence(f"~({query})")
        CNFConverter.expand_atomic(negated_query, negated_query.atomic)
        negated_query_cnf = CNFConverter.convert_to_cnf(negated_query)

        clauses = kb_cnf + negated_query_cnf
        result = self.apply_resolution(clauses)
        print("Resolution Result:", result)
        return result

    def apply_resolution(self, clauses):
        new = set()
        while True:
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
            for (ci, cj) in pairs:
                resolvents = self.resolve(ci, cj)
                if [] in resolvents:
                    return "YES"
                new.update(set(map(tuple, resolvents)))
            if new.issubset(set(map(tuple, clauses))):
                return "NO"
            clauses.extend(map(list, new))

    def resolve(self, ci, cj):
        resolvents = []
        for di in ci:
            for dj in cj:
                if di == '||' or dj == '||':
                    continue  # Skip disjunction operators
                if (di.startswith('~') and di[1:] == dj) or (dj.startswith('~') and dj[1:] == di):
                    new_clause = [x for x in ci if x != di] + [x for x in cj if x != dj]
                    new_clause = list(set(new_clause))
                    new_clause = [lit for lit in new_clause if lit != '||']  # Remove '||' from new clause
                    if new_clause not in resolvents:
                        resolvents.append(new_clause)
        return resolvents
