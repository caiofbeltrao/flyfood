def gerarArranjos(lista, r=None):
    pool = tuple(lista)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    ciclos = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            ciclos[i] -= 1
            if ciclos[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                ciclos[i] = n - i
            else:
                j = ciclos[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def menorCaminho(lista_cobmbinacoes,lista_coordenadas, lista_vazia):
    menor_caminho = 0
    i = 0
    j = 0
    temp = 0
    for c in range(0,len(lista_cobmbinacoes)):
        for d in range(0,len(lista_cobmbinacoes[c])-1):
            while (lista_coordenadas[i][0] != lista_cobmbinacoes[c][d]):
                i += 1
            while (lista_coordenadas[j][0] != lista_cobmbinacoes[c][d+1]):
                j += 1
            a = lista_coordenadas[i][1]
            b = lista_coordenadas[j][1]
            x = lista_coordenadas[i][2]
            y = lista_coordenadas[j][2]
            temp = temp + (abs(a-b) + abs(x-y))
            i = j = 0
        if(menor_caminho == 0):
            lista_vazia = lista_cobmbinacoes[c]
            menor_caminho = temp
        elif(temp < menor_caminho):
            menor_caminho = temp
            lista_vazia = lista_cobmbinacoes[c]
        temp = 0
    print(lista_vazia, menor_caminho)


lista_nova = []
matriz = []
tamanho_matriz = input("").split()
locais = []

for c in range(0,int(tamanho_matriz[0])):
    matriz.append([])
    for d in range(0,int(tamanho_matriz[1])):
        matriz[c].append(0)

while True:
    pontos = [str(i) for i in input().split()]
    if pontos:
        nome = pontos[0].upper()
        locais.append(nome)
        x = int(pontos[1])
        y = int(pontos[2])
        matriz[x-1][y-1] = nome
    else:
        break

ponto_de_partida = str(input("")).upper()
locais.remove(ponto_de_partida)

arranjo = list(gerarArranjos(locais,len(locais)))

listagem = []

for item in arranjo:
    listagem.append(list(item))

for item in listagem:
    item.append(ponto_de_partida)
    item.insert(0,ponto_de_partida)

posicoes = []

for c in range(0,len(matriz)):
    for d in range(0,len(matriz[c])):
        for e in range(0,len(listagem)):
            for f in range(0,len(listagem[e])):
                if len(posicoes) == 0:
                    if matriz[c][d] == listagem[e][f]:
                        posicoes.append([matriz[c][d],c+1,d+1])
                else:
                    if (matriz[c][d] == listagem[e][f]) and ([matriz[c][d],c+1,d+1] not in posicoes):
                        posicoes.append([matriz[c][d],c+1,d+1])

menorCaminho(listagem,posicoes,lista_nova)