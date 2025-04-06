from libs import tsp
from libs.tempera import tempera_simulada
from libs.visual import visualize_graph, visualize_table


def main():
    VISUALIZE = True
    REPEATED_TIME = 100

    tsp_datas = tsp.import_all_tsp_data("./assets")

    for tsp_graph, tsp_data in tsp_datas:
        solutions = []

        for i in range(REPEATED_TIME):
            solution = tempera_simulada(tsp_data)
            solutions.append(solution)
            
        # Visualiza as soluções
        visualize_table(solutions)

        if VISUALIZE:
            for j in range(REPEATED_TIME):
                visualize_graph(tsp_graph, solutions[j])


if __name__ == "__main__":
    main()
