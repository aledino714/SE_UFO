import flet as ft
from geopy import distance

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO
        # 1. Svuoto le opzioni attuali
        self._view.dd_year.options.clear()

        # 2. Ottengo la lista
        lista_anni = self._model.get_sighting()

        # 3. Popolo il dropdown
        for anno in lista_anni:
            self._view.dd_year.options.append(ft.dropdown.Option(key=str(anno), text=str(anno)))

        self._view.update()

    def handle_year_selection(self, e):
        # 1. Recupero il valore selezionato (l'anno) dal dropdown
        anno_selezionato = self._view.dd_year.value

        # 2. Svuoto le opzioni attuali
        self._view.dd_shape.options.clear()

        # 3. Chiedo al model le forme filtrate per l'anno selezionato
        lista_forme = self._model.get_forme_filtrate(anno_selezionato)

        # 4. Popolo il secondo dropdown forma
        for forma in lista_forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(key=forma, text=forma))

        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        self._view.lista_visualizzazione_1.controls.clear()

        # Recupero l'input dell'utente
        anno_selezionato = self._view.dd_year.value
        forma_selezionata = self._view.dd_shape.value

        n_nodi, n_archi = self._model.creazione_grafo(anno_selezionato, forma_selezionata)

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {n_nodi} Numero di archi: {n_archi}"))

        #--------------------------------------------------------------------------------------------------------------------------------
        lista_pesi = self._model.get_somma_pesi_nodi()

        for n, somma in lista_pesi:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {n}, somma pesi su archi = {somma}"))

        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        self._view.lista_visualizzazione_2.controls.clear()

        percorso, dist_totale = self._model.get_percorso_massimo()

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Peso cammino massimo: {dist_totale}"))

        # Ciclo sul percorso per stampare i singoli archi
        for i in range(len(percorso) - 1):
            u = percorso[i]
            v = percorso[i + 1]
            peso = self._model.grafo[u][v]['weight']
            dist = distance.geodesic(self._model.idMap[u], self._model.idMap[v]).km

            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{u} --> {v}: weight {peso} distance {dist}"))

        self._view.update()
