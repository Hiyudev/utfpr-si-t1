from libs.tsp import Node
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def clear_tables():
    """
    Limpa os arquivos de saida
    """

    try:
        import os

        for file in os.listdir("./output"):
            if file.endswith(".csv"):
                os.remove(os.path.join("./output", file))
    except Exception as e:
        print(f"Erro ao limpar os arquivos de saida: {e}")


def visualize_table(
    name,
    solutions: list[tuple[list[Node]]],
    best_solution: int,
    headers: list[str] = [],
) -> None:
    """
    Visualizes a table of solutions for the TSP problem.
    Each row represents a solution, and each column represents a node in the solution path.
    """

    # Prepare table data
    table_data = []
    for solution_data in solutions:
        solution = solution_data[0]

        weights: list[float] = []
        
        for i in range(len(solution) - 1):
            node = solution[i]
            next_node = solution[i + 1]
            node_next_weight_index = -1

            for j, neighbor in enumerate(node.neighbors):
                if neighbor == next_node:
                    node_next_weight_index = j
                    break

            neighbor, weight = node.neighbors[node_next_weight_index]
            weights.append(weight)

        num_nodes = len(solution)
        sum_weights = sum(weights)
        is_first_last_equal = solution[0] == solution[-1]

        solution_set_length = len(set(solution))
        if is_first_last_equal:
            solution_set_length += 1

        had_repeated_nodes = len(solution) != is_first_last_equal
        # Calcula a porcentagem em relacao a melhor solucao, quanto menor, melhor (sendo 0, é igual a melhor solucao)
        percentage_of_best = ((sum_weights - best_solution) / best_solution) * 100

        other_data = solution_data[1:] if len(solution_data) > 1 else []

        table_data.append(
            [
                num_nodes,
                sum_weights,
                had_repeated_nodes,
                is_first_last_equal,
                percentage_of_best,
                *other_data,
            ]
        )

    column_labels = [
        "Numero de nos",
        "Soma dos pesos",
        "Houve nos repetidos?",
        "O primeiro e o ultimo no sao iguais?",
        "Porcentagem em relacao a melhor solucao (em %)",
        *headers,
    ]

    # Create DataFrame
    df = pd.DataFrame(table_data, columns=column_labels)
    df.to_csv(f"./output/{name}_data.csv", index=False)

    print(f"Dados para o problema {name} salvos em {name}_data.csv")


def visualize_graph(graph: nx.Graph, solution: list[Node]):
    """
    Visualiza a solucao do problema do caixeiro viajante
    """

    vanity_graph = nx.Graph()
    for i, node in enumerate(graph.nodes()):
        vanity_graph.add_node(i)

    for i, node in enumerate(graph.nodes()):
        closest_nodes = sorted(
            graph.neighbors(node), key=lambda x: graph[node][x]["weight"]
        )

        for j in range(1, len(closest_nodes)):
            # Verifica se o no sao os mesmos
            if closest_nodes[j] == node:
                continue

            vanity_graph.add_edge(
                i, closest_nodes[j], weight=graph[node][closest_nodes[j]]["weight"]
            )

    pos = nx.spring_layout(vanity_graph, scale=50)

    plt.figure()
    plt.title("TSP Solution")

    visualizing_nodes: list[Node] = [node.id for node in solution]
    mapped_edge_list = list(nx.utils.pairwise(visualizing_nodes))

    nx.draw_networkx_edges(vanity_graph, pos, edge_color="blue", width=0.2)
    nx.draw_networkx(
        graph,
        pos,
        with_labels=True,
        edgelist=mapped_edge_list,
        edge_color="red",
        width=1,
    )

    plt.show()
