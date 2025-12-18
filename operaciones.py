from utils import (
    VERDE, ROJO, AMARILLO, AZUL, CYAN, NEGRITA, RESET,
    validar_numero, seleccionar_categoria, buscar_producto,
    seleccionar_de_lista, confirmar_accion, calcular_anchos_columnas,
    formatear_precio
)


def registrar_producto(productos, skus_usados):
    """
    Registra un producto nuevo en el inventario.
    Args:
        productos (list): Lista de diccionarios de productos.
        skus_usados (set): Conjunto de SKUs para validación de unicidad.
    """
    print(f"\n{CYAN}{NEGRITA}{'='*60}{RESET}")
    print(f"{AZUL}{'REGISTRAR NUEVO PRODUCTO'.center(60)}{RESET}")
    print(f"{CYAN}{NEGRITA}{'='*60}{RESET}\n")
    
    # Solicita SKU
    print(f"{AZUL}Ingrese código SKU: {RESET}", end='')
    sku = input().strip().upper()
    
    if not sku:
        print(f"{ROJO}Error: El SKU no puede estar vacío.{RESET}")
        return
    
    # Valida que el SKU no exista
    if sku in skus_usados:
        print(f"{ROJO}Error: El SKU '{sku}' ya existe en el inventario.{RESET}")
        return
    
    # Solicita nombre 
    print(f"{AZUL}Ingrese nombre del producto: {RESET}", end='')
    nombre = input().strip().upper()
    
    if not nombre:
        print(f"{ROJO}Error: El nombre no puede estar vacío.{RESET}")
        return
    
    # Selecciona categoría de la tupla
    categoria = seleccionar_categoria()
    
    # Valida precio
    precio = validar_numero("Ingrese precio en CLP: ", int, permitir_cero=False)
    
    # Valida stock
    stock = validar_numero("Ingrese cantidad en stock: ", int, permitir_cero=True)
    
    # Crea diccionario del producto
    nuevo_producto = {
        'sku': sku,
        'nombre': nombre,
        'categoria': categoria,
        'precio': precio,
        'stock': stock
    }
    
    # Agrega a la lista y al conjunto
    productos.append(nuevo_producto)
    skus_usados.add(sku)
    
    print(f"\n{VERDE}✓ Producto registrado exitosamente:{RESET}")
    print(f"  SKU: {sku}")
    print(f"  Nombre: {nombre}")
    print(f"  Categoría: {categoria}")
    print(f"  Precio: {formatear_precio(precio)}")
    print(f"  Stock: {stock} unidades")


def visualizar_inventario(productos):
    """
    Muestra el inventario completo en formato de tabla ordenada.
    Args:
        productos (list): Lista de diccionarios de productos.
    """
    if not productos:
        print(f"\n{AMARILLO}⚠ El inventario está vacío. No hay productos para mostrar.{RESET}")
        return
    
    # Ordena productos por categoría y luego por nombre
    productos_ordenados = sorted(productos, key=lambda p: (p['categoria'], p['nombre']))
    
    # Calcula anchos dinámicos de columnas
    anchos = calcular_anchos_columnas(productos_ordenados)
    
    # Calcula ancho total de la tabla
    ancho_total = (anchos['sku'] + anchos['nombre'] + anchos['categoria'] + anchos['precio'] + anchos['stock'] + anchos['total'] + 17)
    
    # Encabezado de la tabla
    print(f"\n{CYAN}{NEGRITA}{'='*ancho_total}{RESET}")
    print(f"{AMARILLO}{'INVENTARIO TECHSTORE'.center(ancho_total)}{RESET}")
    print(f"{CYAN}{NEGRITA}{'='*ancho_total}{RESET}")
    
    # Encabezados de columnas
    print(f"{VERDE}{'SKU'.ljust(anchos['sku'])} | "
        f"{'NOMBRE'.ljust(anchos['nombre'])} | "
        f"{'CATEGORÍA'.ljust(anchos['categoria'])} | "
        f"{'PRECIO (CLP)'.rjust(anchos['precio'])} | "
        f"{'STOCK'.rjust(anchos['stock'])} | "
        f"{'TOTAL (CLP)'.rjust(anchos['total'])}{RESET}")
    
    print(f"{CYAN}{'-'*ancho_total}{RESET}")
    
    # Filas de productos
    suma_total = 0
    productos_sin_stock = 0
    
    for producto in productos_ordenados:
        # Calcula precio total por producto (precio * stock)
        precio_total = producto['precio'] * producto['stock']
        suma_total += precio_total
        
        # Cuenta productos sin stock
        if producto['stock'] == 0:
            productos_sin_stock += 1
        
        # Formatea y alinea cada columna
        sku_truncado = producto['sku'][:anchos['sku']]
        nombre_truncado = producto['nombre'][:anchos['nombre']]
        categoria_truncada = producto['categoria'][:anchos['categoria']]
        
        print(f"{sku_truncado.ljust(anchos['sku'])} | "
            f"{nombre_truncado.ljust(anchos['nombre'])} | "
            f"{categoria_truncada.ljust(anchos['categoria'])} | "
            f"{formatear_precio(producto['precio']).rjust(anchos['precio'])} | "
            f"{str(producto['stock']).rjust(anchos['stock'])} | "
            f"{formatear_precio(precio_total).rjust(anchos['total'])}")
    
    # Pie de tabla con totales
    print(f"{CYAN}{'='*ancho_total}{RESET}")
    print(f"{AMARILLO}{'VALOR TOTAL DEL INVENTARIO:'.ljust(ancho_total - anchos['total'] - 3)}"
        f"{formatear_precio(suma_total).rjust(anchos['total'])}{RESET}")
    print(f"{CYAN}{'='*ancho_total}{RESET}")
    
    # Estadísticas adicionales
    print(f"\n{VERDE}Total de productos: {len(productos)} | "
        f"Productos sin stock: {productos_sin_stock}{RESET}\n")


