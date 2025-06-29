from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_stores():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                        SELECT *
                        FROM stores s"""

            cursor.execute(query,)
            result = []
            for row in cursor.fetchall():
                result.append(Store(**row))
            return result
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_orders(store_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                        SELECT *
                        FROM orders o
                        WHERE o.store_id = %s
                        """

            cursor.execute(query, (store_id, ))
            result = []
            for row in cursor.fetchall():
                result.append(Order(**row))
            return result
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_edges(store_id, k_giorni):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                    SELECT DISTINCT o1.order_id as o1, o2.order_id as o2, SUM(oi.quantity+ oi2.quantity) as somma_prodotti
                    FROM orders o1, orders o2, order_items oi, order_items oi2 
                    WHERE o1.store_id = %s
                        AND o1.store_id=o2.store_id 
                        AND o1.order_date > o2.order_date
                        AND oi.order_id = o1.order_id
                        AND oi2.order_id  = o2.order_id
                        AND DATEDIFF(o1.order_Date, o2.order_date) < %s
                    GROUP BY o1.order_id, o2.order_id"""

            cursor.execute(query, (store_id, k_giorni))
            result = []
            for row in cursor.fetchall():
                result.append((row['o1'], row['o2'], row['somma_prodotti']))
            return result
        finally:
            cursor.close()
            conn.close()