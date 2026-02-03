class Notebook:
    def __init__(self, codigo, marca, precio):
        self.codigo = codigo
        self.marca = marca
        self.precio = precio

    def getCodigo(self):
        return self.codigo

    def getMarca(self):
        return self.marca

    def getPrecio(self):
        return self.precio
