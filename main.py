from libs import tsp
from libs.tempera import tempera_simulada
from libs.visual import visualize_graph, visualize_table
from libs.genetico import algoritmo_genetico


def tempera():
    VISUALIZE = False
    REPEATED_TIME = 100

    tsp_datas = tsp.import_all_tsp_data("./assets")
    best_datas = tsp.import_all_tsp_solutions("./assets")

    for tsp_name, tsp_info in tsp_datas.items():
        tsp_graph, tsp_data = tsp_info
        tsp_solution = best_datas[tsp_name]

        solutions = []
        for i in range(REPEATED_TIME):
            solution = tempera_simulada(tsp_data)
            solutions.append(solution)

        # Visualiza as soluções
        visualize_table(tsp_name, solutions, tsp_solution)

        if VISUALIZE:
            for j in range(REPEATED_TIME):
                visualize_graph(tsp_graph, solutions[j])


def genetico():
    VISUALIZE = False
    REPEATED_TIME = 100
    GENERATIONS = 100
    GENERATIONS_SIZE = 10

    tsp_datas = tsp.import_all_tsp_data("./assets")
    best_datas = tsp.import_all_tsp_solutions("./assets")

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
    # tempera()
    genetico()
