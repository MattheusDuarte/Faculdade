from math import sqrt
from copy import deepcopy
import time
from random import uniform, randint, random, shuffle
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

class State:
    def __init__(self, antenas, residentes):
        self.raio = 6
        self.antenas = antenas
        self.residentes = residentes
        self.f = objetivo( self.raio ,antenas, residentes)
  
def foiAnalisado(residencia, analisado):
    for cliente in analisado:

        if(residencia == cliente):
            return True
    return False

def objetivo(raio, antenas, residentes):
    vet_analisados = []
    for antena in antenas:
        for residente in residentes: 

            if not foiAnalisado(residente, vet_analisados):
                #os pontos A(xA, yA) e B (xB, Yb)
                #dAB² = (xB – xA)² + (yB – yA)²
                d = sqrt(pow((residente[0] - antena[0]), 2) + pow((residente[1] - antena[1]), 2))
                if (d <= raio):
                    vet_analisados.append(residente)
    return len(vet_analisados)

def residentesInicial(tamPopulacao, limite):
    n_Residentes = tamPopulacao/2
    vet_residentes = [] 
    for m in range(int(n_Residentes)):

        p = (uniform(-limite, limite), uniform(-limite, limite))
        vet_residentes.append(p)
    return vet_residentes

def estadoInicial(numAntena, limite, residentes):
    vet_antenas = []  
    for n in range(numAntena):

        p = (uniform(-limite, limite), uniform(-limite, limite))
        vet_antenas.append(p)

    return State( vet_antenas, residentes)


def showState(s, limite, titulo):
    print('>>>>>', titulo, '<<<<<')
    print('Pessoas conectadas = ', s.f)
    patches = []

    for antena in s.antenas:
        patches.append(plt.Circle(antena, s.raio))

    fig, ax = plt.subplots()
    ax.cla()
    ax.set_xlim((-limite, limite))
    ax.set_ylim((-limite, limite))
    ax.set_aspect('equal')

    p = PatchCollection(patches, color='b', alpha=0.2)
    ax.add_collection(p)

    plt.scatter(*zip(*s.residentes), c='black', s=5)
    plt.scatter(*zip(*s.antenas), c='k', marker='x', s=15)
    plt.grid(linestyle='--', linewidth=0.5)
    plt.title(titulo)
    plt.xlabel('$Eixo$ $X$')
    plt.ylabel('$Eixo$ $Y$')
    plt.legend(['residentes', 'antenas'],
               bbox_to_anchor=(0.982, 1), frameon=False)
    plt.text(21.4, 12.5, '- Cobertos = ' + str(s.f))
    fig.savefig(titulo+'.png')
    plt.show()
    
def sucessor(s):
    lista = deepcopy(s.antenas)
    k = randint(0, (len(lista)-1))
    (x, y) = lista[k]

    a = uniform(-20, 20)
    b = uniform(-20,20)
    lista[k] = (a, b)

    return State( lista, s.residentes)

def escolher(set):

    x = set[randint(0, len(set) - 1)]
    y = set[randint(0, len(set) - 1)]

    if(x.f > y.f):
        return x
    return y

#para 6 antenas demorou 1h e não encotrou resultado
def cruzamento2(x,y):

    antena1 = deepcopy(x.antenas)
    antena2 = deepcopy(y.antenas)
    proxima_antena=[]
    shuffle(antena1)
    shuffle(antena2)
    for i in range(len(x.antenas)):

        
        proxima_antena.append(antena1[i])
        proxima_antena.append(antena2[i])
    
    shuffle(proxima_antena)

    return State( proxima_antena, x.residentes)

def cruzamento(x, y): 
    antena1 = deepcopy(x.antenas)
    antena2 = deepcopy(y.antenas)
    proxima_antena = []
    #quadro de punnet x[i] + x[i+1]
                    # y[i] + y[i+1]
    for i in range(len(x.antenas)):

        if ((randint(0, 1) % 2 == 0)):
            proxima_antena.append(antena1[i])
        else:
            proxima_antena.append(antena2[i])

    return State( proxima_antena, x.residentes)


