#!/usr/bin/python

import copy,Queue,sys
regions = ([['c'+str(i)+str(j) for i in range(0,9)] for j in range(0,9)] + # columns - these are the forward checking sets
          [['c'+str(j)+str(i) for i in range(0,9)] for j in range(0,9)] + # rows
           [['c'+str(i)+str(j) for i in range(3*y,3*y+3) for j in range(3*x, 3*x+3)] for x in range(0,3) for y in range(0,3)]) # boxes

class csp: # object which holds the state of a board
  def __init__(self, domains, arcs, constraint):
    self.domains = domains 
    self.arcs = arcs 
    self.constraint = constraint # function(i,j) returns true if i,j satisfy the constraint
    self.guesses = 0

def read(file):
  def boxRange(x): return range((x/3)*3,(x/3)*3+3) #
  def constraint(i, j): return (i != j)
  def arcgen(x,y): # generates a list of the keys which x,y constrains
    return ['c'+str(i)+str(j) for i in range(0,9) for j in range(0,9) if 
            (i != x or y != j) and (i == x or j == y or (i in boxRange(x) and j in boxRange(y)))]
  data = [('c'+str(i)+str(j/2), c) for i, line in enumerate(open(file)) for j, c in enumerate(line[0:-1]) if c!=' ']
  domains = {key: (range(1,10) if c == '-' else [int(c)]) for (key, c) in data}
  arcs = {key: arcgen(int(key[1]),int(key[2])) for (key, c) in data}
  sudoku = csp(domains, arcs, constraint)
  print 'Puzzel for ',file,' is '
  print_sudoku(sudoku)
  print_sudoku(sudoku)
  return sudoku

def print_sudoku(csp): # print the board state nicely
  sudoku = [range(0,9) for i in range(0,9)]
  for x in csp.domains:
    sudoku[int(x[1])][int(x[2])] = str(csp.domains[x][0]) if len(csp.domains[x]) == 1 else "-"
  for x in sudoku: print (' '.join(x))

def removeInconsistency(csp, i, j): # Standard apply_AC3 with its helper method, based on AIMA pseudocode
  removed = False
  for x in csp.domains[i][:]:
    if not any([csp.constraint(x, y) for y in csp.domains[j]]):
      csp.domains[i].remove(x)
      removed = True
  return removed

def apply_AC3(csp):
  queue = [(i, j) for i in csp.domains for j in csp.arcs[i]]
  while queue:
    i, j = queue.pop()
    if removeInconsistency(csp, i, j):
        for k in csp.arcs[i]:
          if i != k: queue.append((k, i))

def solveForward(csp):
  changed = True
  while changed:
    apply_AC3(csp)
    changed = False
    for r in regions: # for each region (row, column, box)
      domain = range(1,10)
      [domain.remove(csp.domains[k][0]) for k in r if len(csp.domains[k]) == 1]
      for d in domain: # iterate over the values which haven't been assigned in that value
        if sum(csp.domains[k].count(d) for k in r) == 1:
          csp.domains[[k for k in r if csp.domains[k].count(d) > 0][0]] = [d] # if only one cell can have that value, assign it
          changed = True

def solve(csp):
    q = Queue.LifoQueue()
    q.put(copy.deepcopy(csp))
    while q:
        node = q.get()
        solveForward(node) # use forward checking as a subroutine for each node
        #apply_AC3(node)
        #print node.domains
        if all([len(node.domains[k]) == 1 for k in node.domains]): # if solved, return
            return node
        if not any([len(node.domains[k]) == 0 for k in node.domains]): # if the node is potentially solvable (no domains are empty)
            # apply MRV heuristic            
            domain_size = 10
            pick_index = 0
            for k in node.domains:
                if len(node.domains[k]) > 1 and len(node.domains[k]) < domain_size :
                    domain_size = len(node.domains[k])
                    pick_index = k
            guessKey = pick_index
            
            for guess in node.domains[guessKey]:# add each guess to the queue
                csp.guesses +=1 
                #print 'entering evaluation : number of guesses is',csp.guesses
                successor = copy.deepcopy(node)
                successor.domains[guessKey] = [guess]
                #print 'number is ',csp.guesses
                q.put(successor)
#for testing                
#s =solve(read('puz-001.txt'))
#print_sudoku(s)
puzzels = sys.argv
puzzels.pop(0)
f = open('guesses_with_inference_ac3.txt','a')

for puzzel in puzzels:
    sudoku = read(puzzel)
    solve(sudoku)
    print 'number of guesses is ', sudoku.guesses
    f.write('For '+puzzel+' there are '+ str(sudoku.guesses)+' guesses\n')
    print 'Solution for  is ' 
    print_sudoku(sudoku)
f.write('--------------------------------------------------\n\n')
