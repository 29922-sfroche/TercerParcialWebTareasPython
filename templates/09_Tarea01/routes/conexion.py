import pymysql
from pymysql.cursors import DictCursor


DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "123"
DB_NAME = "Productos_BD"


def _ensure_database_and_tables(con):
    """Crea la base de datos y la tabla detalle_factura si no existen.

    Equivalente a la lógica de conexion.php en PHP.
    """
    with con.cursor() as cur:
        cur.execute(
            f"""
            CREATE DATABASE IF NOT EXISTS {DB_NAME}
            DEFAULT CHARACTER SET utf8mb4
            DEFAULT COLLATE utf8mb4_spanish_ci
            """
        )

    # Seleccionar la base de datos
    con.select_db(DB_NAME)

    # Crear la tabla detalle_factura si no existe
    with con.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS detalle_factura (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                precio DECIMAL(10, 2) NOT NULL,
                cantidad INT NOT NULL,
                total DECIMAL(10, 2) NOT NULL
            )
            """
        )


def get_connection():
    """Devuelve una conexión lista para usar la BD Productos_BD.

    - Conecta al servidor MySQL.
    - Crea la base de datos y la tabla detalle_factura si no existen.
    - Devuelve una conexión usando cursor tipo diccionario.
    """
    # Primero conectamos sin base de datos para poder crearla
    con = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=DictCursor,
    )

    _ensure_database_and_tables(con)

    # Aseguramos charset
    with con.cursor() as cur:
        cur.execute("SET NAMES utf8mb4")

    return con
