from CNFConverter import CNFConverter

class ResolutionProver:
    def solve(self, query):
        kb_cnf = [CNFConverter.convert_to_cnf(sentence) for sentence in self.kb.sentences]
        negated_query = CNFConverter.convert_to_cnf(f"~({query})")
        clauses = kb_cnf + negated_query
        return self.apply_resolution(clauses)

    def apply_resolution(self, clauses):
        new = set()
        while True:
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
            for (ci, cj) in pairs:
                resolvents = self.resolve(ci, cj)
                if [] in resolvents:
                    return "YES"
                new.update(set(resolvents))
            if new.issubset(set(clauses)):
                return "NO"
            clauses.extend(list(new))

    def resolve(self, ci, cj):
        resolvents = []
        for di in ci:
            for dj in cj:
                if di == f'~{dj}' or dj == f'~{di}':
                    new_clause = list(set(ci).union(set(cj)) - {di, dj})
                    resolvents.append(new_clause)
        return resolvents
