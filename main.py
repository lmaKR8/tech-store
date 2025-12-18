from inventario import cargar_inventario, guardar_inventario
from utils import mostrar_menu, confirmar_accion, AMARILLO, CYAN, ROJO, NEGRITA, RESET
from operaciones import (
    registrar_producto,
    visualizar_inventario,
    actualizar_stock,
    eliminar_producto,
)


def main():
    """
    Función principal que ejecuta el menú del sistema.
    """
    print(f"{CYAN}{NEGRITA}{'='*60}{RESET}")
    print(f"{AMARILLO}{NEGRITA}{'GESTIÓN DE INVENTARIO • TECHSTORE'.center(60)}{RESET}")
    print(f"{CYAN}{NEGRITA}{'='*60}{RESET}\n")

    # Carga el inventario al iniciar el programa
    datos = cargar_inventario()
    productos = datos[0]
    # Crea el set a partir de los productos cargados
    skus_usados = datos[1]
    
    # Menú
    while True:
        try:
            mostrar_menu()
            opcion = input(f"Seleccione una opción (1-6): ").strip()
            
            if opcion == "1":
                visualizar_inventario(productos)
            elif opcion == "2":
                registrar_producto(productos, skus_usados)
            elif opcion == "3":
                actualizar_stock(productos)
            elif opcion == "4":
                eliminar_producto(productos, skus_usados)
            elif opcion == "5":
                guardar_inventario(productos)
            elif opcion == "6":
                # Salir (confirma si desea guardar)
                print()
                if confirmar_accion("¿Desea guardar el inventario antes de salir?"):
                    guardar_inventario(productos)
                
                print(f"\n{CYAN}¡Gracias por usar TechStore!{RESET}\n")
                break
            else:
                print(f"{ROJO}Opción inválida. Por favor seleccione una opción del 1 al 6.{RESET}")
        
        except Exception as e:
            print(f"{ROJO}Error inesperado: {e}{RESET}")
            print(f"{CYAN}El programa continuará ejecutándose...{RESET}")


if __name__ == "__main__":
    """
    Punto de entrada del programa.
    """
    try:
        main()
    except KeyboardInterrupt:
        # Manejo de salida con Ctrl+C
        print(f"\n\n{CYAN}Programa interrumpido por el usuario. ¡Hasta pronto!{RESET}\n")
