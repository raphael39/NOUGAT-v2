import heapq  # Importieren des heapq Moduls

class reRoutingTravel:
    def __init__(self, start, ziel, printed_matrix):
        self.start_x = round(start[0])
        self.start_y = round(start[1])
        self.ziel_x = round(ziel[0])
        self.ziel_y = round(ziel[1])
        self.start = (self.start_x, self.start_y)
        self.ziel = (self.ziel_x, self.ziel_y)
        self.printed_matrix = printed_matrix

    # Methode zum Finden der äußeren Grenzen der Matrix
     

    def findPathWithDJ(self):
        # Initialisieren einer Warteschlange für die Knoten, die noch zu besuchen sind
        queue = [self.start]
        # Erstellen eines Dictionaries zur Speicherung des Pfades (Vorgänger von jedem Knoten)
        previous_nodes = {self.start: None}

        while queue:
            current_node = queue.pop(0)

            # Wenn das Ziel erreicht wurde, den Pfad zurückverfolgen und zurückgeben
            if current_node == self.ziel:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                return path[::-1]  # Rückwärtige Reihenfolge für den korrekten Pfad

            x, y = current_node

            # Überprüfen der umliegenden Knoten (links, rechts, oben, unten)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_node = (x + dx, y + dy)

                # Überprüfen, ob der nächste Knoten innerhalb der Matrixgrenzen liegt und nicht gedruckt ist
                if 0 <= next_node[0] < len(self.printed_matrix) and 0 <= next_node[1] < len(self.printed_matrix[0]):
                    if self.printed_matrix[next_node[0]][next_node[1]] == 0 and next_node not in previous_nodes:
                        queue.append(next_node)
                        previous_nodes[next_node] = current_node

        # Kein Pfad gefunden
        return []
    
    # Methode zum Finden des Pfades mit dem A* Algorithmus
    # Ansonsten genau wie die Methode oben nur mit einer anderen Warteschlange
    # die Warteschlange wird sortiert nach der Heuristik (Distanz zum Ziel) und den G-Kosten (Kosten vom Startknoten zum aktuellen Knoten)
    def findPathWithA(self):

        # Hilfsfunktion für die Manhattan Distanz
        def heuristic(new_node, ziel):
            # Manhattan Distanz
            return abs(new_node[0] - ziel[0]) + abs(new_node[1] - ziel[1])
            
            # Euklidische Distanz
            # dx = abs(new_node[0] - ziel[0])
            # dy = abs(new_node[1] - ziel[1])
            # return (dx ** 2 + dy ** 2) ** 0.5
            
            # Octile Distanz
            # dx = abs(new_node[0] - ziel[0])
            # dy = abs(new_node[1] - ziel[1])
            # return 1 * (dx + dy) + (1.414 - 2 * 1) * min(dx, dy)

        # Initialisieren der Priority Queue
        queue = []
        heapq.heappush(queue, (0, self.start))  # Initialisieren der Queue mit dem Startknoten

        # G-Kosten und Vorgänger
        g_costs = {self.start: 0.0}
        previous_nodes = {self.start: None}

        while queue:
            current_node = heapq.heappop(queue)[1]

            if current_node == self.ziel:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                return path[::-1]  # Rückwärtige Reihenfolge für den korrekten Pfad

            x, y = current_node

            # Überprüfen der umliegenden Knoten (links, rechts, oben, unten, diagonal)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                next_node = (x + dx, y + dy)

                # Überprüfen, ob der nächste Knoten innerhalb der Matrixgrenzen liegt und nicht gedruckt ist, wenn bereits gedruckt ist, kostet der Knoten 500 extra
                if 0 <= next_node[0] < len(self.printed_matrix) and 0 <= next_node[1] < len(self.printed_matrix[0]):
                    
                    if next_node not in previous_nodes:
                        extra_cost = 500 if self.printed_matrix[next_node[0]][next_node[1]] == 1 else 0
                        # Berechnen der G-Kosten für den nächsten Knoten, +1 für horizontal/vertikal, +1.414 für diagonal
                        new_g_cost = g_costs[current_node] + 1 + extra_cost if dx == 0 or dy == 0 else g_costs[current_node] + 1.414 + extra_cost

                        # Wenn der neue Pfad kürzer ist, die G-Kosten aktualisieren und den Knoten zur Warteschlange hinzufügen
                        if next_node not in g_costs or new_g_cost < g_costs[next_node]:
                            g_costs[next_node] = new_g_cost
                            f_cost = new_g_cost + heuristic(next_node, self.ziel)
                            heapq.heappush(queue, (f_cost, next_node))
                            previous_nodes[next_node] = current_node

        return []