import networkx as nx
from database.dao import DAO
from geopy import distance

class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.lista_anni = []
        self.lista_forme = []
        self.lista_avvistamenti = []
        self.lista_nodi = []
        self.lista_archi = []

        # --- AGGIUNTE PER LA RICORSIONE ---
        self.best_percorso = []  # Memorizzerà la lista di stati del cammino più lungo
        self.best_distanza = 0  # Memorizzerà il valore (km) della distanza massima trovata
        self.idMap = {}  # Dizionario per tradurre 'ID stato' in (latitudine, longitudine)

    def creazione_grafo(self, anno_selezionato, forma_selezionata):
        self.grafo.clear()
        self.lista_nodi.clear()
        self.lista_archi.clear()
        self.idMap = {}

        #---------------------------------------
        # AGGIUNGO I NODI
        vertici1 = DAO.read_state()

        for v in vertici1:
            self.lista_nodi.append(v['id'])
            for a in self.lista_nodi:
                self.grafo.add_node(a)
                self.idMap[v['id']] = (v['lat'], v['lng'])
        #---------------------------------------
        # CALCOLO IL PESO
        conteggio_stati = {} # esempio: {'TX': 5, 'AL': 2}
        for a in self.lista_avvistamenti:
            if str(a['year']) == str(anno_selezionato) and a['shape'] == forma_selezionata:
                s = a['state']
                conteggio_stati[s] = conteggio_stati.get(s, 0) + 1

        # DEBUG:
        print(f"Conteggi generati per ogni stato: {conteggio_stati}")

        #---------------------------------------
        # AGGIUNGO GLI ARCHI CON IL PESO
        archi1 = DAO.read_neighbor()

        for a in archi1:
            self.lista_archi.append(a)
            for n in self.lista_archi:
                u = n['state1']
                v = n['state2']

                # Trasformo u e v in minuscolo per corrispondere alle chiavi del dizionario
                peso_u = conteggio_stati.get(u.lower(), 0)
                peso_v = conteggio_stati.get(v.lower(), 0)

                peso_arco = peso_u + peso_v

                self.grafo.add_edge(u, v, weight=peso_arco)

        return len(self.grafo.nodes), len(self.grafo.edges)

    def get_sighting(self):
        self.lista_anni.clear()

        self.lista_avvistamenti = DAO.read_sighting()

        for a in self.lista_avvistamenti:
            anno = a['year']
            if anno not in self.lista_anni:
                self.lista_anni.append(anno)

        return self.lista_anni

    def get_forme_filtrate(self, anno_selezionato):
        self.lista_forme.clear()

        for a in self.lista_avvistamenti:
            if str(a['year']) == str(anno_selezionato):
                if a['shape'] != '' and a['shape'] not in self.lista_forme:
                    self.lista_forme.append(a['shape'])

        return self.lista_forme

    def get_somma_pesi_nodi(self):
        lista_pesi = []

        for n in self.grafo.nodes:
            somma = self.grafo.degree(n, weight='weight')
            lista_pesi.append((n, somma))

        # DEBUG:
        print(f'Lista pesi: {lista_pesi}')
        print(f'self.grafo.nodes {self.grafo.nodes}')
        print(f'self.grafo.degree {self.grafo.degree}')

        return lista_pesi

    def get_percorso_massimo(self):
        self.best_percorso = []
        self.best_distanza = 0

        # Il cammino può partire da qualsiasi nodo del grafo
        for nodo in self.grafo.nodes():
            self._ricorsione([nodo], 0)

        return self.best_percorso, self.best_distanza

    def _ricorsione(self, parziale, distanza_parziale):
        # parziale (la lista dei nodi) = è una lista che tiene traccia della strada che si sta percorrendo in quel preciso momento
        # distanza parziale (il valore accomulato) = è un numero (float o int) che rappresenta la somma delle distanze (in km) degli archi che compongono il percorso dentro parziale.

        # Condizione di uscita: non ci sono più vicini con peso crescente
        ultimo = parziale[-1]
        vicini = self.grafo.neighbors(ultimo)

        fermati = True
        for v in vicini:
            # 1. Percorso semplice: v non deve essere già nel percorso
            if v not in parziale:
                peso_nuovo = self.grafo[ultimo][v]['weight']

                # 2. Vincolo: peso SEMPRE CRESCENTE
                # Se è il primo arco del percorso o se il peso è > dell'ultimo arco
                if len(parziale) == 1 or peso_nuovo > self.grafo[parziale[-2]][parziale[-1]]['weight']:
                    fermati = False

                    # Calcolo distanza tra 'ultimo' e 'v'
                    dist_aggiuntiva = distance.geodesic(self.idMap[ultimo], self.idMap[v]).km

                    # Aggiungo e continuo la ricerca
                    parziale.append(v)
                    self._ricorsione(parziale, distanza_parziale + dist_aggiuntiva)

                    # Backtracking
                    parziale.pop()

        # Se non posso più andare avanti, controllo se questo è il miglior percorso
        if fermati:
            if distanza_parziale > self.best_distanza:
                self.best_distanza = distanza_parziale
                self.best_percorso = list(parziale)





























