import pandas as pd

def cargar_productos(path="data/productos.csv"):
    """Carga el catálogo de productos desde el archivo CSV."""
    return pd.read_csv(path)

def generar_cotizacion(productos_seleccionados, path="data/productos.csv"):
    """
    Recibe una lista de nombres de productos y devuelve:
    - Un DataFrame con la información de los productos seleccionados
    - El total en MXN como float
    """
    productos = cargar_productos(path)
    seleccion = productos[productos["Nombre"].isin(productos_seleccionados)].copy()

    # Validación: Convertir precios a float si vienen como string
    seleccion["Precio (MXN)"] = seleccion["Precio (MXN)"].astype(float)

    total = seleccion["Precio (MXN)"].sum()
    return seleccion, total
