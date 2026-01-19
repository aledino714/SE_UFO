from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    # Funzione per leggere tutta la tabella sighting
    def read_sighting():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, YEAR(s_datetime) AS year, state, shape
                    FROM sighting
                    ORDER BY year
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

# result = [
#               {'id': 1, 'year': 1949, 'state': 'tx', 'shape': 'cylinder'},
#               {'id': 4, 'year': 1956, 'state': 'tx', 'shape': 'circle'},
#               {'id': 5, 'year': 1960, 'state': 'hi', 'shape': 'light'}
#          ]

#---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    # Funzione per leggere tutta la tabella neighbor
    def read_neighbor():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT state1, state2
                    FROM neighbor
                    WHERE state1 < state2
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

# result = [
#               {'state1': 'AL', 'state2': 'FL'},
#               {'state1': 'AL', 'state2': 'GA'},
#               {'state1': 'AL', 'state2': 'MS'}
#          ]

#---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    # Funzione per leggere tutta la tabella state
    def read_state():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, name, lat, lng
                    FROM state
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result