def mutacao(s):
    #valor adaptativo compara a capacidade que os portadores de uma mutação têm de transmiti-la 
    # à geração seguinte, com a capacidade que os não-portadores dessa mutação têm em transmitir 
    # o alelo mais antigo
    estadoAtual = s
    valor_adaptativo = 0.375
    #vizinhança
    for i in range( len(s.residentes) * int(1/5)):

        if (uniform(0.0, 1.0) > valor_adaptativo):
            estadoMutação = sucessor(s)
        if(estadoMutação.f > estadoAtual.f):
            estadoAtual = estadoMutação

        ##possivel implementação é verificar se alguma antenna bate com a outra 
    return estadoAtual

tamanho_Populacao = 100 # MUDAR AQUI
numero_Geracoes = 2 * tamanho_Populacao
numero_Antenas = 5
limite = 1/5 * tamanho_Populacao
residentes = [(-3.201778581003765, -18.500944995695594), (19.545648904154724, 4.433240093881491), 
            (-15.62738671946887, 14.55347110349846), (17.25740126659513, -3.2566836563722923), 
            (-9.245288224107494, 6.910428788684399), (-11.976599913896827, -13.623761522380708), 
            (-9.157584311139164, -10.872430028439553), (-0.6879204464676327, -9.319378890778257), 
            (-18.839851092236888, 19.037774925213036), (-8.873576992283812, 3.738727140095179), 
            (6.851896617319429, -13.88040073259667), (13.62463246958766, -6.025183237796497), 
            (13.134229752272965, -13.774517222962643), (10.580141837953555, 1.6640240658373706), 
            (-5.534844671123192, 14.589113481147749), (12.095208642782517, -11.890420180842547), 
            (-18.96512820107675, 4.134693017038472), (-3.406757413566261, 4.492205096518131),
            (9.17116859960742, -2.2677633221882516), (2.022725168815228, 11.358187178859819), 
            (-12.404404598894798, 17.942195056983323), (-5.396144321155836, -10.072078655191694), 
            (16.891265444585372, 6.840042704981197), (2.431582715917898, 12.072827451149173), 
            (-17.439566615760008, -3.467633426755686), (-5.369732504466915, 0.7442045389460645), 
            (-11.537069000224026, -18.131318762044316), (-13.55569963495828, -6.27504185353108), 
            (-2.755497931327433, -15.043836738684163), (-2.766863145928049, -17.88105319808441), 
            (-12.01602400972873, -10.85445791160662), (4.407618317602822, -6.416444313778369), 
            (-9.715939569078538, -0.3494474542380921), (3.7084530486853673, -18.392321124128706), 
            (10.175926747635849, 0.8627304208050823), (-16.4752039197829, -2.648627276042596), 
            (-15.22891325744698, 10.575604890261317), (-13.15085139222373, 6.716730727484315), 
            (-7.701826304684651, 10.800387180140358), (-13.330844589523604, -17.54663893780668), 
            (15.15980378375771, -13.005939500591715), (-11.273279312825096, 11.572783035023882), 
            (3.2592237455596127, 9.532663691971916), (-0.1600711958458234, 2.581809733832582), 
            (14.308852453043528, -17.25590275991462), (-5.730672930243417, 12.049760659043102), 
            (-5.51312626626672, -17.87561343718288), (-18.884891503508598, -3.638895943425169), 
            (-4.17551479818178, -13.426772512881922), (-6.155354098120785, -8.864917631377693)]
#residentes = residentesInicial(tamanho_Populacao, limite)
geracao_Atual = []
for i in range(tamanho_Populacao):
    geracao_Atual.append(estadoInicial(numero_Antenas, limite, residentes))

melhor = geracao_Atual[0]
w=[]
showState(melhor, limite, "Genetico (Antes)")
w.append(melhor.f)

start = time.time()

for i in range(numero_Geracoes):
    proxima_gen = []

    for j in range(tamanho_Populacao):

        x = escolher(geracao_Atual)
        y = escolher(geracao_Atual)
        filho = cruzamento(x, y)
        filho = mutacao(filho)
        proxima_gen.append(filho)

    geracao_Atual = proxima_gen

melhor = geracao_Atual[0]
for s in geracao_Atual:
    w.append(melhor.f)
    if(s.f > melhor.f):
        melhor = s

end = time.time()

showState(melhor, limite, "Genetico (Depois)")
print(end - start)

plt.figure(figsize=(12, 8))
plt.title('Genético')
plt.xlabel('$Iterações$')
plt.ylabel('$Clientes$')
plt.plot(w)
plt.show()

