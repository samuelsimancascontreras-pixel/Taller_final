import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "chef_costos.db")

class ChefDB:
    @staticmethod
    def inicializar():
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_proveedores (
                                id_proveedor INTEGER PRIMARY KEY, nombre TEXT, ciudad TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_ingredientes (
                                id_ingrediente INTEGER PRIMARY KEY, articulo TEXT, unidad TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS fact_costos (
                                id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_proveedor INTEGER, id_ingrediente INTEGER,
                                precio_historico REAL, precio_mercado REAL, fecha TEXT,
                                FOREIGN KEY(id_proveedor) REFERENCES dim_proveedores(id_proveedor),
                                FOREIGN KEY(id_ingrediente) REFERENCES dim_ingredientes(id_ingrediente))''')
            
            cursor.execute("SELECT COUNT(*) FROM dim_ingredientes")
            if cursor.fetchone()[0] == 0:
                print("Inyectando 5 registros iniciales (Seeding)...")
                cursor.executemany("INSERT INTO dim_proveedores VALUES (?, ?, ?)", 
                                   [(1, "Carnes Bog", "Bogotá"), (2, "Agro Sabana", "Chía"), 
                                    (3, "Lácteos Andinos", "Cajicá"), (4, "Pescadería Mar", "Cartagena"), (5, "Granos Col", "Bogotá")])
                cursor.executemany("INSERT INTO dim_ingredientes VALUES (?, ?, ?)", 
                                   [(101, "Lomo de Res", "Kg"), (102, "Papas Nativas", "Kg"), (103, "Queso Mozzarella", "Kg"), (104, "Salmón Fresco", "Kg"), (105, "Arroz Premium", "Kg")])
                cursor.executemany("INSERT INTO fact_costos (id_proveedor, id_ingrediente, precio_historico, precio_mercado, fecha) VALUES (?, ?, ?, ?, ?)", 
                                   [(1, 101, 35000, 45000, "2026-05-01"), (2, 102, 3000, 4000, "2026-05-02"), (3, 103, 18000, 22000, "2026-05-03"), (4, 104, 50000, 65000, "2026-05-04"), (5, 105, 4500, 5000, "2026-05-05")])
            conn.commit()