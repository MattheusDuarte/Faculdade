import copy
from heapq import heappop, heappush
import time


boardEasy =[['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '0', '0', '0', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '0', '1', '0', '#', '#', '#', '#'],
            ['#', '#', '0', '0', '0', '1', '0', '0', '0', '#', '#'],
            ['#', '#', '0', '1', '1', '1', '1', '1', '0', '#', '#'],
            ['#', '#', '0', '0', '0', '1', '0', '0', '0', '#', '#'],
            ['#', '#', '#', '#', '0', '1', '0', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '0', '0', '0', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

boardMedium =[['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '0', '0', '0', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '0', '1', '0', '#', '#', '#', '#'],
            ['#', '#', '0', '0', '1', '1', '1', '0', '0', '#', '#'],
            ['#', '#', '0', '1', '1', '1', '1', '1', '0', '#', '#'],
            ['#', '#', '1', '1', '1', '1', '1', '1', '1', '#', '#'],
            ['#', '#', '#', '#', '0', '0', '0', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '0', '0', '0', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

board =[['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '1', '1', '1', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '1', '1', '1', '#', '#', '#', '#'],
        ['#', '#', '1', '1', '1', '1', '1', '1', '1', '#', '#'],
        ['#', '#', '1', '1', '1', '0', '1', '1', '1', '#', '#'],
        ['#', '#', '1', '1', '1', '1', '1', '1', '1', '#', '#'],
        ['#', '#', '#', '#', '1', '1', '1', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '1', '1', '1', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

class State:
    def __init__(self, board, g, parent):
        self.board = board
        self.parent = parent
        self.g = g
        self.h = heuristic(board)
    
    def __lt__(self, other):
        return self.g + self.h < other.g + other.h
    
def initialState():
    return State(board, 0, None)

def isGoal(Tboard):
    cont = 0 
    for i in range(len(Tboard.board)):
        for j in range(len(Tboard.board[i])):
            if (Tboard.board[i][j] == '1'):
                cont += 1
                if cont > 1 :
                    return False
    
    return True

def showState(Tboard):
    for i in range(len(Tboard)):
        for j in range(len(Tboard[i])):
            print(Tboard [i][j] + '   ' , end='')
        print('\n')
    print('\n')

def copyBoard(Tboard):
    boardCopy = copy.deepcopy(Tboard)    
    return boardCopy


# COPIA UM ESTADO
def copyState(state):
    return State(copyBoard(state.board), state.g + 1 , state)    


def moveLeft(s, i, j):
    if(s.board[i][j + 1] != '1' ):
        return None
    
    if(s.board[i][j + 2] != '1' ):
        return None

    child = copyState(s)

    child.board[i][j] = '1'
    child.board[i][j + 1] = '0'
    child.board[i][j + 2] = '0'

    return child

def moveRight(s, i, j):
    if(s.board[i][j - 1] != '1' ):
        return None
    
    if(s.board[i][j - 2] != '1' ):
        return None

    child = copyState(s)

    child.board[i][j] = '1'
    child.board[i][j - 1] = '0'
    child.board[i][j - 2] = '0'

    return child

def moveUp(s, i, j):
    if(s.board[i - 1][j] != '1' ):
        return None
    
    if(s.board[i - 2][j] != '1' ):
        return None

    child = copyState(s)

    child.board[i][j] = '1'
    child.board[i - 1][j] = '0'
    child.board[i - 2][j] = '0'

    return child

def moveDown(s, i, j):
    if(s.board[i + 1][j] != '1' ):
        return None
    
    if(s.board[i + 2][j] != '1' ):
        return None

    child = copyState(s)

    child.board[i][j] = '1'
    child.board[i + 1][j] = '0'
    child.board[i + 2][j] = '0'

    return child

def expand(s):
    ret = []
    for i in range(0,11):
        for j in range(0,11):
            if (s.board[i][j] == '0'):
                
                child1 = moveLeft(s, i, j)
                if(child1 != None):
                    ret.append(child1)
                child2 = moveRight(s, i, j)
                if(child2 != None):
                    ret.append(child2)
                child3 = moveUp(s, i, j)
                if(child3 != None):
                    ret.append(child3)
                child4 = moveDown(s, i, j)
                if(child4 != None):
                    ret.append(child4)

    return ret

#Peças Sozinhas
def heuristic1(board):
    cont = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '1' and board[i+1][j] != '1' and board[i-1][j] != '1' and board[i][j+1] != '1' and board[i][j-1] != '1':
                cont += 1

    return cont

# Peças pares e impares 
def heuristic2(board):
    cont = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '1':
                neighboors = 0
                if board[i+1][j] == '1':
                    neighboors +=1
                if board[i-1][j] == '1':
                    neighboors += 1
                if board[i][j+1] == '1':
                    neighboors +=1
                if board[i][j-1] == '1':
                    neighboors += 1
                
                if neighboors%2 == 0:
                    cont += 1

    return cont

# Disponibilidade de peças juntas
def heuristic(board):
    cont = 0
    jmin = 1000
    jmax = 0
    imin = 1000
    imax = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '1':
                #cont += 1
                if i < imin:
                    imin = i
                if i > imax:
                    imax = i
                
                if j < jmin:
                    jmin = j
                if j > jmax:
                    jmax = j 
                                        
    height = jmax - jmin + 1
    width = imax - imin + 1
    cont = height * width
    return cont
queue = []

def enqueue(state):
    heappush(queue, (state.g + state.h, state))

def dequeue():
    (g, state) = heappop(queue)
    return state 

def queueIsEmpty():
    return len(queue) == 0

def showPath(state):
    if state is None:
        return
    showPath(state.parent)
    showState(state.board)

s = initialState()
enqueue(s)
cont = 0
cost = 0
#aux = 0
#comp = 0 
timeIn = time.time()

while not queueIsEmpty():
    
    current = dequeue()
    
    if isGoal(current):
        cost = current.g
        print('Reach goal !!!')
        showPath(current)
        break
 #   aux = len(current)
    children = expand(current)
    cont +=1    
    for child in children:
        enqueue(child)
    #if aux > comp:
     #   comp = aux
      #  aux = 0
timeGoal = time.time()

print('\n Estados Expndidos: ', cont)
#print('\n Estados máximos:', comp)
print('\n Tempo de execução em segundos: ', timeGoal - timeIn )

