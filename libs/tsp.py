# Arquivo para extrair dados de um arquivo .atsp, que contém a matriz de adjacência
import tsplib95
from networkx import Graph
from os import listdir


class Node:
    def __init__(self, id: int):
        self.id = id
        self.neighbors: list[tuple[Node, float]] = []

    def add_neighbor(self, node, weight: float):
        self.neighbors.append((node, weight))


def load_tsp_data(file_path: str):
    problem = tsplib95.load(file_path)

    nodes_length = problem.as_dict()["dimension"]
    nodes = [Node(i) for i in range(nodes_length)]

    graph = problem.get_graph()
    graph_adjacency_list = list(graph.adjacency())

    for node_id, node_neighbors in graph_adjacency_list:
        node = nodes[node_id]

        for neighbor_id, weight_dict in node_neighbors.items():
            # Verifica se o no e o vizinho são o mesmo
            if node_id == neighbor_id:
                continue

            neighbor = nodes[neighbor_id]
            neightbor_weight = weight_dict["weight"]

            node.add_neighbor(neighbor, neightbor_weight)

    return graph, nodes


def import_all_tsp_data(file_path: str) -> dict[str, tuple[Graph, list[Node]]]:
    # Pega todos os arquivos .astp do diretório
    files = [f for f in listdir(file_path) if f.endswith(".atsp")]
    data: dict[str, tuple[Graph, list[Node]]] = {}

    for file in files:
        load_file_path = f"{file_path}/{file}"
        load_file_graph, load_file_nodes = load_tsp_data(load_file_path)

        file_name = file.split(".")[0]
        data[file_name] = (load_file_graph, load_file_nodes)

    # Ordena os arquivos pela quantidade de nós
    data = dict(sorted(data.items(), key=lambda x: len(x[1][1])))

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
