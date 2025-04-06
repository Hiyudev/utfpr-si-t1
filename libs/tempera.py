from random import randint, random
from math import exp, log10
import numpy as np
from libs.tsp import Node


def funcao_tempo_temperatura(t: int) -> float:
    """
    Funcao que calcula a temperatura em funcao de um dado tempo
    """

    t /= 100
    temperatura = -log10(t + 0.1)

    # Limite
    if temperatura <= 0:
        return 0

    return temperatura


def funcao_objetivo(nodes: list[Node]) -> float:
    """
    Funcao que calcula o valor da funcao objetivo
    """

    score = len(nodes)

    # OBJETIVO 1: Nao pode ter nos repetidos
    diff = len(nodes) - len(set(nodes))
    if diff > 0:
        score = 0

    return score


def tempera_simulada(nodes: list[Node]):
    solution: list[Node] = []

    # Instancia inicial, que e um no aleatorio
    solution.append(nodes[randint(0, len(nodes) - 1)])
    last_node = solution[0]

    # Instancia maxima de tempo
    t = 0
    temperatura = funcao_tempo_temperatura(t)

    while temperatura != 0:
        # Calcula a temperatura
        temperatura = funcao_tempo_temperatura(t)

        if temperatura == 0:
            break

        # Escolhe um no vizinho aleatorio
        random_neighbor = last_node.neighbors[randint(0, len(last_node.neighbors) - 1)][
            0
        ]

        # Constroi uma nova solucao temporaria
        temp_solution = solution.copy()
        temp_solution.append(random_neighbor)

        # Calcula delta da funcao objetivo
        delta = funcao_objetivo(temp_solution) - funcao_objetivo(solution)

        probabilidade = exp(delta / temperatura)

        if delta >= 0 or probabilidade > random():
            # Se a solucao e melhor, aceita
            solution.append(random_neighbor)
            last_node = random_neighbor

        t += 1

    return solution
