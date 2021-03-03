import random
import operator
import matplotlib.pyplot as plt

random.seed(42)


# Cria a classe que vai guardar os pontos de entrega

class Cidade:
    def __init__(self, nome, x, y):
        self.nome = nome
        self.x = x
        self.y = y

    def distancia(self, Cidade):
        xDis = abs(self.x - Cidade.x)
        yDis = abs(self.y - Cidade.y)
        distancia = xDis+yDis
        return distancia

    def __repr__(self):
        return f'({str(self.nome)})'


# Criando uma classe fitness

class Fitness:
    def __init__(self, rota):
        self.rota = rota
        self.distancia = 0
        self.fitness = 0.0

    def rotadistancia(self):
        if self.distancia == 0:
            distanciaDaRota = 0
            for i in range(0, len(self.rota)):
                CidadeInicial = self.rota[i]
                ProximaCidade = None
                if i + 1 < len(self.rota):
                    ProximaCidade = self.rota[i + 1]
                else:
                    ProximaCidade = self.rota[0]
                distanciaDaRota += CidadeInicial.distancia(ProximaCidade)
            self.distancia = distanciaDaRota
        return self.distancia

    def rotaFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.rotadistancia())
        return self.fitness


# Criando a população inicial e Gerando as possiveis rotas

def criarRota(ListaDeCidades):
    rota = random.sample(ListaDeCidades, len(ListaDeCidades))
    return rota


# Criando a Primeira População com um tamanho especifico

def populacaoInicial(tamanhoDaPopulacaoInicial, ListaDeCidades):
    populacao = []

    for i in range(0, tamanhoDaPopulacaoInicial):
        populacao.append(criarRota(ListaDeCidades))
    return populacao


# Ordenando as rotas da população inicial de acordo com o seu fitness do maior pro menor
def rankrotas(populacao):
    fitnessResults = {}
    for i in range(0, len(populacao)):
        fitnessResults[i] = Fitness(populacao[i]).rotaFitness()
    rotasOrdenadas = sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)
    return rotasOrdenadas

# Calculando a média das distâncias em cada geração
def mediaDistanciaRotas(rotasOrdenadas):
    somatorio = 0
    for i in range(0,len(rotasOrdenadas)):
        somatorio += Fitness(rotasOrdenadas[i]).rotadistancia()
    return somatorio/len(rotasOrdenadas)


# Criando os metodos de seleção de reprodutores
# Torneio
def torneio(populacaoOrdenada, tamanhoElitismo):
    resultadoDaSelecao = []
    a = populacaoOrdenada[random.randint(0, len(populacaoOrdenada) - 1)]
    b = populacaoOrdenada[random.randint(0, len(populacaoOrdenada) - 1)]
    for i in range(0, tamanhoElitismo):
        resultadoDaSelecao.append(populacaoOrdenada[i][0])
    for i in range(0, len(populacaoOrdenada) - tamanhoElitismo):
        a = populacaoOrdenada[random.randint(0, len(populacaoOrdenada) - 1)][0]
        b = populacaoOrdenada[random.randint(0, len(populacaoOrdenada) - 1)][0]
        while b == a:
            b = populacaoOrdenada[random.randint(0, len(populacaoOrdenada) - 1)][0]
        if a >= b:
            resultadoDaSelecao.append(a)
        else:
            resultadoDaSelecao.append(b)
    return resultadoDaSelecao



def matingPool(populacao, resultadoDaSelecao):
    matingpool = []
    for i in range(0, len(resultadoDaSelecao)):
        index = resultadoDaSelecao[i]
        matingpool.append(populacao[index])
    return matingpool


# Criando função crossOver para gerar os filhos
# CrossOver Aleatório
def crossOver1(pai1, pai2):
    filho = []
    filhoP1 = []
    filhoP2 = []

    geneA = int(random.random() * len(pai1))
    geneB = int(random.random() * len(pai1))

    inicio = min(geneA, geneB)
    final = max(geneA, geneB)

    for i in range(inicio, final):
        filhoP1.append(pai1[i])

    filhoP2 = [item for item in pai2 if item not in filhoP1]
    filho = filhoP1 + filhoP2
    return filho

# CrossOver do tipo que parte na metade
def crossOver2(pai1, pai2):
    filho = []
    filhoP1 = []
    filhoP2 = []
    meio = len(pai1)//2
    for i in range(0, meio):
        filhoP1.append(pai1[i])
    filhoP2 = [item for item in pai2 if item not in filhoP1]
    filho = filhoP1 + filhoP2
    return filho


# Aplicando o crossOver em toda a população

