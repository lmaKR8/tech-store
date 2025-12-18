# ===================================================
# CONSTANTES
# ===================================================
VERDE = '\033[92m'
ROJO = '\033[91m'
AMARILLO = '\033[93m'
AZUL = '\033[94m'
CYAN = '\033[96m'
NEGRITA = '\033[1m'
RESET = '\033[0m'

CATEGORIAS = ("LAPTOPS", "PERIFÉRICOS", "ACCESORIOS")


# ===================================================
# FUNCIONES AUXILIARES
# ===================================================

def mostrar_menu():
    """
    Muestra el menú principal.
    """
    print(f"\n{CYAN}{NEGRITA}{'='*60}{RESET}")
    print(f"{AZUL}    Menú de Opciones{RESET}")
    print(f"{CYAN}{'-'*24}{RESET}")
    print(f"{CYAN}  1. Ver Inventario{RESET}")
    print(f"{CYAN}  2. Registrar Producto{RESET}")
    print(f"{CYAN}  3. Actualizar Stock{RESET}")
    print(f"{CYAN}  4. Eliminar Producto{RESET}")
    print(f"{CYAN}  5. Guardar Inventario{RESET}")
    print(f"{CYAN}  6. Salir{RESET}")
    print(f"{CYAN}{NEGRITA}{'='*60}{RESET}\n")


def formatear_precio(valor):
    """
    Formatea un número a pesos chilenos (CLP).
    Args:
        valor (int): Número a formatear.
    Returns:
        str: String formateado ("$1.250.000")
    """
    return f"${valor:,}".replace(',', '.')


def validar_numero(texto, tipo=int, permitir_cero=True):
    """
    Solicita y valida que el número sea positivo o cero según el parámetro [permitir_cero].
    Args:
        texto (str): Mensaje que se muestra al usuario.
        tipo (type): Tipo de dato a retornar (int o float).
        permitir_cero (bool): Si True, permite valor 0. Si False, solo valores > 0.
    Returns:
        int o float: Número válido ingresado por el usuario.
    """
    while True:
        try:
            print(f"{AZUL}{texto}{RESET}", end='')
            valor = tipo(input())
            
            if permitir_cero:
                if valor >= 0:
                    return valor
                else:
                    print(f"{ROJO}Error: El valor debe ser mayor o igual a 0.{RESET}")
            else:
                if valor > 0:
                    return valor
                else:
                    print(f"{ROJO}Error: El valor debe ser mayor a 0.{RESET}")
                
        except ValueError:
            print(f"{ROJO}Error: Debe ingresar un número válido.{RESET}")


def seleccionar_categoria():
    """
    Menú para seleccionar una categoría.
    """
    print(f"\n{CYAN}Seleccione una categoría:{RESET}")
    for i, categoria in enumerate(CATEGORIAS, 1):
        print(f"  {i}. {categoria}")
    
    while True:
        try:
            print(f"{AZUL}Opción (1-{len(CATEGORIAS)}): {RESET}", end='')
            opcion = int(input())
            if 1 <= opcion <= len(CATEGORIAS):
                return CATEGORIAS[opcion - 1]
            else:
                print(f"{ROJO}Error: Opción inválida. Seleccione entre 1 y {len(CATEGORIAS)}.{RESET}")
            
        except ValueError:
            print(f"{ROJO}Error: Debe ingresar un número válido.{RESET}")


def buscar_producto(productos, busqueda):
    """
    Realiza búsqueda parcial en el nombre o exacta en SKU.
    Args:
        productos (list): Lista de diccionarios de productos.
        busqueda (str): Término de búsqueda ingresado por el usuario.
    Returns:
        list: Lista de productos que coinciden con la búsqueda.
    """
    busqueda = busqueda.upper()
    coincidencias = []
    
    for producto in productos:
        if busqueda == producto['sku'] or busqueda in producto['nombre']:
            coincidencias.append(producto)
    return coincidencias


def seleccionar_de_lista(coincidencias, titulo="Resultados encontrados"):
    """
    Muestra una lista numerada de productos y permite seleccionar uno.
    Args:
        coincidencias (list): Lista de productos a mostrar.
        titulo (str): Título a mostrar en el menú.
    Returns:
        int o None: Índice del producto seleccionado o None si cancela.
    """
    print(f"\n{CYAN}{titulo}:{RESET}")
    
    for i, producto in enumerate(coincidencias, 1):
        print(f"  {i}. {producto['nombre']} - SKU: {producto['sku']}")
    print(f"  0. Cancelar")
    
    while True:
        try:
            print(f"{AZUL}Seleccione una opción (0-{len(coincidencias)}): {RESET}", end='')
            opcion = int(input())
            if opcion == 0:
                return None
            elif 1 <= opcion <= len(coincidencias):
                return opcion - 1
            else:
                print(f"{ROJO}Error: Opción inválida.{RESET}")

        except ValueError:
            print(f"{ROJO}Error: Debe ingresar un número válido.{RESET}")


def confirmar_accion(mensaje):
    """
    Solicita confirmación del usuario para una acción.
    Args:
        mensaje (str): Mensaje de confirmación a mostrar.
    Returns:
        bool: True si el usuario confirma (S), False en caso contrario (N).
    """
    while True:
        print(f"{AMARILLO}{mensaje} (S/N): {RESET}", end='')
        respuesta = input().strip().upper()

        if respuesta == 'S':
            return True
        elif respuesta == 'N':
            return False
        else:
            print(f"{ROJO}Error: Responda 'S' para Sí o 'N' para No.{RESET}")


def calcular_anchos_columnas(productos):
    """
    Determina el ancho necesario para cada columna (evita desborde).
    Args:
        productos (list): Lista de diccionarios de productos.
    Returns:
        dict: Diccionario con los anchos de cada columna.
    """
    # Anchos mínimos basados en los encabezados
    anchos = {
        'sku': len("SKU"),
        'nombre': len("NOMBRE"),
        'categoria': len("CATEGORÍA"),
        'precio': len("PRECIO (CLP)"),
        'stock': len("STOCK"),
        'total': len("TOTAL (CLP)")
    }
    
    # Analiza el contenido de los productos
    for producto in productos:
        anchos['sku'] = max(anchos['sku'], len(producto['sku']))
        anchos['nombre'] = max(anchos['nombre'], len(producto['nombre']))
        anchos['categoria'] = max(anchos['categoria'], len(producto['categoria']))
        anchos['precio'] = max(anchos['precio'], len(formatear_precio(producto['precio'])))
        anchos['stock'] = max(anchos['stock'], len(str(producto['stock'])))
        
        precio_total = producto['precio'] * producto['stock']
        anchos['total'] = max(anchos['total'], len(formatear_precio(precio_total)))
    
    # Aplica límites máximos para evitar desborde
    anchos['sku'] = min(anchos['sku'], 15)
    anchos['nombre'] = min(anchos['nombre'], 40)
    anchos['categoria'] = min(anchos['categoria'], 20)
    anchos['precio'] = min(anchos['precio'], 15)
    anchos['stock'] = min(anchos['stock'], 8)
    anchos['total'] = min(anchos['total'], 15)
    
    return anchos
