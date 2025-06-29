import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_store(self):
        stores = self._model.get_all_stores()
        for store in sorted(stores):
            self._view._ddStore.options.append(ft.dropdown.Option(key=store.store_id, text=str(store)))

    def get_nodes(self):
        return self._model.get_nodes()

    def handle_crea_grafo(self, e):
        try:
            store = self._view._ddStore.value
            if store is None:
                self._view.create_alert("Attenzione! Selezionare uno store.")
                return
            k_giorni = self._view._txtIntK.value
            if k_giorni is None:
                self._view.create_alert("Attenzione! Indicare una durata minima di giorni.")
                return

            nNodes, nEdges = self._model.build_graph(store, k_giorni)
            self.fill_dd_nodes(self.get_nodes())

            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        finally:
            self._view._ddStore.disabled = True
            self._view._txtIntK.disabled = True
            self._view._btnCreaGrafo.disabled = True
            self._view._ddNode.disabled = False
            self._view._btnCerca.disabled = False
            self._view.update_page()

    def handleCerca(self, e):
        try:
            node = self._view._ddNode.value
            if node is None:
                self._view.create_alert("Attenzione! Selezionare un ordine.")
                return
            self._view.txt_result.controls.append(ft.Text(f"Caricamento"))
            self._view.update_page()
            longest_path = self._model.get_longest_path(node)
            self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {node}"))
            for element in longest_path:
                self._view.txt_result.controls.append(ft.Text(f"{element}"))
        finally:
            self._view._ddNode.disabled = True
            self._view._btnCerca.disabled = True
            self._view._btnRicorsione.disabled = False
            self._view.update_page()

    def handleRicorsione(self, e):
        pass

    def fill_dd_nodes(self, list_of_orders):
        for order in list_of_orders:
            self._view._ddNode.options.append(ft.dropdown.Option(key=order.order_id, text=str(order)))
