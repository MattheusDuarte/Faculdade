import numpy as np 
import matplotlib.pyplot as plt

#Divisão de conjuntos
def testeTreino(file, perc):

    file2 = np.array(file)

    [ linha, coluna ] = file2.shape
    lTreino = int(linha*perc)
    lTeste = linha - lTreino
    treino = np.zeros((lTreino, coluna))
    teste = np.zeros((lTeste, coluna))
    
    conjSetosa, conjVersicolor, conjVirginica = subConjuntos(file2)

    lim = int(len(conjSetosa)*perc)
    
    treino[0:lim] = conjSetosa[0:lim]
    treino[lim:(lim*2)] = conjVersicolor[0:lim]
    treino[(lim*2):(lim*3)] = conjVirginica[0:lim]

    lim1 = len(conjSetosa) - lim
    
    teste[0:lim1] = conjSetosa[lim: len(conjSetosa)]
    teste[lim1:(lim1*2)] = conjVersicolor[lim: len(conjVersicolor)]
    teste[(lim1*2):(lim1*3)] = conjVirginica[lim: len(conjVirginica)]

    return [treino, teste]

#separação de carcateristicas
def dataXY (file):

    labels = np.array(list(set(file[1:,-1])))#['Iris-setosa' 'Iris-virginica' 'Iris-versicolor']
    xData = np.zeros((len(file),len(file[0])-1))#x_data são os dados para treino.
    yData = np.empty(len(file))#y_data são as classe alvo.
    
    for x in range(0,len(file)):

        xData[x] = file[x][:-1]#Armazeno em x_data apenas os dados .

        for y in range(len(labels)):#dou um for na variavel labels

            if labels[y] in file[x]:#avalio qual classe esta contida na linha
                yData[x] = y#Substituo a string por um float no caso 0 ou 1
    
    return [xData, yData]
    
# tratamento dos dados
def open_file(path):#retorno x_data = dados tratados, y_data = classe das flores 
    
    data = []
    with open(path, 'rt') as dataset:

        for linha in dataset.readlines():
            a=linha.replace('\n','').split(',')
            data.append(a)
        
        for i in range( len(data) ):
            for j in range(4):
                data[i][j] = float(data[i][j])
            
            if data[i][-1] == 'Iris-setosa':

                data[i][-1] = 1

            if data[i][-1] == 'Iris-versicolor':

                data[i][-1] = 2
                

            if data[i][-1] == 'Iris-virginica':

                data[i][-1] = 3
    
    return data

#Transformação de sub conjuntos
def subConjuntos(file):

    setosa = []
    versicolor = []
    virginica = []

    setosa = file[0:50]
    versicolor = file[50:100]
    virginica = file[100:150]

    return [setosa, versicolor, virginica]

#Maximo e minimo da coluna 
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

#Normalização dos dados
def normalizaConjunto(conjunto):
    
    x = 0

    copiaConjunto = conjunto.copy()

    for i in range(4):

        maxValor, minValor = maxMinColuna(i, conjunto)
        
        for j in range( len(conjunto) ):
            x = round( -1 + (2*(conjunto[j][i] - minValor)/(maxValor - minValor)) , 2)
            copiaConjunto[j][i] = x

    return copiaConjunto

def funcaoDegrau(num):
    return 1.0 if (num > 0) else 0.0

#Stochastic Gradient Descent, SGD
def perceptron(X, Y, taxAprend):#perceptron Utilizando SGD

    X = np.insert(X[:,],len(X[0]),1,axis=1)
    #inicializando os pesos com 0 
    w = np.zeros(len(X[0])) #crio um array de zeros
    
    for l in range(len(X[0])):#adicionar pessos aleatorios
        w[l] = 1

    eta = taxAprend #taxa de aprendizado(Dar prferências a valores menores) mais precisa 0.01 ou 0.001
    epochs = len(X)
    errors = [] #armazena quantos valores são classificados erroneamente por cada interação

    for epoch in range(epochs):
        
        #variavel para armazenar os classificado incorretamente
        totalError = 0

        #loop para cada evento
        for i in range(len(X)):

            #calcula a predição/Hipotese
            wConv = w.astype(float)
            a = np.dot(X[i] ,wConv)

            output =funcaoDegrau(a)#saida

            #atualizo pesos
            if (output != Y[i]): 
                
                erroIt = Y[i] - output
                w += eta*X[i]*erroIt #pesos atualizados
                totalError += output

        errors.append(totalError*-1)
    
    return [w, errors]

