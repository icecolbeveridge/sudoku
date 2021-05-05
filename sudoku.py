# bayesian sudoku
import itertools
import random

puzzle = """
 6 3  948
3 8 2   1
     1   
5 3 9 8  
  1  8   
6 7 4 3  
     7   
7 4 5   9
 9 6  723"""

class Cell:
    def __init__(self):
        self.probs = {i: 1/9 for i in range(1,10)}
        self.solved = False
        
    def set_value(self, v):
        self.probs = {v: 1.}
        self.solved = True
        
    def get_value(self):
        if len(self.probs) == 1:
            return min(self.probs)
        
    def remove_key(self, v):
        if v in self.probs:
            del self.probs[v]
        if len (self.probs) == 1:
            self.solved = True
        else:
            self.normalise()
        
    def normalise(self):
        s = sum(self.probs.values())
        todel = []
        for k in self.probs:
            if self.probs[k] == 0:
                todel.append(k)
            else:
                self.probs[k] /= s
        for k in todel:
            self.remove_key(k)        
     
    def get_prob(self, i):
        if i in self.probs:
            return self.probs[i]
        else:
            return 0    
            
    def set_prob(self, i,v):
        if i in self.probs:
            self.probs[i] = v   

class Puzzle:
    def __init__(self, grid):
        self.grid = grid
        
        self.cells = { (i,j) : Cell() for (i,j) in itertools.product(range(1,10),repeat = 2)}
        self.handle_grid()
        
    def handle_grid(self):
        lines = self.grid.split("\n")
        for i,l in enumerate(lines):
            for j,k in enumerate(l):
                try:
                    ki = int(k)
                    self.cells[(i,1+j)].set_value(ki)
                except ValueError:
                    pass
                    
    def get_random_column_keys(self):
        r = random.choice(range(1,10))
        return [(r,i) for i in range(1,10)]
    
    def get_random_row_keys(self):
        r = random.choice(range(1,10))
        return [(i,r) for i in range(1,10)]
        
    def get_random_box_keys(self):
        r1 = 3 * random.choice(range(3))
        r2 = 3 * random.choice(range(3))
        out = []
        for i in range(r1+1,r1+4):
            for j in range(r2+1,r2+4):
                out.append((i,j))
        return out
    
    def sanitise(self, block_keys):
        # get values of solved cells
        cells = [self.cells[i] for i in block_keys]
        solved_values = [c.get_value() for c in cells if c.solved]
        for v in solved_values:
            for c in cells:
                if not c.solved:
                    c.remove_key(v)

        
    
    def fix_random_block(self):
        # this is the workhorse
        funcs = [self.get_random_column_keys,
                 self.get_random_row_keys,
                 self.get_random_box_keys]
        f = random.choice(funcs)
        
        block_keys = f()
        # sanitise for solved cells
        self.sanitise(block_keys)
        # normalise by cell
        cells = [self.cells[i] for i in block_keys]
        
        for c in cells:
            c.normalise()
        
        # normalise the block
        for i in range(1,10):
            s = sum([c.get_prob(i) for c in cells ])
            for c in cells:
                c.set_prob( i, c.get_prob(i) / s )
        # normalise by cell
        for c in cells:
            c.normalise()

    def solve_count(self):
        return len([c for c in self.cells.values() if c.solved])
    
    def __repr__(self):
        out = ""
        for i in range(1,10):
            for j in range(1,10):
                if self.cells[(i,j)].solved:
                    out += str (self.cells[(i,j)].get_value())
                else:
                    out += " "
                if j in (3,6):
                    out += "|"
            out += "\n"
            if i in (3,6):
                out += "---+" * 2 + "---\n"
        return out
            
         
            
    def solve(self):
        sc = 0
        while (nsc := self.solve_count()) < 81:
            self.fix_random_block()
            if nsc != sc:
                print (self)
                #input()
                sc = nsc
        print (self)
P = Puzzle(puzzle)
P.solve()