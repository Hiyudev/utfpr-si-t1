from libs.tsp import Node
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def visualize_table(name, solutions: list[list[Node]], best_solution: int) -> None:
    """
    Visualizes a table of solutions for the TSP problem.
    Each row represents a solution, and each column represents a node in the solution path.
    """

    # Prepare table data
    table_data = []
    for solution in solutions:
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
        mean_weights = np.mean(weights)
        std_dev_weights = np.std(weights)
        variance_weights = np.var(weights)
        is_first_last_equal = solution[0] == solution[-1]

        solution_set_length = len(set(solution))
        if is_first_last_equal:
            solution_set_length += 1

        had_repeated_nodes = len(solution) != is_first_last_equal

        # Calculate percentage relative to the best solution
        percentage_of_best = (sum_weights / best_solution) * 100

        table_data.append(
            [
                num_nodes,
                sum_weights,
                mean_weights,
                std_dev_weights,
                variance_weights,
                had_repeated_nodes,
                is_first_last_equal,
                percentage_of_best,
            ]
        )

    column_labels = [
        "Numero de nos",
        "Soma dos pesos",
        "Media dos pesos",
        "Desvio padrao dos pesos",
        "Variancia dos pesos",
        "Houve nos repetidos?",
        "O primeiro e o ultimo no sao iguais?",
        "Porcentagem em relacao a melhor solucao",
    ]

    # Create DataFrame
    df = pd.DataFrame(table_data, columns=column_labels)
    df.to_csv(f"./output/{name}_data.csv", index=False)


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

    visualizing_nodes: list[Node] = []
    for i, node in enumerate(solution):
        visualizing_nodes.append(node)

        mapped_visualizing_nodes = [node.id for node in visualizing_nodes]
        mapped_edge_list = list(nx.utils.pairwise(mapped_visualizing_nodes))

        plt.clf()
        plt.title(f"TSP Solution - Step {i+1} of {len(solution)}")

        nx.draw_networkx_edges(vanity_graph, pos, edge_color="blue", width=0.2)
        nx.draw_networkx(
            graph,
            pos,
            with_labels=True,
            edgelist=mapped_edge_list,
            edge_color="red",
            width=1,
        )

        plt.draw()
        plt.waitforbuttonpress()

    plt.waitforbuttonpress()
    plt.close()
