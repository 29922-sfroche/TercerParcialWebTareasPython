import html
from typing import List


class Producto:
    """Equivalente en Python de la clase producto de PHP.

    Solo se implementa lo necesario para el combo (get_select_options),
    manteniendo nombres y comportamiento similares.
    """

    def __init__(self, con):
        self.con = con

    # ********** LISTA SIMPLE PARA COMBOS (SELECT) ***************************
    def get_select_options(self) -> str:
        """Devuelve un string con las etiquetas <option> para el <select>.

        Equivale a producto::get_select_options() en PHP.
        """
        opciones: List[str] = [
            '<option value="">Seleccione un producto...</option>'
        ]

        sql = "SELECT ProductoID, Descripcion, Precio FROM Productos ORDER BY Descripcion"

        try:
            with self.con.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
        except Exception:
            # Si hay error (por ejemplo aún no se han creado/insertado productos),
            # simplemente regresamos la opción por defecto.
            return opciones[0]

        for row in rows:
            prod_id = int(row["ProductoID"])
            nombre = html.escape(str(row["Descripcion"]), quote=True)
            precio = float(row["Precio"])

            opciones.append(
                f'<option value="{prod_id}" data-precio="{precio}">{nombre}</option>'
            )

        return "".join(opciones)

    # Métodos siguientes son solo esqueletos con nombres equivalentes a PHP
    # para que se vea la correspondencia, aunque no se usen en este ejercicio.

    def update_producto(self):
        raise NotImplementedError("update_producto no está implementado en esta versión Python")

    def save_producto(self):
        raise NotImplementedError("save_producto no está implementado en esta versión Python")

    def delete_producto(self, _id: int):
        raise NotImplementedError("delete_producto no está implementado en esta versión Python")

    def get_form(self, _id=None):
        raise NotImplementedError("get_form no está implementado en esta versión Python")

    def get_list(self):
        raise NotImplementedError("get_list no está implementado en esta versión Python")

    def get_detail_producto(self, _id: int):
        raise NotImplementedError("get_detail_producto no está implementado en esta versión Python")
