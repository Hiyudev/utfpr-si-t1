import numpy as np
from random import sample, randint
from libs.tsp import Node


def get_cidade(nodes: list[Node], id: int):
      for node in nodes:
            if node.id == id:
                  return node 

def calc_custo(nodes: list[Node], ordem: list[int]) -> float:
      custo_total = 0.0

      for i in range(len(ordem)-1):
            cidade_atual = get_cidade(nodes, ordem[i])

            for vizinho, custo in cidade_atual.neighbors:
                  if vizinho.id == ordem[i+1]:
                        custo_total += custo
                        break
      
      ultima_cidade = get_cidade(nodes, ordem[-1])

      for vizinho, custo in ultima_cidade.neighbors:
            if vizinho.id == ordem[0]:
                  custo_total += custo
                  break
      
      return custo_total  

def funcao_adaptacao(geracao):
      scores = []
      for solucao, custo in geracao:
            score = 1 / (1 + custo)
            scores.append(score)     

      probabilidades = [(score / sum(scores)) for score in scores]
      return probabilidades

def seleciona_pais(probs):
      indices_escolhidos = np.random.choice(len(probs), 2, replace=False, p=np.array(probs))
      return indices_escolhidos

def func_reproducao(nodes, s1, s2) -> tuple[list: int, float]:
      ponto_cruzamento = randint(1, len(s1) - 1)
      nova_solucao = s1[:ponto_cruzamento]

      for cidade in s2:
            if cidade not in nova_solucao:
                  nova_solucao.append(cidade)

      custo = calc_custo(nodes, nova_solucao)   
      return (nova_solucao, custo)


def crossover(nodes, geracao, probs):
      nova_geracao = []
      for i in range(len(geracao)):
            indices_escolhidos = seleciona_pais(probs)
            s1 = geracao[indices_escolhidos[0]][0]
            s2 = geracao[indices_escolhidos[1]][0]

            solucao: tuple[list: int, float] = func_reproducao(nodes, s1, s2)
            nova_geracao.append(solucao)

      return nova_geracao

def get_nodes(nodes, solucao: tuple[list: int, float]) -> list[Node]:
      solucao_final = []
      for cidade_id in solucao[0]:
            solucao_final.append(get_cidade(nodes, cidade_id))

      return solucao_final

def algoritmo_genetico(nodes: list[Node], n_populacao: int, n_geracoes):
      n_cidades = len(nodes)
      populacao_inicial: list[tuple[list: int, float]] = []

      # Criando a populacao inicial de estados
      for i in range(n_populacao):
            ordem_aleatoria = sample(range(0, n_cidades), n_cidades)
            solucao: tuple[list: int, float] = [ordem_aleatoria, calc_custo(nodes, ordem_aleatoria)]
            populacao_inicial.append(solucao)

      geracao = populacao_inicial

      melhor_solucao = min(geracao, key=lambda x: x[1])

      for i in range(n_geracoes):
            probabilidades = funcao_adaptacao(geracao)
            nova_geracao = crossover(nodes, geracao, probabilidades)

            melhor_geracao = min(geracao, key=lambda x: x[1])
            
            if melhor_geracao[1] < melhor_solucao[1]:
                  melhor_solucao = melhor_geracao

            geracao = nova_geracao
      
      print(melhor_solucao)
      nodes_solucao_final = get_nodes(nodes, melhor_solucao)
      return nodes_solucao_final