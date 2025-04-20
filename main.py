import sys
import csv
import numpy as np
from os import listdir
from libs import tsp
from libs.genetico import algoritmo_genetico
from libs.visual import clear_tables, visualize_table
from libs.tempera import tempera_simulada


def tempera():
    REPEATED_TIME = 100
    LIMIT_DATA = (
        -1
    )  # -1 para pegar todos os dados, n (numero natural qualquer) pega os primeiros n dados
    TEMPERA_PARAMETERS = {
        "temperatura_inicial": 10,
        "temperatura_final": 0,
        "tempo_maximo": 5000,
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
            caminho, custo, geracao = algoritmo_genetico(
                tsp_data, GENERATIONS_SIZE, GENERATIONS
            )

            if custo < melhor_custo or melhor_custo == -1:
                melhor_custo = custo
                melhor_iteracao = i
                melhor_caminho = caminho

            # Novas colunas para o csv
            solutions.append(
                (
                    caminho,
                    REPEATED_TIME,
                    GENERATIONS,
                    GENERATIONS_SIZE,
                    " -> ".join(map(str, caminho)),
                    custo,
                    geracao,
                )
            )

            extra_headers = [
                "Número de execuções do algoritmo",
                "Número de gerações executadas",
                "Tamanho de cada geração",
                "Caminho da solução encontrada",
                "Custo da solução",
                "Geração em que a melhor solução foi encontrada",
            ]

        #
        print(
            f"Melhor custo encontrado: {melhor_custo} na execução de número {melhor_iteracao}."
        )

        # Visualiza as soluções
        visualize_table(tsp_name, solutions, tsp_solution, headers=extra_headers)


def analyse():
    # Pega todos os arquivos dentro do diretório "output"
    files = listdir("./output")

    # Cria uma lista com os nomes dos arquivos
    tsp_names = [file.split("_")[0] for file in files if file.endswith(".csv")]

    mean_porcentages = []
    mean_times = []

    for index, file in enumerate(files):
        tsp_name = tsp_names[index]

        weights = []
        porcentages = []
        tempo = []

        with open(f"./output/{file}", "r") as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                is_header = "Numero de nos" in row[0]
                if is_header:
                    continue

                weights.append(int(row[1]))
                porcentages.append(float(row[2]))
                tempo.append(int(row[3]))

        minimum_weight = np.min(weights)
        mean_weight = np.mean(weights)
        maximum_weight = np.max(weights)

        mean_porcentage = np.mean(porcentages)
        mean_time = np.mean(tempo)

        mean_porcentages.append(mean_porcentage)
        mean_times.append(mean_time)

        print(f"Problema {tsp_name}")
        print(f"Menor peso: {minimum_weight}")
        print(f"Média de peso: {mean_weight}")
        print(f"Maior peso: {maximum_weight}")
        print(f"Média de porcentagem: {mean_porcentage}")
        print(f"Média de tempo: {mean_time}")
        print("\n")

    print("Resultados gerais")
    print(f"Média de porcentagem: {np.mean(mean_porcentages)}")
    print(f"Média de tempo: {np.mean(mean_times)}")
    print("\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "g":
            genetico()
        elif arg == "t":
            tempera()
        elif arg == "a":
            analyse()
        else:
            print("Argumento inválido. Use 'g', 't' ou 'a'.")
    else:
        print("Argumento inválido. Use 'g', 't' ou 'a'.")
