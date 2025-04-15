from random import random, sample
from math import exp, isclose
from libs.tsp import Node
from libs.utils import get_total_distance, formalize_solution


def funcao_tempo_temperatura(
    t: int, n: int, temperatura_inicial=100, temperatura_final=5
) -> float:
    """
    Funcao que calcula a temperatura em funcao de um dado tempo

    t: Tempo atual
    n: Tempo maximo
    temperatura_inicial
    temperatura_final
    """

    temperatura = temperatura_final + (temperatura_inicial - temperatura_final) * pow(
        (n - t) / n, 2
    )

    return temperatura


def funcao_objetivo(nodes: list[Node], order: list[int]) -> float:
    """
    Funcao que calcula o valor da funcao objetivo
    """

    # Calcula o custo total da solucao
    score = get_total_distance(nodes, order)

    return score


def tempera_simulada(nodes: list[Node], max_t: int):
    # Instancia inicial, que e uma solucao aleatoria
    solution = sample(range(0, len(nodes)), len(nodes))
    last_solution = solution

    # Instancia maxima de tempo
    t = 0
    temperatura = funcao_tempo_temperatura(t, max_t)

    while temperatura != 0 and t < max_t:
        # Calcula a temperatura
        temperatura = funcao_tempo_temperatura(t, max_t)

        # Se a temperatura for 0, encerra o loop
        if isclose(temperatura, 0, rel_tol=1e-3):
            break

        # Constroi uma nova solucao (sucessor) aleatoria
        temp_solution = last_solution.copy()
        p1, p2 = sample(range(len(nodes)), 2)
        temp_solution[p1], temp_solution[p2] = (
            temp_solution[p2],
            temp_solution[p1],
        )

        # Calcula delta da funcao objetivo
        delta = funcao_objetivo(nodes, temp_solution) - funcao_objetivo(
            nodes, last_solution
        )

        # Calcula a probabilidade de aceitar a nova solucao
        probabilidade = exp(delta / temperatura)

        if delta <= 0 or probabilidade > random():
            # Se a solucao e melhor OU a probabilidade e maior que um numero aleatorio
            last_solution = temp_solution.copy()

        t += 1

    formal_solution = formalize_solution(nodes, last_solution)
    return (formal_solution, t)
