from cgi import print_form


class State:
  def __init__(self, ori , aux, des, parent):
    self.ori = ori 
    self.aux = aux
    self.des = des
    self.parent = parent
  
    
def showState(s):#Mostrar pilha
  print('TorreA \t' + str(s.ori) + '\n' + 'TorreB \t' + str(s.aux) + '\n' + 'TorreC \t'+ str(s.des) + '\n')
  
def question():
  num = int(input('\nInforme a quantidade de discos: '))
  aux = [int(x) for x in range(num, 0, -1)]
  return aux
  
tower = question()

def initialState(tower):
  return State(tower, [], [], None) 

def isGoal(sgoal, tower):#Verificar se duas pilhas são iguais
  a = sgoal.des.copy()
  copyTower = tower.copy()
  if isEmpty(a):
    return False
  if lenght(a) != lenght(copyTower):
    return False
  towerqueue =[int(x) for x in range(0,lenght(copyTower), +1 )]
  while (lenght(copyTower)):
    if(a[0] == copyTower[0]):
      a.pop()
      copyTower.pop()
    else:
      return False
  return True
#  
# OPERAÇÕES COM PILHA
#
#EMPTY
def isEmpty(stack):
  return stack == []
  
#PUSH
def push(stack, element):
  aux = element
  return stack.append(aux)

#POP
def pop(stack):
  return stack.pop()
  
#TOP
def peek(stack):
  if isEmpty(stack):
    return 0
  return stack[len(stack) - 1]
  
#lENGTH
def lenght(stack):
  return len(stack)

#TRABALHANDO COM A FUNÇÃO DA EXPANSÃO
def copyState(stateCopy):
  cOri = stateCopy.ori.copy()
  cDes = stateCopy.des.copy()
  cAux = stateCopy.aux.copy()
  return State(cOri,cAux,cDes,stateCopy)
#
def verifyGoal(Vori, Vdes):
  return Vori > Vdes 
#
def playValidation(playOri, playDes):
  if isEmpty(playOri):
    return None
  if verifyGoal(peek(playOri), peek(playDes)) and not isEmpty(playDes):
    return None
  #if peek(playOri)%2 and peek(playDes)%2:
    #return None
  return True

def isEqual(s1, s2):
  if s1.ori == s2.ori and s1.aux == s2.aux and s1.des == s2.des:
    return True
  return False
#AÇÕES
#
#ori -> aux
def action1(ac1):
  copyAction1 = copyState(ac1)
  ori1 = copyAction1.ori
  aux1 = copyAction1.aux
  des1 = copyAction1.des

  if playValidation(ori1, aux1) == None:
    return None
  
  element = peek(ori1)
  pop(ori1)
  push(aux1, element)
  childState = State(ori1, aux1, des1, ac1)
  
  if isEqual(childState, ac1):
    return None
  return childState
#  
#ori -> des
def action2(ac2):
  copyAction2 = copyState(ac2)
  ori2 = copyAction2.ori
  aux2 = copyAction2.aux
  des2 = copyAction2.des

  if playValidation(ori2, des2) == None:
    return None
 
  element = peek(ori2)
  pop(ori2)
  push(des2, element)
  childState = State(ori2, aux2, des2, ac2)
  
  if isEqual(childState, ac2):
    return None
  return childState
#
#aux -> ori
def action3(ac3):
  copyAction3 = copyState(ac3)
  ori3 = copyAction3.ori
  aux3 = copyAction3.aux
  des3 = copyAction3.des

  if playValidation(aux3, ori3) == None:
    return None
    
  element = peek(aux3)
  pop(aux3)
  push(ori3, element)
  childState = State(ori3, aux3, des3, ac3)
  
  if isEqual(childState, ac3):
    return None
  return childState
#
#aux -> des
def action4(ac4):
  copyAction4 = copyState(ac4)
  ori4 = copyAction4.ori
  aux4 = copyAction4.aux
  des4 = copyAction4.des

  if playValidation(aux4, des4) == None:
    return None
  
  element = peek(aux4)
  pop(aux4)
  push(des4, element)
  childState = State(ori4, aux4, des4, ac4)
  
  if isEqual(childState, ac4):
    return None
  return childState
#
#des -> ori
def action5(ac5):
  copyAction5 = copyState(ac5)
  ori5 = copyAction5.ori
  aux5 = copyAction5.aux
  des5 = copyAction5.des

  if playValidation(des5, ori5) == None:
    return None
  
  element = peek(des5)
  
  pop(des5)
  push(ori5, element)
  childState = State(ori5, aux5, des5, ac5)
  
  if isEqual(childState, ac5):
    return None
  return childState
#
#des -> aux
def action6(ac6):
  copyAction6 = copyState(ac6)
  ori6 = copyAction6.ori
  aux6 = copyAction6.aux
  des6 = copyAction6.des

  if playValidation(des6, aux6) == None:
    return None
  
  element = peek(des6)
  pop(des6)
  push(aux6, element)
  childState = State(ori6, aux6, des6, ac6)
  
  if isEqual(childState, ac6):
    return None
  return childState

#Função de Expansão
def expand(stateExpand):    
  ret = []
  print('Expand')
  child1 = action1(stateExpand)
  if (child1 != None):
    ret.append(child1)
    
  child2 = action2(stateExpand)
  if (child2 != None):
    #showState(child2)
    ret.append(child2)
    
  child3 = action3(stateExpand)
  if (child3 != None):
    ret.append(child3)
    
  child4 = action4(stateExpand)
  if (child4 != None): 
    ret.append(child4)
    
  child5 = action5(stateExpand)
  if (child5 != None): 
    ret.append(child5)
    
  child6 = action6(stateExpand)
  if (child6 != None): 
    ret.append(child6)

  return ret

def showPath(s):
  if s is None:
    return
  showPath(s.parent)
  showState(s)
  
  
def isOnPath(child, ancestor):
  if ancestor is None:
    return False
  if isEqual(child, ancestor):
    return True
  return(child, ancestor.parent)

def isOpenState(s):
  for state in queue:
    if isEqual(s, state):
        return True
  return False

def isOnExpandedStates(s):
  for state in expandedStates:
    if isEqual(s,state):
      return True
  return False

#OPErAÇÔES COM A FILA
queue = [] 
def queueIsEmpty(queue):
  return queue == []

def enqueue(s):
  queue.append(s)

def dequeue():
  ret = queue[0]
  del queue[0]
  return ret

s = initialState(tower)

enqueue(s)

expandedStates = []
cont = 0

while not queueIsEmpty(queue):
  current = dequeue()
  if isOnExpandedStates(current):
    continue
  if isGoal( current, tower):
    print('Estado Objetivo')
    showPath(current)
    break

  showState(current) 

  children = expand(current)
  expandedStates.append(current)
  
  for child in children:
    enqueue(child)
    cont += 1
    
print('Filhos Expandidos', cont )
  
  