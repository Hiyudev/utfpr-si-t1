import numpy as np
from random import sample, randint
from libs.tsp import Node
from libs.utils import get_total_distance, formalize_solution

def funcao_adaptacao(geracao: list[tuple[list[int], float]]):
    scores = []
    for solucao, custo in geracao:
        score = 1 / (1 + custo)
        scores.append(score)

    probabilidades = [(score / sum(scores)) for score in scores]
    return probabilidades


def seleciona_pais(probs):
    indices_escolhidos = np.random.choice(
        len(probs), 2, replace=False, p=np.array(probs)
    )
    return indices_escolhidos


def func_reproducao(
    nodes, ordem_s1: list[int], ordem_s2: list[int]
) -> tuple[list:int, float]:
    # Ordem se refere a ordem de visita das cidades - uma parte da solucao (ordem, custo)
    ponto_cruzamento = randint(1, len(ordem_s1) - 1)
    nova_ordem = ordem_s1[:ponto_cruzamento]

    for cidade in ordem_s2:
        if cidade not in nova_ordem:
            nova_ordem.append(cidade)

    custo = get_total_distance(nodes, nova_ordem)
    return (nova_ordem, custo)


def mutacao(nodes: list[Node], solucao: tuple[list:int, float]):
    ordem = solucao[0][:]
    i1, i2 = sample(range(len(ordem)), 2)
    ordem[i1], ordem[i2] = ordem[i2], ordem[i1]
    custo = get_total_distance(nodes, ordem)
    return (ordem, custo)


def crossover(nodes: list[Node], geracao: list[tuple[list[int], float]], probs: list):
    nova_geracao = []
    for i in range(len(geracao)):
        indices_escolhidos = seleciona_pais(probs)

        # Ordem de visita dos pais selecionados
        ordem_s1 = geracao[indices_escolhidos[0]][0]
        ordem_s2 = geracao[indices_escolhidos[1]][0]

        nova_solucao = func_reproducao(nodes, ordem_s1, ordem_s2)

        if randint(1, 100) == 1:
            # print("Função mutação!!!")
            nova_solucao = mutacao(nodes, nova_solucao)

        nova_geracao.append(nova_solucao)

    return nova_geracao





def algoritmo_genetico(nodes: list[Node], tam_populacao: int, n_geracoes: int):
    n_cidades = len(nodes)
    populacao_inicial: list[tuple[list[int], float]] = []

    # Criando a populacao inicial de solucoes (estados)
    for i in range(tam_populacao):
        ordem_aleatoria = sample(range(0, n_cidades), n_cidades)

        # Solucao = (ordem de visita, custo total)
        solucao: tuple[list[int], float] = [
            ordem_aleatoria,
            get_total_distance(nodes, ordem_aleatoria),
        ]
        populacao_inicial.append(solucao)

    geracao = populacao_inicial

    melhor_solucao = min(geracao, key=lambda x: x[1])

    # Gerações são um conjunto de tam_populacao de soluções
    for i in range(n_geracoes):
        probabilidades = funcao_adaptacao(geracao)
        nova_geracao = crossover(nodes, geracao, probabilidades)

        melhor_geracao = min(geracao, key=lambda x: x[1])

        if melhor_geracao[1] < melhor_solucao[1]:
            melhor_solucao = melhor_geracao

        geracao = nova_geracao

    print(melhor_solucao)
    nodes_solucao_final = formalize_solution(nodes, melhor_solucao[0])
    return (nodes_solucao_final,)
