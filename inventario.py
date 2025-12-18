import json
import shutil
import os
from utils import VERDE, ROJO, AMARILLO, RESET

# Rutas de los archivos de inventario
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_INVENTARIO = os.path.join(DIRECTORIO_BASE, 'inventario', 'inventario.txt')
RUTA_BACKUP = os.path.join(DIRECTORIO_BASE, 'inventario', 'inventario_backup.txt')


def cargar_inventario():
    """
    - Carga el inventario desde el archivo inventario.txt
    - Si el archivo no existe, retorna una lista vacía y un set vacío.
    - Si el archivo está corrupto, crea un respaldo y retorna una lista vacía y un set vacío.
    Returns:
        tuple: (lista de productos, set de SKUs usados)
    Raises:
        FileNotFoundError: Si el archivo inventario.txt no existe.
        json.JSONDecodeError: Si el archivo está corrupto o tiene formato inválido.
    """
    try:
        with open(RUTA_INVENTARIO, 'r', encoding='utf-8') as f:
            productos = json.load(f)
            # Almacena los SKUs usados para validaciones
            skus_usados = set()
            
            # Itera sobre cada producto y agrega su SKU al set
            for producto in productos:
                skus_usados.add(producto['sku'])
            
            print(f"{VERDE}✓ Inventario cargado exitosamente: {len(productos)} productos.{RESET}")
            return productos, skus_usados
    
    except FileNotFoundError:
        print(f"{AMARILLO}⚠ Archivo no encontrado. Iniciando con inventario vacío.{RESET}")
        return [], set()
    
    except json.JSONDecodeError:
        print(f"{ROJO}✗ Error: Archivo inventario.txt corrupto.{RESET}")

        try:
            # Crear respaldo del archivo corrupto
            shutil.copy2(RUTA_INVENTARIO, RUTA_BACKUP)
            print(f"{AMARILLO}Respaldo creado en inventario_backup.txt{RESET}")

        except Exception as e:
            print(f"{ROJO}✗ No se pudo crear el respaldo: {e}{RESET}")
        
        print(f"{AMARILLO}⚠ Iniciando con inventario vacío.{RESET}")
        return [], set()


def guardar_inventario(productos):
    """
    Guarda el inventario en el archivo inventario/inventario.txt en formato JSON.
    Args:
        productos (list): Lista de diccionarios con los productos a guardar.
    Raises:
        Exception: Si ocurre un error al guardar el archivo.
    """
    try:
        with open(RUTA_INVENTARIO, 'w', encoding='utf-8') as f:
            # Guarda los productos en formato JSON con indentación
            json.dump(productos, f, indent=2, ensure_ascii=False)
        print(f"{VERDE}✓ Inventario guardado exitosamente en inventario.txt{RESET}")

    except Exception as e:
        print(f"{ROJO}✗ Error al guardar el inventario: {e}{RESET}")
