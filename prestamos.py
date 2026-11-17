"""
prestamos.py - Registro de prestamos y devoluciones de equipos LabTech.

Responsabilidad: aplicar las reglas del negocio:
  * solo se presta un equipo registrado en el catalogo;
  * un equipo ya prestado (estado "No disponible") no se puede volver a prestar;
  * al devolver, el equipo vuelve a estar "Disponible".

Reutiliza las validaciones de utilidades.py en lugar de reimplementarlas.
"""

from equipos import ESTADO_DISPONIBLE, ESTADO_NO_DISPONIBLE
from utilidades import solicitar_codigo_equipo, validar_texto_no_vacio


def registrar_prestamo(equipos, prestamos):
    """Registra un prestamo si el codigo existe y el equipo esta disponible.

    Entrada: lista de equipos y lista de prestamos activos.
    Salida: True si el prestamo se registro, False si no se cumplio alguna regla.
    """
    print("\n--- Registrar prestamo ---")
    codigo, equipo = solicitar_codigo_equipo(equipos)

    if equipo["estado"] != ESTADO_DISPONIBLE:
        print(f"  [Error] El equipo {codigo} tiene estado "
              f"'{equipo['estado']}'; no se puede prestar.")
        return False

    estudiante = validar_texto_no_vacio("Nombre del estudiante: ")
    fecha = validar_texto_no_vacio("Fecha del prestamo (dd/mm/aaaa): ")

    equipo["estado"] = ESTADO_NO_DISPONIBLE
    prestamos.append({
        "codigo": equipo["codigo"],
        "estudiante": estudiante,
        "fecha": fecha,
    })
    print(f"  Prestamo registrado: {equipo['codigo']} ({equipo['nombre']}) "
          f"-> {estudiante} - {fecha}")
    return True


def devolver_equipo(equipos, prestamos):
    """Marca un equipo como disponible y elimina su prestamo activo.

    Entrada: lista de equipos y lista de prestamos activos.
    Salida: True si hubo una devolucion, False si el equipo no estaba prestado.
    """
    print("\n--- Devolver equipo ---")
    codigo, equipo = solicitar_codigo_equipo(equipos)

    if equipo["estado"] == ESTADO_DISPONIBLE:
        print("  [Error] El equipo no tiene un prestamo activo.")
        return False

    for prestamo in prestamos:
        if prestamo["codigo"].lower() == codigo.strip().lower():
            prestamos.remove(prestamo)
            break

    equipo["estado"] = ESTADO_DISPONIBLE
    print(f"  Equipo {codigo} devuelto. Ahora esta disponible.")
    return True


def listar_prestamos_activos(prestamos):
    """Muestra los equipos prestados, a quien y desde que fecha."""
    print("\n--- Prestamos activos ---")
    if not prestamos:
        print("  No hay prestamos activos.")
        return

    print(f"  {'CODIGO':<10}{'ESTUDIANTE':<25}{'FECHA'}")
    print("  " + "-" * 45)
    for prestamo in prestamos:
        print(f"  {prestamo['codigo']:<10}{prestamo['estudiante']:<25}"
              f"{prestamo['fecha']}")
