from libs.tsp import Node


def get_node(nodes: list[Node], id: int) -> Node:
    for node in nodes:
        if node.id == id:
            return node


def get_total_distance(nodes: list[Node], ordem: list[int]) -> float:
    custo_total = 0.0

    for i in range(len(ordem) - 1):
        cidade_atual = get_node(nodes, ordem[i])

        for vizinho, custo in cidade_atual.neighbors:
            if vizinho.id == ordem[i + 1]:
                custo_total += custo
                break

    ultima_cidade = get_node(nodes, ordem[-1])

    for vizinho, custo in ultima_cidade.neighbors:
        if vizinho.id == ordem[0]:
            custo_total += custo
            break

    return custo_total


def formalize_solution(nodes: list[Node], order: list[int]):
    solution = []
    for id in order:
        solution.append(get_node(nodes, id))

    return solution
