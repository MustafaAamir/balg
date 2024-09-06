from itertools import combinations

'''
initialize variables and minterms
variables := [A, B, C]
minterms  := [0, 3, 6, 7]
minters   := [000, 011, 110, 111]
        |
        V
find prime_implicants from
| A | B | C |output |
--------------------
| 0 | 0 | 0 |  1   |
| 0 | 0 | 1 |  0   |
| 0 | 1 | 0 |  0   |
| 0 | 1 | 1 |  1   |
| 1 | 0 | 0 |  0   |
| 1 | 0 | 1 |  0   |
| 1 | 1 | 0 |  1   |
| 1 | 1 | 1 |  1   |
--------------------

| group | minterm | A | B | C |
------------------------------
|   0   | m[0]    | 0 | 0 | 0 |
|   2   | m[1]    | 0 | 1 | 1 |
|       | m[2]    | 1 | 1 | 0 |
|   3   | m[3]    | 1 | 1 | 1 |
------------------------------

find pair where only one variable differs

| group | minterm      | A | B | C |
------------------------------------
|   0   | m[0]         | 0 | 0 | 0 | -> ~(ABC)
|   2   | m[1]-m[3]    | _ | 1 | 1 | -> BC
|       | m[2]-m[3]    | 1 | 1 | _ | -> AB
-----------------------------------

since the bit-diff between pairs in each class is > 1, we move onto the next step

|  expr  | m0  | m1  | m2  | m3  |
---------------------------------
| ~(ABC) | X   |     |     |     |
|   BC   |     |  X  |     |     |
|   AB   |     |     |  X  |     |
----------------------------------

If each column contains one element, the expression can't be eliminated. Therefore, the resulting expression is:
        ~(ABC) + BC + AB
'''

class TruthTableSynthesizer:
    def __init__(self, variables, minterms):
        self.variables = variables
        self.minterms = set(minterms)
        self.num_vars = len(variables)
        # unnecesary
        self.max_iterations = 1000  # Safeguard against excessive looping

    def decimal_to_binary(self, num):
        return format(num, f'0{self.num_vars}b')

    def combine_implicants(self, implicants):
        combined = set()
        for a, b in combinations(implicants, 2):
            diff = [i for i in range(self.num_vars) if a[i] != b[i]]
            # appends minterms with a 1 bit difference
            if len(diff) == 1:
                combined_implicant = list(a)
                combined_implicant[diff[0]] = '-'
                combined.add(''.join(combined_implicant))
        return combined

    def get_prime_implicants(self):
        # creating the aforementioned classes for n + 1 bits
        groups = [set() for _ in range(self.num_vars + 1)]
        for m in self.minterms:
            # classifies minters into groups, so
            # groups[3] = '0b0111'
            # groups[2] = '0b1001'
            groups[bin(m).count('1')].add(self.decimal_to_binary(m))

        prime_implicants = set()
        iteration = 0
        while iteration < self.max_iterations: # precaution, although i don't think it's necessary
            new_groups = [set() for _ in range(self.num_vars)]
            for i in range(len(groups) - 1):
                # compares each element in group n to each element in group n + 1
                # if the bit-diff == 1, group[n] = the implicant + the uncommon bit is set to 'don't care'
                new_implicants = self.combine_implicants(groups[i] | groups[i+1])
                new_groups[i] = new_implicants
                uncombined = groups[i] | groups[i+1] - {imp for imp in new_implicants for c in imp if c != '-'}
                prime_implicants |= uncombined
            if not any(new_groups):
                prime_implicants |= set.union(*groups)
                break
            groups = new_groups
            iteration += 1
        return prime_implicants

    def covers_minterm(self, implicant, minterm):
        # will return true if implicant implicant overlaps with minterm, disregarding the 'dont care' bits
        return all(i == '-' or i == m for i, m in zip(implicant, self.decimal_to_binary(minterm)))

    def get_essential_prime_implicants(self, prime_implicants):
        coverage = {m: [pi for pi in prime_implicants if self.covers_minterm(pi, m)] for m in self.minterms}
        essential = set()
        for _, implicants in coverage.items():
            if len(implicants) == 1:
                essential.add(implicants[0])
        return essential

    def minimize_function(self, prime_implicants, essential_implicants):
        covered_minterms = set()
        result = list(essential_implicants)
        remaining_implicants = prime_implicants - essential_implicants
        for ei in essential_implicants:
            covered_minterms |= {m for m in self.minterms if self.covers_minterm(ei, m)}

        while covered_minterms != self.minterms:
            best_implicant = max(remaining_implicants, key=lambda x: sum(self.covers_minterm(x, m) for m in self.minterms - covered_minterms))
            result.append(best_implicant)
            covered_minterms |= {m for m in self.minterms if self.covers_minterm(best_implicant, m)}
            remaining_implicants.remove(best_implicant)

        return result

    def implicant_to_expression(self, implicant):
        terms = []
        # forms a list of tuples of variables and implicants
        # if a variable's corresponding bit is 0, appends NOT <variable>
        # otherwies, appends variable
        # | A | B | C |
        # ------------
        # | 0 | 1 | 0 | -> (A's bit == 0 ? append NOT A)
        #               -> (B's bit == 1 ? append B')
        #               -> (C's bit == 0 ? append NOT C)
        #               -> join every appended element with AND
        # | 1 | 0 | 1 | -> ...
        for var, value in zip(self.variables, implicant):
            if value == '1':
                terms.append(var)
            elif value == '0':
                terms.append(f'NOT {var}')
        return ' AND '.join(terms) if terms else '1'

    def synthesize(self):
        # case where every output is NOT high
        if not self.minterms:
            return '0'
        # case where every output is high
        if len(self.minterms) == 2**self.num_vars:
            return '1'

        prime_implicants = self.get_prime_implicants()
        essential_implicants = self.get_essential_prime_implicants(prime_implicants)
        minimal_implicants = self.minimize_function(prime_implicants, essential_implicants)

        expression_terms = [self.implicant_to_expression(imp) for imp in minimal_implicants]
        expression = ' OR '.join(f'({term})' for term in expression_terms)

        return expression