def crossOverNaPopulacao(matingpool, tamanhoElitismo):
    filhos = []
    tamanho = len(matingpool) - tamanhoElitismo
    amostra = random.sample(matingpool, len(matingpool))

    for i in range(0, tamanhoElitismo):
        filhos.append(matingpool[i])

    for i in range(0, tamanho):
        filho = crossOver1(amostra[i], amostra[len(matingpool) - i - 1])
        filhos.append(filho)
    return filhos


# Função mutação em apenas um gene de uma unica rota
def mutar(individuo, taxaDeMutacao):
    for trocado in range(len(individuo)):
        if (random.random() < taxaDeMutacao):
            trocarCom = int(random.random() * len(individuo))

            Cidade1 = individuo[trocado]
            Cidade2 = individuo[trocarCom]

            individuo[trocado] = Cidade2
            individuo[trocarCom] = Cidade1
    return individuo


# Aplicando a mutação em toda a população

def mutarpopulacao(populacao, taxaDeMutacao):
    populacaoMutada = []

    for ind in range(0, len(populacao)):
        mutardInd = mutar(populacao[ind], taxaDeMutacao)
        populacaoMutada.append(mutardInd)
    return populacaoMutada


# Juntando todos os passos até agora

def proximaGeracao(geneAtual, tamanhoElitismo, taxaDeMutacao):
    populacaoOrdenada = rankrotas(geneAtual)
    resultadoDaSelecao = torneio(populacaoOrdenada, tamanhoElitismo)
    matingpool = matingPool(geneAtual, resultadoDaSelecao)
    filhos = crossOverNaPopulacao(matingpool, tamanhoElitismo)
    proximaGeracao = mutarpopulacao(filhos, taxaDeMutacao)
    return proximaGeracao



def algoritmoGenetico(populacao, tamanhoDaPopulacaoInicial, tamanhoElitismo, taxaDeMutacao, numeroDeGeracoes):
    pop = populacaoInicial(tamanhoDaPopulacaoInicial, populacao)
    distanciaDaMelhorRota = [1 / rankrotas(pop)[0][1]]
    media = [mediaDistanciaRotas(pop)]
    print(f'Ppulação inicial, Distância Inicial: {str(distanciaDaMelhorRota[0])}, Média: {float(media[0])}')

    for i in range(1, numeroDeGeracoes + 1):

        pop = proximaGeracao(pop, tamanhoElitismo, taxaDeMutacao)
        media.append(mediaDistanciaRotas(pop))
        distanciaDaMelhorRota.append(1 / rankrotas(pop)[0][1])
        print(f'Geração {str(i)}, Distância: {distanciaDaMelhorRota[i]}, Media: {media[i]}')

    bestrotaIndex = rankrotas(pop)[0][0]
    bestrota = pop[bestrotaIndex]

    plt.plot(distanciaDaMelhorRota)
    plt.ylabel('Distância')
    plt.xlabel('Geração')
    plt.title('Melhor Aptidão vs Geração')
    plt.tight_layout()
    plt.show()

    plt.plot(media)
    plt.ylabel('Média')
    plt.xlabel('Geração')
    plt.title('Média da Aptidão vs Geração')
    plt.tight_layout()
    plt.show()

    return bestrota

#Main

ListaDeCidades = []
nome_dos_pontos = []
numero_de_pontos = int(input('Quantos pontos: '))
for i in range(0, numero_de_pontos):
    cidade = input().split()
    nome_dos_pontos.append(str(cidade[0]))
    ListaDeCidades.append(Cidade(str(cidade[0]), int(cidade[1]), int(cidade[2])))
tamanho_da_pop_inicial = int(input('Tamanho da população inicial: '))
tamanho_do_elitismo = int(input('Tamanho do elitismo: '))
taxa_de_mutacao = float(input('Taxa de mutação: '))
numero_de_geracoes = int(input('Número de gerações: '))

best_rota = algoritmoGenetico(populacao=ListaDeCidades, tamanhoDaPopulacaoInicial=tamanho_da_pop_inicial, tamanhoElitismo=tamanho_do_elitismo, taxaDeMutacao=taxa_de_mutacao, numeroDeGeracoes=numero_de_geracoes)
print(best_rota)

x = []
y = []
for i in best_rota:
    x.append(i.x)
    y.append(i.y)
x.append(best_rota[0].x)
y.append(best_rota[0].y)
plt.plot(x, y, '--o')
plt.xlabel('X')
plt.ylabel('Y')
ax = plt.gca()
plt.title('Melhor Rota')
bbox_props = dict(boxstyle="circle,pad=0.3", fc='C0', ec="black", lw=0.5)
for i in range(1, len(ListaDeCidades) + 1):
    ax.text(ListaDeCidades[i - 1].x, ListaDeCidades[i - 1].y, nome_dos_pontos[i-1], ha="center", va="center", size=8, bbox=bbox_props)
plt.tight_layout()
plt.show()