
# Este programa, que define nuestro propio filtro jinja, tiene 2 partes:

# Función filtrado
def limpiar_nulos(datos):
    # Esos datos pueden ser una lista, un diccionario, un valor simple (numero, cadena, etc.)
    # Cuando se use el filtro escribirán algo asi como:
    #   {{ datos | limpiar_nulos }}
    #   {{ [1, None, 2] | limpiar_nulos }}              # Resultado esperado: [1, 2]     La ~ de YAML en python llega como None
    #   {{ {'a': 1, 'b': None} | limpiar_nulos }}       # Resultado esperado: {'a': 1}
    # Es un poco más complejo.. porque debe ser recursiva, eliminando los valores None dentro de listas y diccionarios anidados.
    #   {{ {'a': 1, 'b': None, 'c': {'d': None, 'e': 2}} | limpiar_nulos }}  # Resultado esperado: {'a': 1, 'c': {'e': 2}}

    if isinstance(datos, list):               # Si lo que me llega en datos es una lista
        return [limpiar_nulos(elemento) for elemento in datos if elemento is not None]
    if isinstance(datos, dict):               # Si lo que me llega en datos es un diccionario
        return {clave: limpiar_nulos(valor) for clave, valor in datos.items() if valor is not None}
    return datos

# Registro en ansioble (Dar de alta en ansible nuestra función de filtrado)
class FilterModule(object):
    def filters(self):
        return {
            'limpiar_nulos': limpiar_nulos
            #                ^^^^^^^^^^^^^           Esto es el nombr de mi función python
            # ^^^^^^^^^^^^^                          Esto es el nombre en jinja del filtro que estamos definiendo
            
            # Estos nombres no tienen porque coincidir. Lo normal es que lo cree todo con el mismo nombre.. por comodidad para mi.
            # Pero realmente:
            # El fichero podria llamarse menchu.py. Da igual el nombre. Lo único importante es que esté dentro de la carpeta filter_plugins 
            # La función python podría llamarse federico
            #              Y en jinja seguiría siendo {{ datos | limpiar_nulos }}
        }
