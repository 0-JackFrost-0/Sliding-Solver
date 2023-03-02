### TEAM MEMBERS
## MEMBER 1: <roll_number_1>
## MEMBER 2: <roll_number_2>
## MEMBER 3: <roll_number_3>
import sys
import time
from copy import deepcopy

from z3 import *

init_time = time.time()

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

ideal_matrix = [[(i*n+j+1)for j in range(n)] for i in range(n)]

elements = [[[Int(f"x_{i+1}_{j+1}_{k}") for j in range(n)] for i in range(n)] for k in range(T+1)]

moves_l = [[Bool(f"l_{j+1}_{i+1}") for j in range(n)] for i in range(T)] 
moves_r = [[Bool(f"r_{j+1}_{i+1}") for j in range(n)] for i in range(T)]
moves_u = [[Bool(f"u_{j+1}_{i+1}") for j in range(n)] for i in range(T)]
moves_d = [[Bool(f"d_{j+1}_{i+1}") for j in range(n)] for i in range(T)]
moves_n = [[Bool(f"n_{i+1}")] for i in range(T)]

def get_next_state(curr_state, move):
	curr_state_copy = deepcopy(curr_state)
	move = str(move)
	if move[0] == 'l':
		row = move.split("_")[1]
		curr_state_copy[int(row)-1] = curr_state[int(row)-1][1:] + [curr_state[int(row)-1][0]]
	elif move[0] == 'r':
		row = move.split("_")[1]
		curr_state_copy[int(row)-1] = [curr_state[int(row)-1][-1]] + curr_state[int(row)-1][:-1]
	elif move[0] == 'u':
		col = move.split("_")[1]
		col_values = [curr_state[i][int(col)-1] for i in range(n)]
		for i in range(n):
			curr_state_copy[i][int(col)-1] = col_values[(i+1)%n]
		pass
	elif move[0] == 'd':
		col = move.split("_")[1]
		col_values = [curr_state[i][int(col)-1] for i in range(n)]
		for i in range(n):
			curr_state_copy[i][int(col)-1] = col_values[(i-1)%n]
	elif move[0] == 'n':
		pass
	return curr_state_copy

initial_state = [elements[0][i][j] == matrix[i][j] for i in range(n) for j in range(n)]

final_state = [elements[T][i][j] == ideal_matrix[i][j] for i in range(n) for j in range(n)]

s = Solver()

# Set s to the required formula
s.add(initial_state)
s.add(final_state)

# all elements are in range 1 to n^2
# for k in range(T+1):
# 	for i in range(n):
# 		for j in range(n):
# 			s.add(And(elements[k][i][j] >= 1, elements[k][i][j] <= n*n))

for k in range(T):
	moves_available = moves_r[k] + moves_l[k] + moves_u[k] + moves_d[k] + moves_n[k]
	s.add(PbEq([(x,1) for x in moves_available], 1))
	for move in moves_available:
		for i in range(n):
			for j in range(n):
				s.add(Implies(move, elements[k+1][i][j] == get_next_state(elements[k], move)[i][j]))
	
	# if k < T-1:
	# 	moves_available_next = moves_r[k+1] + moves_l[k+1] + moves_u[k+1] + moves_d[k+1] + moves_n[k+1]
	# 	for i, move in enumerate(moves_available):
	# 		s.add(Implies(move, moves_available_next[i] == False))

x = s.check()
print(x)
if x == sat:
	m = s.model()
	# for k in range(T+1):
	# 	moves_available = []
	# 	if k < T:
	# 		moves_available = moves_r[k] + moves_l[k] + moves_u[k] + moves_d[k]
	# 	print(f"State {k}")
	# 	for i in range(n):
	# 		for j in range(n):
	# 			print(m[elements[k][i][j]], end=" ")
	# 		print()
	# 	print()
	# 	for elem in moves_available:
	# 		if m[elem] == True:
	# 			print(str(int(str(elem).split("_")[1])-1)+str(elem)[0])
	# 	print()

	# Output the moves
	for i in range(T):
		moves_available = moves_r[i] + moves_l[i] + moves_u[i] + moves_d[i]
		for move in moves_available:
			if m[move] == True and str(move).startswith("n")==False:
				print(str(int(str(move).split("_")[1])-1)+str(move)[0])
				break
finish = time.time()
sys.stderr.write("Time taken: " + str(finish-init_time) + " seconds\n")