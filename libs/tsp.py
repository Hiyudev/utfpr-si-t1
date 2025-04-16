# Arquivo para extrair dados de um arquivo .atsp, que contém a matriz de adjacência
import tsplib95
from networkx import Graph
from os import listdir


def load_tsp_data(file_path: str):
    problem = tsplib95.load(file_path)

    nodes_length = problem.as_dict()["dimension"]

    # Cada elemento da lista representa um no, identificado pela sua indice/posicao
    # Dentro de cada elemento, possui uma outra lista que representa as distanias em relacao aos outros nos de acordo com a indice tambem.
    # Exemplo: [[999, 1], [1, 999]] -> distancia entre 0 e 0 é 999, entre 0 e 1 é 1, entre 1 e 0 é 1 e entre 1 e 1 é 999
    # Assim, na implementação fica node[0][0] seria a distância entre o nó 0 e ele mesmo. Outro exemplo: node[0][1] seria a distância entre o nó 0 e o nó 1.
    nodes: list[list[int]] = [[0] * nodes_length for _ in range(nodes_length)]

    graph = problem.get_graph()
    graph_adjacency_list = list(graph.adjacency())

    for node_id, node_neighbors in graph_adjacency_list:
        for neighbor_id, weight_dict in node_neighbors.items():
            weight = weight_dict["weight"]

            nodes[node_id][neighbor_id] = weight

    return graph, nodes


def import_all_tsp_data(
    file_path: str, limit=-1
) -> dict[str, tuple[Graph, list[list[int]]]]:
    # Pega todos os arquivos .astp do diretório
    files = [f for f in listdir(file_path) if f.endswith(".atsp")]
    data: dict[str, tuple[Graph, list[list[int]]]] = {}

    for file in files:
        load_file_path = f"{file_path}/{file}"
        load_file_graph, load_file_nodes = load_tsp_data(load_file_path)

        file_name = file.split(".")[0]
        data[file_name] = (load_file_graph, load_file_nodes)

    # Ordena os arquivos pela quantidade de nós
    data = dict(sorted(data.items(), key=lambda x: len(x[1][1])))
    if limit > 0:
        data = dict(list(data.items())[:limit])

    return data


def import_all_tsp_solutions(file_path: str) -> dict[str, int]:
    # Pega o arquivo de solucao
    file = f"{file_path}/best.csv"

    data = {}

    with open(file, "r") as f:
        rows = f.readlines()

        for row in rows:
            columns = row.strip().split(",")

            file_name = columns[0]
            solution_value = int(columns[1])

            data[file_name] = solution_value

    return data
