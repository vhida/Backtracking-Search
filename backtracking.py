#!/usr/bin/python

import sys


class sudoku_solver():
    def __init__(self,size):
        self.size = size
        self.sudoku = [[0 for x in range(self.size)] for y in range(self.size)] 
        self.guesses = 0
    def read(self,f):
        s = open(f,'r').read().split('\n')
        for k in range(0,self.size):
            self.sudoku[k] = s[k].split(' ')
            for j in range(0,self.size):
                if self.sudoku[k][j] == '-':
                    self.sudoku[k][j] = 0
                else:
                    self.sudoku[k][j] = int(self.sudoku[k][j])
        print 'Puzzle for ',f,' is : '
        for k in range(self.size):
            print ' '.join(map(str,self.sudoku[k]))
        rs = open('guesses.txt','a')
        rs.write('puzzel '+f)
    def is_valid(self,v,row, col, s):
        # check row        
        if v in s[row]:
            return False
        # row column
        for k in range(9):
            if s[k][col] == v :
                return False
        #check sub-square
        b_row = row/3
        b_col = col/3
        
        dial = [s[b_row*3][b_col*3],s[b_row*3+1][b_col*3+1],s[b_row*3+2][b_col*3+2]]
        if v in dial :
            return False
            
        return True  
    
    def solve(self):
        for i in range(self.size) :
            for j in range(self.size):
                if (self.sudoku[i][j] != 0) :
                    continue;
                
                for v in range(self.size):
                    self.guesses +=8# always loop through 9 possible values 
                    if (self.is_valid(v+1, i, j, self.sudoku)) :
                        self.sudoku[i][j] = v+1
                        if self.solve() :
                            return True
                        else: 
                            self.sudoku[i][j] = 0;

                return False;
        return True;
        
    
    def present(self):
        if self.solve() :
            print '-----------------------------------'
            print "Solution is : "
            for k in range(self.size):
                print ' '.join(map(str,self.sudoku[k]))
            print 'Number of Guesses is :', self.guesses
            rs = open('guesses.txt','a')
            rs.write(' : there are '+str(self.guesses)+' guesses\n')
puzzels = sys.argv
puzzels.pop(0)
print puzzels
for puzzel in puzzels:
    solver = sudoku_solver(9)
    solver.read(puzzel)
    solver.present()