def saidaY(file, tipo):

    y_data = np.empty(len(file))

    for i in range(len(file)):

        if(file[i] == tipo):
            y_data[i] = 1
        else:
            y_data[i] = 0
    
    return y_data

def avaliacaoPerceptron(X, Y, w):

    #X -> conjunto de amostras
    # Y -> valores reais 
    # w -> pesos
    # labels[1,0]
    
    if len(X) != len(Y):
         return None
    
    # considerando a primeira classe como a positiva, e a segunda a negativa
    classe_positiva = 1
    classe_negativa = 0

    # valores preditos corretamente
    vp = 0 
    vn = 0
    # valores preditos incorretamente 
    fp = 0
    fn = 0
    
    X = np.insert(X[:,],len(X[0]),1,axis=1)
    preditos = np.zeros(len(X))

    for i in range(len(X)):

        resultado = np.dot(X[i], w)
        valorPredito = funcaoDegrau(resultado)
        preditos[i] = valorPredito

    for (indice, v_real) in enumerate(Y):
        v_predito = preditos[indice]

        if v_real == classe_positiva:
            vp += 1 if v_predito == v_real else 0
            fp += 1 if v_predito != v_real else 0
        else:
            vn += 1 if v_predito == v_real else 0
            fn += 1 if v_predito != v_real else 0

    
    acuracia = ( (vp+vn) / (len(X)) )*100 #taxa de acerto
    sensibilidade = ( vp / (vp+fn))*100 
    especificidade = ( vn / (vn+fp))*100 

    print('Estatísticas do Algoritmo')
    print('Verdadeiros positivos {}'.format(vp))
    print('Verdadeiros Negativos {}'.format(vn))
    print('Falso Positivo {}'.format(fp))
    print('Falso Negativo {}'.format(fn))
    print('Acurácia: {:.2f}%'.format(acuracia))
    print('Sensibilidade: {:.2f}%'.format(sensibilidade))
    print('Especificidade: {:.2f}%'.format(especificidade))
    print('\n')

    return preditos
        
def juntarConjuntos(A1, A2):

    if(len(A1) != len(A2)):
        return None

    matriz = np.zeros((2, len(A1)))
    
    for i in range(len(A1)):
        matriz[0] = A1
        matriz[1] = A2
    #matriz = np.concatenate(( A1, A2 ), axis= 0)
    return matriz.T  
#Carrega Banco de Dados
database = open_file('Algortimo_KNN_Implementação/iris.data')

#Normalizar o Banco
databaseNorm = normalizaConjunto(database)

#Divisão da amostra entre treino e teste
treino, teste = testeTreino(databaseNorm,0.4)

xTreino , yTreino = dataXY(treino)#conjunto de Treino
xTeste , yTeste = dataXY(teste) #conjuntos de teste

############ IRIS-SETOSA######################################
print('classe : Iris-setosa ')

yTreino_modificado = saidaY(yTreino, 0)
yTeste_modificado = saidaY(yTeste,0)
w, pErrror = perceptron(xTreino, yTreino_modificado,0.01 )
setosaPredicao = avaliacaoPerceptron(xTeste, yTeste_modificado, w)

############ IRIS-VERSICOLOR######################################
print('classe : Iris-versicolor ')

yTreino_modificado = saidaY(yTreino, 1)
yTeste_modificado = saidaY(yTeste,1)
w, pErrror = perceptron(xTreino, yTreino_modificado,0.01 )
irisVersicolor = avaliacaoPerceptron(xTeste, yTeste_modificado, w)

############ IRIS-VIRGINICA######################################
print('classe : Iris-virginica ')

yTreino_modificado = saidaY(yTreino, 2)
yTeste_modificado = saidaY(yTeste,2)
w, pErrror = perceptron(xTreino, yTreino_modificado,0.01 )
virginicaPredicao = avaliacaoPerceptron(xTeste, yTeste_modificado, w)


############ IRIS-VERSICOLOR 2.0 ######################################

print('classe : Iris-versicolor 2.0')
inVirginica = juntarConjuntos(setosaPredicao,virginicaPredicao)
yTreino_modificado = saidaY(yTreino, 1)
print(yTreino_modificado)
yTeste_modificado = saidaY(yTeste,1)
print(yTeste_modificado)
w, pErrror = perceptron(inVirginica, yTreino_modificado,0.01 )
print(w)
versicolorPredicao = avaliacaoPerceptron(inVirginica, yTeste_modificado, w)
print(versicolorPredicao)