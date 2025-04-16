import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from libs.utils import get_weights


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
    nodes: list[list[int]],
    solutions: list[tuple[list[int], int]],
    best_solution: int,
    headers: list[str] = [],
) -> None:
    """
    #Visualizes a table of solutions for the TSP problem.
    #Each row represents a solution, and each column represents a node in the solution path.
    """

    # Prepare table data
    table_data = []
    for solution_data in solutions:
        solution = solution_data[0]

        weights: list[float] = get_weights(nodes, solution)

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
