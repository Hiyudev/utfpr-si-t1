import sys
import os
from libs import tsp
from libs.genetico import algoritmo_genetico
from libs.visual import clear_tables, visualize_table
from libs.tempera import tempera_simulada

os.makedirs("logs", exist_ok=True)

def tempera():
    REPEATED_TIME = 100
    LIMIT_DATA = 1  # -1 para pegar todos os dados, n (numero natural qualquer) pega os primeiros n dados
    TEMPERA_PARAMETERS = {
        "temperatura_inicial": 1000,
        "temperatura_final": 0,
        "tempo_maximo": 100,
    }

    tsp_datas = tsp.import_all_tsp_data("./assets", LIMIT_DATA)
    best_datas = tsp.import_all_tsp_solutions("./assets")

    # Limpa as tabelas da pasta "output"
    clear_tables()

    for tsp_name, tsp_info in tsp_datas.items():
        tsp_graph, tsp_data = tsp_info
        tsp_solution = best_datas[tsp_name]

        solutions: list[tuple[list[int], int]] = []
        for i in range(REPEATED_TIME):
            solution = tempera_simulada(tsp_data, TEMPERA_PARAMETERS)
            solutions.append(solution)

        # Visualiza as soluções
        # Como a solucao, alem de ter o caminho, tem o tempo tambem, entao é adicionado "Tempo" na tabela
        visualize_table(tsp_name, tsp_data, solutions, tsp_solution, ["Tempo"])


def genetico():
    REPEATED_TIME = 100
    GENERATIONS = 100
    GENERATIONS_SIZE = 10
    CORTE_RANDOM = True
    LIMIT_DATA = 2  # -1 para pegar todos os dados, n (numero natural qualquer) pega os primeiros n dados

    tsp_datas = tsp.import_all_tsp_data("./assets", LIMIT_DATA)
    best_datas = tsp.import_all_tsp_solutions("./assets")

    # Limpa as tabelas da pasta "output"
    clear_tables()

    for tsp_name, tsp_info in tsp_datas.items():
        tsp_graph, tsp_data = tsp_info
        tsp_solution = best_datas[tsp_name]

        solutions = []
        melhor_iteracao = 0
        melhor_custo = -1

        for i in range(REPEATED_TIME):
            caminho, custo, i_geracao = algoritmo_genetico(
                tsp_data, GENERATIONS_SIZE, GENERATIONS, CORTE_RANDOM
            )

            if custo < melhor_custo or melhor_custo == -1:
                melhor_custo = custo
                melhor_iteracao = i

            # Novas colunas para o csv
            solutions.append(
                (
                    caminho,
                    i_geracao
                )
            )

        print(
            f"Melhor custo encontrado: {melhor_custo} na execução de número {melhor_iteracao}."
        )

        # Visualiza as soluções
        visualize_table(tsp_name, tsp_data, solutions, tsp_solution, headers=["Geração em que a melhor solução foi encontrada"])

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
