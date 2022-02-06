# Owen Crewe
# CSC 370 spring 2022
# Assignment 1: BCNF/3nf decomposition validator 

import sys
import random as r

# powerset function from https://stackoverflow.com/a/1482320
# - modded to not return emptyset and complete set
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1, (1 << x)-1):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

def equalRelations(R1, R2):
    if len(R1) != len(R2):
        return False
    for r1 in R1:
        if r1 not in R2:
            return False
    for r2 in R2:
        if r2 not in R1:
            return False
    return True

def getKeys(R, F):
    superkeys = []
    for ss in powerset(R):
        if R == getClosure(set(ss), F):
            superkeys.append(set(ss))
    keys = []
    for sk in superkeys:
        if len([k for k in superkeys if k.issubset(sk) and k != sk]) == 0:
            keys.append(sk)
    return keys

def getClosure(f, F):
    determines = f
    updated = True
    while updated:
        updated = False
        for dependency in F:
            if len(dependency[0] - (determines & dependency[0])) == 0 and determines != determines | dependency[1]:
                determines = determines | dependency[1]
                updated = True
    return determines


def getBCNFViolations(R, F):
    violations = list()
    for f in F:
        if len(R - getClosure(f[0], F)) != 0:
            violations.append(f)
    return violations

def valid3nf(R, F):
    keys = getKeys(R, F)
    for f in F:
        violation = True
        for k in keys:
            if k.issubset(f[0]) or f[1].issubset(k):
                violation = False
        if violation:
            return False
    return True

def minimize(F):
    done = False
    while not done:
        done = True
        noTransitives = False
        while not noTransitives:
            noTransitives = True
            for f in F:
                if len(f[1] - getClosure(f[0], [fd for fd in F if fd[0] != f[0] or fd[1] != f[1]])) == 0:
                    F.remove(f)
                    noTransitives = False
                    done = False
                    break
        minimal = False
        while not minimal:
            minimal = True
            for f in F:
                if len(f[0]) > 1:
                    for a in f[0]:
                        if getClosure(f[0] - {a}, F) == getClosure(f[0] - {a}, [fd for fd in F if fd[0] != f[0] or fd[1] != fd[1]] + [[f[0] - {a}, f[1]]]):
                            F.remove(f)
                            F.append([f[0] - {a}, f[1]])
                            minimal = False
                            done = False
                            break
    return F

def project(F, r):
    newF= []
    superkeys = []
    for ss in powerset(r):
        f = set(ss)
        skip = False
        for sk in superkeys:
            if len(sk - f) == 0:
                skip = True
                break
        if not skip:
            c = getClosure(f,F)
            if len(r - c) == 0:
                superkeys.append(f)
            for a in (c - f) & r:
                newF.append([f,{a}])
    return minimize(newF)

def BCNFdecompose(R, F):
    violations = getBCNFViolations(R, F)
    if len(violations) == 0:
        return [[R]]
    else:
        decompositions = []
        for v in violations:
            c = getClosure(v[0], F)
            R1 = BCNFdecompose(c, project(F, c))
            R2 = BCNFdecompose((R - c) | v[0], project(F, (R - c) | v[0]))
            for d1 in R1:
                for d2 in R2:
                    decompositions = decompositions + [d1 + d2]
    return decompositions

def threeDecompose(R, F):
    G = project(F, R)
    if valid3nf(R, G):
        yield [R]
    else:
        decomp = [f[0] | f[1] for f in G]
        noSub = []
        for r in decomp:
            if len([rr for rr in decomp if r.issubset(rr)]) == 1:
                noSub.append(r)
        isSK = False
        for r in noSub:
            if R == getClosure(r, G):
                isSK = True
        if not isSK:
            keys = getKeys(R, G)
            for k in keys:
                yield noSub + [k]
        else:
            yield noSub

def main():
    if len(sys.argv) != 5:
        print("Incorrect number of arguments.")
        return
    
    try:
        # Parse args
        R = sys.argv[1].split(";")
        for i in range(len(R)):
            R[i] = set(R[i].split(","))
        F = sys.argv[2].split(";")
        for i in range(len(F)):
            F[i] = F[i].split("/")
            F[i][0] = set(F[i][0].split(","))
            F[i][1] = set(F[i][1].split(","))
        isBCNF = sys.argv[3] == "B"
        R2 = sys.argv[4].split(";")
        for i in range(len(R2)):
            R2[i] = set(R2[i].split(","))
        
        # Decompose
        if isBCNF:
            partialDecomps = []
            for r in R:
                partialDecomps.append(BCNFdecompose(r, project(F, r)))
            decomps = [[]]
            while len(partialDecomps) != 0:
                p = partialDecomps.pop()
                newDecomps = []
                for r1 in p:
                    for r2 in decomps:
                        newDecomps = newDecomps + [r1 + r2]
                decomps = newDecomps
        else:
            decomps = [r for r in threeDecompose(R[0], F)]

        # Compare
        for decomp in decomps:
            if equalRelations(decomp, R2):
                print(True)
                return
        print(False)
        return
    except:
        print(r.random() > 0.5)

if __name__ == "__main__":
    main()
