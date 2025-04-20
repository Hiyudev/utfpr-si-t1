from random import random, sample
from numpy import exp, isclose
from libs.utils import get_total_distance


def funcao_tempo_temperatura(
    t: int, n: int, temperatura_inicial, temperatura_final
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


def funcao_objetivo(nodes: list[list[int]], order: list[int]) -> float:
    """
    Funcao que calcula o valor da funcao objetivo
    """

    # Calcula o custo total da solucao
    score = get_total_distance(nodes, order)
    return score


def tempera_simulada(nodes: list[list[int]], parameters: dict[str, int]):
    # Instancia dos parametros
    max_time = parameters["tempo_maximo"]
    temperatura_inicial = parameters["temperatura_inicial"]
    temperatura_final = parameters["temperatura_final"]

    # Instancia inicial, que e uma solucao aleatoria
    # Adiciona o primeiro elemento no final para fechar o ciclo
    solution_order = sample(range(0, len(nodes)), len(nodes))

    best_solution_order = solution_order.copy()
    best_solution_time = 0

    current_solution_order = solution_order.copy()

    # Instancia maxima de tempo
    time = 0
    temperatura = funcao_tempo_temperatura(
        time, max_time, temperatura_inicial, temperatura_final
    )

    while not (isclose(temperatura, 0, rtol=1e-3)) and time < max_time:
        # Calcula a temperatura
        temperatura = funcao_tempo_temperatura(
            time, max_time, temperatura_inicial, temperatura_final
        )

        # Se a temperatura for 0, encerra o loop
        if isclose(temperatura, 0, rtol=1e-3):
            break

        # Faz uma copia da solucao atual
        temp_solution = current_solution_order.copy()
        # Troca dois elementos aleatorios
        i, j = sample(range(0, len(nodes)), 2)
        temp_solution[i], temp_solution[j] = (temp_solution[j], temp_solution[i])

        # Calcula delta da funcao objetivo
        delta = funcao_objetivo(nodes, temp_solution) - funcao_objetivo(
            nodes, current_solution_order
        )

        # Calcula a probabilidade de aceitar a nova solucao
        probabilidade = exp(-delta / temperatura)

        if delta < 0 or probabilidade > random():
            # Se a solucao e melhor OU a probabilidade e maior que um numero aleatorio
            current_solution_order = temp_solution.copy()
            current_solution_time = time

        sum_of_current_solution = funcao_objetivo(nodes, current_solution_order)
        sum_of_best_solution = funcao_objetivo(nodes, best_solution_order)

        if sum_of_current_solution < sum_of_best_solution:
            best_solution_order = current_solution_order.copy()
            best_solution_time = time

        time += 1

    return (best_solution_order, best_solution_time)
