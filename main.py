import sys
from libs import tsp
from libs.tempera import tempera_simulada
from libs.visual import visualize_graph, visualize_table, clear_tables
from libs.genetico import algoritmo_genetico


def tempera():
    VISUALIZE = False
    REPEATED_TIME = 100
    LIMIT_DATA = (
        -1
    )  # -1 para pegar todos os dados, n (numero natural qualquer) pega os primeiros n dados

    tsp_datas = tsp.import_all_tsp_data("./assets", LIMIT_DATA)
    best_datas = tsp.import_all_tsp_solutions("./assets")

    # Limpa as tabelas da pasta "output"
    clear_tables()

    for tsp_name, tsp_info in tsp_datas.items():
        tsp_graph, tsp_data = tsp_info
        tsp_solution = best_datas[tsp_name]

        solutions: list[tuple[list[tsp.Node], int]] = []
        for i in range(REPEATED_TIME):
            MAXIMUM_ITERATIONS = len(tsp_data)
            solution = tempera_simulada(tsp_data, MAXIMUM_ITERATIONS)
            solutions.append(solution)

        # Visualiza as soluções
        # Como a solucao, alem de ter o caminho, tem o tempo tambem, entao é adicionado "Tempo" na tabela
        visualize_table(tsp_name, solutions, tsp_solution, ["Tempo"])

        if VISUALIZE:
            for j in range(REPEATED_TIME):
                visualize_graph(tsp_graph, solutions[j][0])


def genetico():
    VISUALIZE = False
    REPEATED_TIME = 100
    GENERATIONS = 100
    GENERATIONS_SIZE = 10
    LIMIT_DATA = 2  # -1 para pegar todos os dados, n (numero natural qualquer) pega os primeiros n dados

    tsp_datas = tsp.import_all_tsp_data("./assets", LIMIT_DATA)
    best_datas = tsp.import_all_tsp_solutions("./assets")

    # Limpa as tabelas da pasta "output"
    clear_tables()

    for tsp_name, tsp_info in tsp_datas.items():
        tsp_graph, tsp_data = tsp_info
        tsp_solution = best_datas[tsp_name]

        solutions = []
        for i in range(REPEATED_TIME):
            solution = algoritmo_genetico(tsp_data, GENERATIONS_SIZE, GENERATIONS)
            solutions.append(solution)

        # Visualiza as soluções
        visualize_table(tsp_name, solutions, tsp_solution)

        if VISUALIZE:
            for j in range(REPEATED_TIME):
                visualize_graph(tsp_graph, solutions[j])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "g":
            genetico()
        elif arg == "t":
            tempera()
        else:
            print("Argumento inválido. Use 'g' ou 't'.")
    else:
        print("Argumento inválido. Use 'g' ou 't'.")