def actualizar_stock(productos):
    """
    Actualiza la cantidad en stock de un producto existente.
    Args:
        productos (list): Lista de diccionarios de productos.
    """
    print(f"\n{CYAN}{NEGRITA}{'='*60}{RESET}")
    print(f"{AZUL}{'ACTUALIZAR STOCK DE PRODUCTO'.center(60)}{RESET}")
    print(f"{CYAN}{NEGRITA}{'='*60}{RESET}\n")
    
    if not productos:
        print(f"{AMARILLO}⚠ El inventario está vacío. No hay productos para actualizar.{RESET}")
        return
    
    # Solicitar búsqueda
    print(f"{AZUL}Ingrese nombre o SKU del producto a buscar: {RESET}", end='')
    busqueda = input().strip()
    
    if not busqueda:
        print(f"{ROJO}✗ Error: Debe ingresar un término de búsqueda.{RESET}")
        return
    
    # Buscar producto con búsqueda flexible
    coincidencias = buscar_producto(productos, busqueda)
    
    if not coincidencias:
        print(f"{AMARILLO}⚠ No se encontraron productos con '{busqueda}'.{RESET}")
        return
    
    # Si hay múltiples coincidencias, permitir seleccionar
    if len(coincidencias) > 1:
        indice = seleccionar_de_lista(coincidencias, "Se encontraron varios productos")
        if indice is None:
            print(f"{AMARILLO}⚠ Operación cancelada.{RESET}")
            return
        producto = coincidencias[indice]
    else:
        producto = coincidencias[0]
    
    # Mostrar información actual
    print(f"\n{CYAN}Producto seleccionado:{RESET}")
    print(f"  SKU: {producto['sku']}")
    print(f"  Nombre: {producto['nombre']}")
    print(f"  Stock actual: {producto['stock']} unidades")
    
    # Solicitar nuevo stock
    nuevo_stock = validar_numero("\nIngrese el nuevo stock: ", int, permitir_cero=True)
    
    # Actualizar el stock en el diccionario
    producto['stock'] = nuevo_stock
    
    print(f"\n{VERDE}✓ Stock actualizado: {producto['nombre']} - "
        f"Nuevo stock: {nuevo_stock} unidades{RESET}")


def eliminar_producto(productos, skus_usados):
    """
    Elimina un producto del inventario.    
    Args:
        productos (list): Lista de diccionarios de productos.
        skus_usados (set): Conjunto de SKUs para validación.
    """
    print(f"\n{CYAN}{NEGRITA}{'='*60}{RESET}")
    print(f"{AZUL}{'ELIMINAR PRODUCTO'.center(60)}{RESET}")
    print(f"{CYAN}{NEGRITA}{'='*60}{RESET}\n")
    
    if not productos:
        print(f"{AMARILLO}⚠ El inventario está vacío. No hay productos para eliminar.{RESET}")
        return
    
    # Búsqueda
    print(f"{AZUL}Ingrese nombre o SKU del producto a eliminar: {RESET}", end='')
    busqueda = input().strip()
    
    if not busqueda:
        print(f"{ROJO}Error: Debe ingresar un término de búsqueda.{RESET}")
        return
    
    coincidencias = buscar_producto(productos, busqueda)
    
    if not coincidencias:
        print(f"{AMARILLO}⚠ No se encontraron productos con '{busqueda}'.{RESET}")
        return
    
    # Si hay múltiples coincidencias, permitir seleccionar
    if len(coincidencias) > 1:
        indice = seleccionar_de_lista(coincidencias, "Se encontraron varios productos")
        if indice is None:
            print(f"{AMARILLO}⚠ Operación cancelada.{RESET}")
            return
        producto = coincidencias[indice]
    else:
        producto = coincidencias[0]
    
    # Muestra información del producto a eliminar
    print(f"\n{AMARILLO}Producto a eliminar:{RESET}")
    print(f"  SKU: {producto['sku']}")
    print(f"  Nombre: {producto['nombre']}")
    print(f"  Categoría: {producto['categoria']}")
    print(f"  Precio: {formatear_precio(producto['precio'])}")
    print(f"  Stock: {producto['stock']} unidades")
    
    # Solicita confirmación
    if confirmar_accion("\n¿Está seguro que desea eliminar este producto?"):
        nombre_eliminado = producto['nombre']
        
        # Elimina de la lista y del conjunto
        productos.remove(producto)
        skus_usados.discard(producto['sku'])
        
        print(f"\n{VERDE}✓ Producto '{nombre_eliminado}' eliminado exitosamente.{RESET}")
    else:
        print(f"\n{AMARILLO}⚠ Operación cancelada. El producto no fue eliminado.{RESET}")
