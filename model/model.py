from copy import deepcopy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        # grafo
        self._grafo = nx.DiGraph()
        self._ordini = []
        self._id_map_ordini = {}
        # ricorsione per percorso più lungo
        self._percorso_max = None
        # ricorsione per percorso più pesante
        self._heavier_path = None
        self._best_weight = 0

    def get_all_stores(self):
        return DAO.get_all_stores()

    def get_nodes(self):
        return self._grafo.nodes()

    def build_graph(self, store_id, k_giorni):
        self._grafo.clear()
        # aggiungo i nodi
        self.fill_id_map_ordini(store_id)
        self._grafo.add_nodes_from(self._ordini)
        # aggiungo gli archi
        all_edges = DAO.get_all_edges(store_id, k_giorni)
        for edge in all_edges:
            self._grafo.add_edge(self._id_map_ordini[edge[0]], self._id_map_ordini[edge[1]], weight=edge[2])
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def fill_id_map_ordini(self, store_id):
        self._ordini = DAO.get_all_orders(store_id)
        for ordine in self._ordini:
            self._id_map_ordini[ordine.order_id] = ordine

    def get_longest_path(self, order_id):
        starting_node = self._id_map_ordini[int(order_id)]
        tree = nx.dfs_tree(self._grafo, starting_node)
        self._percorso_max = []
        self.ricorsione(tree, [starting_node])
        return self._percorso_max

    def ricorsione(self, tree, percorso_temp):
        if len(percorso_temp) > len(self._percorso_max):
            self._percorso_max = deepcopy(percorso_temp)
        ultimo = percorso_temp[-1]

        for vicino in tree.successors(ultimo):
            if vicino not in percorso_temp: #per evitare cicli
                percorso_temp.append(vicino)
                self.ricorsione(tree, percorso_temp)
                percorso_temp.pop()

    def get_heavier_path(self, order_id):
        starting_node = self._id_map_ordini[int(order_id)]
        self._heavier_path = []
        self._best_weight = 0

        parziale = []
        parziale.append(starting_node)
        for vicino in self._grafo.successors(starting_node):
                parziale.append(vicino)
                self.ricorsione_by_peso(parziale)
                parziale.pop()
        return self._heavier_path

    def ricorsione_by_peso(self, parziale):
        if self.peso(parziale) > self._best_weight :
            self._best_weight = self.peso(parziale)
            self._heavier_path = deepcopy(parziale)
        ultimo = parziale[-1]
        for vicino in self._grafo.successors(ultimo):
            if self.is_valid(vicino, parziale):
                parziale.append(vicino)
                self.ricorsione_by_peso(parziale)
                parziale.pop()

    def is_valid(self, vicino, parziale):
        # il nodo vicino non deve essere già contenuto nella lista parziale
        # il peso dell'arco che voglio inserire deve essere minore di quello dell'ultimo arco inserito nel percorso parziale
        peso_corrente = self._grafo[parziale[-1]][vicino]["weight"]
        peso_precedente = self._grafo[parziale[-2]][parziale[-1]]["weight"]
        if vicino not in parziale and peso_corrente < peso_precedente:
            return True
        return False

    def peso(self, parziale):
        # calcolo il peso della lista parziale per ogni arco
        peso = 0
        for i in range(0, len(parziale)-1):
            peso += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return peso