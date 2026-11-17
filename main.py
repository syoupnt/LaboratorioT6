"""
main.py - Programa principal del sistema de control de prestamos LabTech.

Responsabilidad: presentar el menu y coordinar los modulos.
Las funciones de negocio viven en equipos.py y prestamos.py, y las
validaciones compartidas en utilidades.py.

Ejecutar con:  python main.py
"""

from equipos import consultar_disponibilidad_por_categoria
from equipos import crear_equipo, listar_disponibilidad, registrar_equipo
from prestamos import devolver_equipo, listar_prestamos_activos
from prestamos import registrar_prestamo
from utilidades import codigo_equipo_existe, seleccionar_opcion

OPCIONES_MENU = ("1", "2", "3", "4", "5", "6", "7", "0")


def cargar_equipos_iniciales():
    """Catalogo de ejemplo para poder probar el sistema de inmediato.

    En un caso real estos datos se cargarian desde un archivo o base de datos.
    """
    return [
        crear_equipo("EQ001", "Laptop Dell 5420", "laptop"),
        crear_equipo("EQ002", "Laptop HP 250", "laptop"),
        crear_equipo("EQ003", "Adaptador USB-C", "adaptador"),
        crear_equipo("EQ004", "Mouse Logitech", "mouse"),
        crear_equipo("EQ005", "Cable HDMI 2 m", "cable hdmi"),
        crear_equipo("EQ006", "Kit basico practica", "kit basico"),
    ]


def mostrar_menu_principal():
    """Dibuja el menu principal (una sola funcion para todo el menu)."""
    print("\n" + "=" * 45)
    print("   SISTEMA DE PRESTAMOS LabTech")
    print("=" * 45)
    print("  1. Registrar equipo")
    print("  2. Prestar equipo")
    print("  3. Devolver equipo")
    print("  4. Listar disponibilidad")
    print("  5. Disponibilidad por categoria")
    print("  6. Listar prestamos activos")
    print("  7. Registrar equipo de ejemplo")
    print("  0. Salir")
    print("-" * 45)


def registrar_equipo_demo(equipos):
    """Agrega un equipo de ejemplo (solo para demostracion/pruebas)."""
    equipo = crear_equipo("EQ900", "Tablet Lenovo", "laptop")
    if codigo_equipo_existe(equipo["codigo"], equipos):
        print("  El equipo de ejemplo ya fue agregado antes.")
        return
    equipos.append(equipo)
    print("  Equipo de ejemplo EQ900 agregado.")


def ejecutar_opcion(opcion, equipos, prestamos):
    """Ejecuta la funcion que corresponde a la opcion elegida."""
    if opcion == "1":
        registrar_equipo(equipos)
    elif opcion == "2":
        registrar_prestamo(equipos, prestamos)
    elif opcion == "3":
        devolver_equipo(equipos, prestamos)
    elif opcion == "4":
        listar_disponibilidad(equipos)
    elif opcion == "5":
        consultar_disponibilidad_por_categoria(equipos)
    elif opcion == "6":
        listar_prestamos_activos(prestamos)
    elif opcion == "7":
        registrar_equipo_demo(equipos)


def main():
    """Bucle principal del programa."""
    equipos = cargar_equipos_iniciales()
    prestamos = []
    print("Bienvenido al control de prestamos del laboratorio LabTech.")

    while True:
        mostrar_menu_principal()
        opcion = seleccionar_opcion("Seleccione una opcion: ", OPCIONES_MENU)
        if opcion == "0":
            print("Sesion finalizada. Hasta luego.")
            break
        ejecutar_opcion(opcion, equipos, prestamos)


if __name__ == "__main__":
    main()
