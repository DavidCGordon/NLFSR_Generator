from BitVector import BitVector

class NLFSR:
    def __init__(self, seed, fn):
        self.fn = fn
        self.size = len(fn)
        if seed == 0:
            raise ValueError("Seed value cannot be 0 or 1")
        else:
            self.state = BitVector(intVal = seed, size = self.size)

    def __iter__(self): return self
    
    def __str__(self): return self.state.__str__()

    def int_val(self): return int(self.state)

    def reverse(self, bitIdx): return (self.size-1-bitIdx % self.size)
    
    def __next__(self):
        nextState = BitVector(intVal = 0, size = self.size)
        
        for bitIdx in range(self.size):
            
            summation = 0
            for term in self.fn[bitIdx]:
                
                product = 1
                for idx in term:
                    product &= self.state[self.reverse(idx)]

                summation ^=  product

            nextState[(self.reverse(bitIdx))] = summation
        
        self.state = nextState
        return self.state