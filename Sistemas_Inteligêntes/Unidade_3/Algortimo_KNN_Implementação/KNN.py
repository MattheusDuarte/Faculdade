import numpy as np
import math
from csv import reader

#ler um arquivo .data e retorna os valores convertidos
def lerDatabase(file):

    lista=[]

    with open(file, 'rt') as f:
        for linha in f.readlines():
            a=linha.replace('\n','').split(',')
            lista.append(a)

    for i in range( len(lista) ):
        for j in range(4):
            lista[i][j] = float(lista[i][j])
    
    return lista

#retornar os subconjuntos
def subConjuntos(file):

    setosa = []
    versicolor = []
    virginica = []

    setosa = file[0:50]
    versicolor = file[50:100]
    virginica = file[100:150]

    return [setosa, versicolor, virginica]

#retorna o maior e menor elemento de uma coluna
def maxMinColuna(coluna, conjunto):

    aux = 0
    aux2 = 0
    maxNum = 0
    minNum = 0

    for i in range( len(conjunto) ):
        if(conjunto[i][coluna] >= aux):
            maxNum = conjunto[i][coluna]
            aux = maxNum

    aux2 = maxNum
    for j in range( len(conjunto) ):
        if(conjunto[j][coluna] <= aux2 ):
            minNum = conjunto[j][coluna]
            aux2 = minNum
    return [maxNum, minNum]

def normalizaConjunto(conjunto):
    
    x = 0

    copiaConjunto = conjunto.copy()

    for i in range(4):

        maxValor, minValor = maxMinColuna(i, conjunto)

        for j in range( len(conjunto) ):
            x = round( -1 + (2*(conjunto[j][i] - minValor)/(maxValor - minValor)) , 2) 
            copiaConjunto[j][i] = x

    return copiaConjunto

#normalização
def normalizacao(file):

    listaNormalizada = []

    subSetosa, subVersicolor, subVirginica = subConjuntos(file)

    normSetosa = normalizaConjunto(subSetosa)
    normVersicolor = normalizaConjunto(subVersicolor)
    normVirginica = normalizaConjunto(subVirginica)

    listaNormalizada = np.concatenate((normSetosa,normVersicolor,normVirginica))
    return listaNormalizada

def testeTreino(file, perc):

    treino = []
    teste = []
    
    
    conjSetosa, conjVersicolor, conjVirginica = subConjuntos(file)

    iSe = int(len(conjSetosa)*perc)
    iVe = int(len(conjVersicolor)*perc)
    iVi = int(len(conjVirginica)*perc)

    treino.extend(conjSetosa[0:iSe])
    treino.extend(conjVersicolor[0:iVe])
    treino.extend(conjVirginica[0:iVi])

    teste.extend(conjSetosa[iSe :len(conjSetosa)])
    teste.extend(conjVersicolor[iVe: len(conjVersicolor)])
    teste.extend(conjVirginica[iVi: len(conjVirginica)])

    return [treino, teste]

#distância Euclidiana
def disEuclidina(v1, v2):

    dim = len(v1)
    soma = 0

    for i in range(dim - 1):
        soma += math.pow(v1[i] - v2[i], 2)
    return math.pow(soma)

#Quando q = 1, esta distância representa a distância de Manhattan e quando
# q = 2, a distância Euclidiana. 

# ditância Minkowski
def disMinkowski(v1, v2, q):
    
    dim = len(v1)
    soma = 0

    for i in range(dim -1):
        soma += math.pow( abs(v1[i] - v2[i]), q )
    
    return math.pow(soma, q)

# distância Manhattan
def disManhattan(v1, v2):
    
    dim = len(v1)
    soma = 0

    for i in range(dim -1):
        soma += abs(v1[i] - v2[i])
    
    return max(soma)

def knn(aTreino, novaAmostra, k, q):

    tamTreino = len(aTreino)
    dist = {}

    for i in range(tamTreino):
        d = disMinkowski(aTreino[i], novaAmostra, q)
        dist[i] = d

    kVizinhos = sorted(dist, key= dist.get) [:k]

    qtdSetosa = 0
    qtdVersicolor = 0
    qtdVirginica = 0

    for indice in kVizinhos:
        if aTreino[indice][-1] == 'Iris-setosa':
            qtdSetosa += 1
        elif aTreino[indice][-1] == 'Iris-versicolor':
            qtdVersicolor += 1
        else:
            qtdVirginica += 1
    
    a = [qtdSetosa,qtdVersicolor,qtdVirginica]
    elemento = a.index(max(a)) + 1

    if(elemento == 1):
        return [1 , 'Iris-setosa']
    if(elemento == 2):
        return [2 ,'Iris-versicolor']
    if(elemento == 3):
        return [3 ,'Iris-virginica']
    
    return None

def MetricasAvaliacao(result):

    classesConjunto = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'] 
    for i in range( len(classesConjunto)):

        fp = 0
        fn = 0
        vp = 0 
        vn = 0 
        
        for res in result:
            hit = False
        
            if (classesConjunto[i] == res[0] and classesConjunto[i] == res[2]):
                hit = True
            if (classesConjunto[i] != res[0] and classesConjunto[i] != res[2]):
                hit = True

            if hit:
                if(res[2] == classesConjunto[i]):
                    vp += 1
                else:
                    vn += 1
            else:
                if(res[2] == classesConjunto[i]):
                    fn += 1
                else:
                    fp += 1

        acuracia = ( (vp+vn) / (vp+vn+fp+fn) )*100 #taxa de acerto
        sensibilidade = ( vp / (vp+fn))*100 
        especificidade = ( vn / (vn+fp))*100 

        print('Estatísticas do Algoritmo')
        print('Verdadeiros positivos {}'.format(vp))
        print('Verdadeiros Negativos {}'.format(vn))
        print('Falso Positivo {}'.format(fp))
        print('Falso Negativo {}'.format(fn))
        print('classe : {}'. format(classesConjunto[i]))
        print('Acurácia: {:.2f}%'.format(acuracia))
        print('Sensibilidade: {:.2f}%'.format(sensibilidade))
        print('Especificidade: {:.2f}%'.format(especificidade))
        print('\n')

# Obter o dataset 
#   150 amostras e 5 colunas:
#       comprimento e largura de sépalas, comprimento e larguras de petálas, classe da flor
#   3 classes:
#       iris-setosa, iris-versicolor e iris-virginica

#Pré- processamento dos dados
database = lerDatabase('Algortimo_KNN_Implementação/iris.data')

databaseNomalizado = normalizaConjunto(database)
print(databaseNomalizado)
#inserir o valor do percentual, retorno, conunto teste e treino
treino, teste = testeTreino(databaseNomalizado,0.3)

K = 3
resultado = []
q = 1
outTeste = 0
outKnn = 0

for amostra in teste:

    if(amostra[-1] == 'Iris-setosa'):
        outTeste = 1
    if( amostra[-1] == 'Iris-versicolor'):
        outTeste = 2
    if(amostra[-1] == 'Iris-virginica'):
        outTeste = 3

    outKnn, classe = knn(treino, amostra, K, q)
    
    resultado.append([amostra[-1], outTeste , classe, outKnn])
    
MetricasAvaliacao(resultado)

        
