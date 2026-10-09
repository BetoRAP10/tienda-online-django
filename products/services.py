# Capa de servicios: aqui vive la logica de negocio, separada de las vistas.

# Patron de comportamiento: Strategy
# Cada estrategia encapsula una forma distinta de calcular el descuento
class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.90


class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.80


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio


# Selecciona la estrategia segun el nombre de la categoria del producto
def obtener_estrategia(categoria_nombre):
    estrategias = {
        'Electronica': DescuentoElectronica(),
        'Ropa': DescuentoRopa(),
    }
    return estrategias.get(categoria_nombre, SinDescuento())
