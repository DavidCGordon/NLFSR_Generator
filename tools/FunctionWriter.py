from BitVector import BitVector
from itertools import permutations

def listXor(a,b):
    c = []
    for n in range(len(a)):
        if a[n] == b[n]:
            c.append(0)
        else:
            c.append(1)
    return c

def TT_to_ANF(n,tt):
    tt = [[x] for x in tt]
    nextRow = [x for x in range(len(tt)//2)]
    for k in range(n):
        for b in range(2**(n-k-1)):
            nextRow[b] = tt[2*b] + (listXor(tt[2*b],tt[2*b+1])) 
        tt = nextRow[:]
    ANF = []
    Cvec = nextRow[0]
    for j in range(len(Cvec)):
        if Cvec[j]:
            jBin = list(BitVector(intVal = j, size = n))
            anfTerm = sorted([(n-idx-1) for (idx, t) in enumerate(jBin) if t == 1], reverse = True)
            if anfTerm == []:
                ANF.append(True)
                pass
            else:
                ANF.append(anfTerm)
    return ANF

def reOrder(size,stateLoops):
    table = []
    for i in range(2**size):
        bitStr = format(i, "0" + str(size) + "b")
        
        for loop in stateLoops:
            for idx in range(len(loop)):
                if loop[idx] == bitStr:
                    table.append(loop[(idx + 1) % len(loop)])
                    
    return table

def writeFn(size,stateLoops):
    bitFn = []
    bigTable = reOrder(size,stateLoops)

    for bit in range(size):    
        bitTable = [int(bitStr[bit]) for bitStr in bigTable]
        bitAnf = TT_to_ANF(size,bitTable)
        bitFn.append(bitAnf)
    return bitFn[::-1]

def permuteEdges (p1, p2,stateLoops):
    out = stateLoops[:]
    loc1 = None
    loc2 = None
    for i in range(len(stateLoops)):
        for j in range(len(stateLoops[i])):
            if stateLoops[i][j] == p1 or stateLoops[i][j] == p2:
                if not loc1:
                    loc1 = (i,j)
                else:
                    loc2 = (i,j)
                    break
    if not loc1 or not loc2:
        pass
    elif loc1[0] == loc2[0]:
        out[loc1[0]] = stateLoops[loc1[0]][:loc1[1]+1] + \
                       stateLoops[loc2[0]][loc2[1]+1:]
        newList = stateLoops[loc1[0]][loc1[1]+1:loc2[1]+1]
        out.insert(loc1[0]+1, newList)
    else:
        out[loc1[0]] = stateLoops[loc1[0]][:loc1[1]+1] + \
                       stateLoops[loc2[0]][loc2[1]+1:] + \
                       stateLoops[loc2[0]][:loc2[1]+1] + \
                       stateLoops[loc1[0]][loc1[1]+1:]
        del out[loc2[0]]
    return out

