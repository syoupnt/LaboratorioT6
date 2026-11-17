"""
equipos.py - Catalogo de equipos del laboratorio universitario LabTech.

Responsabilidad: registrar, buscar, listar y contar los equipos
disponibles. No conoce el menu ni los prestamos: solo maneja el
catalogo. Esto facilita probarlo y modificarlo por separado.
"""

from utilidades import buscar_equipo, codigo_equipo_existe, pedir_categoria
from utilidades import validar_texto_no_vacio

ESTADO_DISPONIBLE = "Disponible"
ESTADO_NO_DISPONIBLE = "No disponible"


def crear_equipo(codigo, nombre, categoria, estado=ESTADO_DISPONIBLE):
    """Crea la estructura de datos de un equipo (sin pedir datos por pantalla)."""
    return {
        "codigo": codigo.strip(),
        "nombre": nombre.strip(),
        "categoria": categoria.strip().lower(),
        "estado": estado,
    }


def registrar_equipo(equipos):
    """Pide los datos de un equipo y lo agrega al catalogo.

    Entrada: lista de equipos (se modifica por referencia).
    Salida: True si se registro, False si el codigo ya existia.
    """
    print("\n--- Registrar equipo ---")
    codigo = validar_texto_no_vacio("Codigo del equipo: ")
    if codigo_equipo_existe(codigo, equipos):
        print("  [Error] Ya existe un equipo con ese codigo.")
        return False

    nombre = validar_texto_no_vacio("Nombre del equipo: ")
    categoria = pedir_categoria(equipos, "Categoria: ")

    equipos.append(crear_equipo(codigo, nombre, categoria))
    print(f"  Equipo {codigo} '{nombre}' registrado correctamente.")
    return True


def listar_disponibilidad(equipos):
    """Muestra la tabla completa de equipos y su estado actual."""
    print("\n--- Listado de disponibilidad ---")
    if not equipos:
        print("  No hay equipos registrados.")
        return

    print(f"  {'CODIGO':<10}{'NOMBRE':<25}{'CATEGORIA':<15}{'ESTADO'}")
    print("  " + "-" * 60)
    for equipo in equipos:
        print(f"  {equipo['codigo']:<10}{equipo['nombre']:<25}"
              f"{equipo['categoria']:<15}{equipo['estado']}")

    disponibles = contar_equipos_disponibles(equipos)
    print(f"  Total: {len(equipos)} equipos | "
          f"{disponibles} disponibles | {len(equipos) - disponibles} prestados")


def contar_equipos_disponibles(equipos, categoria=None):
    """Cuenta los equipos disponibles, opcionalmente de una sola categoria.

    Entrada: lista de equipos y categoria opcional.
    Salida: cantidad entera de equipos con estado "Disponible".
    """
    return sum(
        1 for equipo in equipos
        if equipo["estado"] == ESTADO_DISPONIBLE
        and (categoria is None or equipo["categoria"] == categoria.lower())
    )


def consultar_disponibilidad_por_categoria(equipos):
    """Muestra cuantos equipos disponibles hay en cada categoria."""
    print("\n--- Disponibilidad por categoria ---")
    if not equipos:
        print("  No hay equipos registrados.")
        return

    from utilidades import obtener_categorias
    for categoria in obtener_categorias(equipos):
        total = sum(1 for e in equipos if e["categoria"] == categoria)
        disponibles = contar_equipos_disponibles(equipos, categoria)
        print(f"  {categoria:<15} {disponibles} de {total} disponibles")
