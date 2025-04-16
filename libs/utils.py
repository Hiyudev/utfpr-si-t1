def get_total_distance(nodes: list[list[int]], ordem: list[int]) -> float:
    """
    Funcao que calcula o custo total de uma solucao. Lembrando que a ordem não necessita que a última seja igual a primeira.

    nodes: matriz de adjacencia
    ordem: ordem dos pontos a serem visitados.
    """

    custo_total = 0.0

    for i in range(len(ordem) - 1):
        # Adiciona o custo entre os dois pontos
        custo_total += nodes[ordem[i]][ordem[i + 1]]

    # Adiciona o custo entre o ultimo ponto e o primeiro
    custo_total += nodes[ordem[-1]][ordem[0]]

    return custo_total


def get_weights(nodes: list[list[int]], ordem: list[int]) -> list[float]:
    """
    Funcao que calcula o custo total de uma solucao. Lembrando que a ordem não necessita que a última seja igual a primeira.

    nodes: matriz de adjacencia
    ordem: ordem dos pontos a serem visitados.
    """

    custo_total = []

    for i in range(len(ordem) - 1):
        # Adiciona o custo entre os dois pontos
        custo_total.append(nodes[ordem[i]][ordem[i + 1]])

    # Adiciona o custo entre o ultimo ponto e o primeiro
    custo_total.append(nodes[ordem[-1]][ordem[0]])

    return custo_total
