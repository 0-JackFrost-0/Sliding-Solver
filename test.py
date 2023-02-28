### TEAM MEMBERS
## MEMBER 1: 21d100006
## MEMBER 2: 21d180043
## MEMBER 3: 210100143


from z3 import *
import sys

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

def c1_up(s):
    return [
        [s[1][0], s[0][1], s[0][2]],
        [s[2][0], s[1][1], s[1][2]],
        [s[0][0], s[2][1], s[2][2]]
    ]

def c2_up(s):
    return [
        [s[0][0], s[1][1], s[0][2]],
        [s[1][0], s[2][1], s[1][2]],
        [s[2][0], s[0][1], s[2][2]]
    ]

def c3_up(s):
    return [
        [s[0][0], s[0][1], s[1][2]],
        [s[1][0], s[1][1], s[2][2]],
        [s[2][0], s[2][1], s[0][2]]
    ]

def c1_down(s):
    return [
        [s[2][0], s[0][1], s[0][2]],
        [s[0][0], s[1][1], s[1][2]],
        [s[1][0], s[2][1], s[2][2]]
    ]

def c2_down(s):
    return [
        [s[0][0], s[2][1], s[0][2]],
        [s[1][0], s[0][1], s[1][2]],
        [s[2][0], s[1][1], s[2][2]]
    ]

def c3_down(s):
    return [
        [s[0][0], s[0][1], s[2][2]],
        [s[1][0], s[1][1], s[0][2]],
        [s[2][0], s[2][1], s[1][2]]
    ]

def r1_left(s):
    return [
        [s[0][1], s[0][2], s[0][0]],
        [s[1][0], s[1][1], s[1][2]],
        [s[2][0], s[2][1], s[2][2]]
    ]

def r2_left(s):
    return [
        [s[0][0], s[0][1], s[0][2]],
        [s[1][1], s[1][2], s[1][0]],
        [s[2][0], s[2][1], s[2][2]]
    ]

def r3_left(s):
    return [
        [s[0][0], s[0][1], s[0][2]],
        [s[1][0], s[1][1], s[1][2]],
        [s[2][1], s[2][2], s[2][0]]
    ]

def r1_right(s):
    return [
        [s[0][2], s[0][0], s[0][1]],
        [s[1][0], s[1][1], s[1][2]],
        [s[2][0], s[2][1], s[2][2]]
    ]

def r2_right(s):
    return [
        [s[0][0], s[0][1], s[0][2]],
        [s[1][2], s[1][0], s[1][1]],
        [s[2][0], s[2][1], s[2][2]]
    ]

def r3_right(s):
    return [
        [s[0][0], s[0][1], s[0][2]],
        [s[1][0], s[1][1], s[1][2]],
        [s[2][2], s[2][0], s[2][1]]
    ]

def move(op, s, i, j):
    return  If(op == 0, c1_down(s)[i][j],
            If(op == 1, c2_down(s)[i][j],
            If(op == 2, c3_down(s)[i][j],
            If(op == 3, c1_up(s)[i][j],
            If(op == 4, c2_up(s)[i][j],
            If(op == 5, c3_up(s)[i][j],
            If(op == 6, r1_left(s)[i][j],
            If(op == 7, r2_left(s)[i][j],
            If(op == 8, r3_left(s)[i][j],
            If(op == 9, r1_right(s)[i][j],
            If(op == 10, r2_right(s)[i][j],
            If(op == 11, r3_right(s)[i][j], s[i][j]))))))))))))

move_names = ["c1d", "c2d", "c3d", "c1u", "c2u", "c3u", "r1l", "r2l", "r3l", "r1r", "r2r", "r3r"]

for moves in range(T+1): # 1..11
    print ("moves=", moves)

    s = Solver()
    # check if range of moves is set correctly
    state = [[[Int("s_%d_%d_%d" % (k, i, j)) for j in range(n)] for i in range(n)] for k in range(moves+1)]
    op=[Int('op_%d' % l) for l in range(moves+1)]

    # initial state
    for i in range(n):
        for j in range(n):
            s.add(state[0][i][j] == matrix[i][j])
    
    # final state
    for i in range(n):
        for j in range(n):
            s.add(state[moves][i][j] == i*n+j+1)
    
    # all moves are in range
    for mov in range(moves):
        for i in range(n):
            for j in range(n):
                # s.add(And(state[mov][i][j] >= 1, state[mov][i][j] <= n*n))
                s.add(state[mov+1][i][j] == move(op[mov], state[mov], i, j))
    
# Set s to the required formula

    x = s.check()
    if x == sat:
        print(x)
        m = s.model()
        for mov in range(moves):
            print (move_names[int(str(m[op[mov]]))])
        exit(0)
        
	# Output the moves