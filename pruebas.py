"""
pruebas.py - Pruebas automatizadas del sistema de prestamos LabTech.

Ejecutar con:  python pruebas.py

Cubre los 6 casos exigidos por la guia:
  1. prestamo valido
  2. devolucion
  3. codigo inexistente
  4. equipo no disponible
  5. dato vacio
  6. listado (por categoria)
Ademas verifica el codigo duplicado, que es la regla extra del catalogo.

Las funciones de la guia piden datos por pantalla, por lo que se usa
unittest.mock.patch sobre "input" para simular al usuario y
contextlib.redirect_stdout para capturar lo que se imprime (evidencia).
"""

import io
from contextlib import redirect_stdout
from unittest.mock import patch

from equipos import ESTADO_DISPONIBLE, ESTADO_NO_DISPONIBLE
from equipos import consultar_disponibilidad_por_categoria, crear_equipo
from equipos import registrar_equipo
from prestamos import devolver_equipo, registrar_prestamo


def catalogo_base():
    """Catalogo pequeño y conocido para las pruebas."""
    return [
        crear_equipo("EQ001", "Laptop Dell 5420", "laptop"),
        crear_equipo("EQ002", "Laptop HP 250", "laptop"),
        crear_equipo("EQ003", "Mouse Logitech", "mouse"),
    ]


def ejecutar(entradas, funcion, *args):
    """Ejecuta una funcion simulando el teclado y captura su salida.

    Entrada: lista de respuestas del usuario, la funcion a probar y sus argumentos.
    Salida: tupla (resultado devuelto por la funcion, texto impreso).
    """
    salida = io.StringIO()
    with patch("builtins.input", side_effect=entradas):
        with redirect_stdout(salida):
            resultado = funcion(*args)
    return resultado, salida.getvalue()


def probar_prestamo_valido():
    """Caso 1: prestar un equipo disponible debe cambiar su estado."""
    equipos, prestamos = catalogo_base(), []
    resultado, texto = ejecutar(
        ["EQ001", "Ana Torres", "15/10/2026"],
        registrar_prestamo, equipos, prestamos)

    estado = equipos[0]["estado"]
    obtenido = (f"devolvio={resultado}, estado={estado}, "
                f"prestamos={len(prestamos)}")
    ok = (resultado is True and estado == ESTADO_NO_DISPONIBLE
          and len(prestamos) == 1
          and prestamos[0]["estudiante"] == "Ana Torres")
    return ok, obtenido, texto


def probar_devolucion():
    """Caso 2: la devolucion debe liberar el equipo y borrar el prestamo."""
    equipos, prestamos = catalogo_base(), []
    ejecutar(["EQ001", "Ana Torres", "15/10/2026"],
             registrar_prestamo, equipos, prestamos)

    resultado, texto = ejecutar(["EQ001"], devolver_equipo, equipos, prestamos)
    estado = equipos[0]["estado"]
    obtenido = (f"devolvio={resultado}, estado={estado}, "
                f"prestamos={len(prestamos)}")
    ok = (resultado is True and estado == ESTADO_DISPONIBLE
          and len(prestamos) == 0)
    return ok, obtenido, texto


def probar_codigo_inexistente():
    """Caso 3: un codigo inexistente debe rechazarse y volver a pedirse."""
    equipos, prestamos = catalogo_base(), []
    # El sistema debe rechazar EQ999 y aceptar EQ001 en la segunda pregunta.
    resultado, texto = ejecutar(
        ["EQ999", "EQ001", "Ana Torres", "15/10/2026"],
        registrar_prestamo, equipos, prestamos)

    rechazo = "El codigo no existe" in texto
    obtenido = (f"rechazo={rechazo}, luego_registro={resultado}, "
                f"prestamos={len(prestamos)}")
    ok = rechazo and resultado is True and len(prestamos) == 1
    return ok, obtenido, texto


def probar_equipo_no_disponible():
    """Caso 4: no se puede prestar dos veces el mismo equipo."""
    equipos, prestamos = catalogo_base(), []
    ejecutar(["EQ001", "Ana Torres", "15/10/2026"],
             registrar_prestamo, equipos, prestamos)

    resultado, texto = ejecutar(
        ["EQ001", "Luis Gomez", "16/10/2026"],
        registrar_prestamo, equipos, prestamos)

    rechazo = "no se puede prestar" in texto
    obtenido = (f"segundo_prestamo={resultado}, rechazo={rechazo}, "
                f"prestamos={len(prestamos)}, estudiante="
                f"{prestamos[0]['estudiante']}")
    ok = resultado is False and rechazo and len(prestamos) == 1
    return ok, obtenido, texto


def probar_dato_vacio():
    """Caso 5: un dato vacio debe rechazarse y volver a pedirse."""
    equipos = catalogo_base()
    # El nombre viene vacio: el sistema debe pedirlo de nuevo.
    resultado, texto = ejecutar(
        ["EQ010", "", "Teclado Mecanico", "mouse"],
        registrar_equipo, equipos)

    rechazo = "no puede estar vacio" in texto
    nombres = [e["nombre"] for e in equipos if e["codigo"] == "EQ010"]
    obtenido = (f"rechazo_vacio={rechazo}, registro={resultado}, "
                f"nombre_guardado={nombres[0] if nombres else 'Ninguno'}")
    ok = (resultado is True and rechazo
          and nombres == ["Teclado Mecanico"])
    return ok, obtenido, texto


def probar_listado_por_categoria():
    """Caso 6: el listado debe contar por categoria solo los disponibles."""
    equipos = catalogo_base()
    # Se presta una laptop para que el conteo cambie.
    prestamos = []
    ejecutar(["EQ001", "Ana Torres", "15/10/2026"],
             registrar_prestamo, equipos, prestamos)

    _resultado, texto = ejecutar([], consultar_disponibilidad_por_categoria,
                                 equipos)
    esperado = "laptop     1 de 2 disponibles"
    obtenido = (f"linea_laptop='{[l for l in texto.splitlines() if 'laptop' in l]}'")
    ok = esperado in texto and "mouse      1 de 1 disponibles" in texto
    return ok, obtenido, texto


def probar_codigo_duplicado():
    """Caso extra: no se permite registrar dos veces el mismo codigo."""
    equipos = catalogo_base()
    resultado, texto = ejecutar(
        ["EQ001", "Otra Laptop", "laptop"],
        registrar_equipo, equipos)

    rechazo = "Ya existe un equipo con ese codigo" in texto
    obtenido = (f"registro={resultado}, rechazo={rechazo}, "
                f"total_equipos={len(equipos)}")
    ok = resultado is False and rechazo and len(equipos) == 3
    return ok, obtenido, texto


PRUEBAS = [
    ("1. Prestamo valido",
     "EQ001 / Ana Torres / 15/10/2026",
     "Estado pasa a No disponible y se guarda 1 prestamo",
     probar_prestamo_valido),
    ("2. Devolucion",
     "Prestamo previo y luego codigo EQ001",
     "Estado vuelve a Disponible y la lista de prestamos queda vacia",
     probar_devolucion),
    ("3. Codigo inexistente",
     "EQ999 (luego EQ001)",
     "Rechaza con mensaje de error y vuelve a pedir el codigo",
     probar_codigo_inexistente),
    ("4. Equipo no disponible",
     "Prestar EQ001 dos veces",
     "El segundo prestamo se rechaza; solo queda 1 prestamo",
     probar_equipo_no_disponible),
    ("5. Dato vacio",
     "EQ010 / nombre vacio / Teclado Mecanico / mouse",
     "Rechaza el nombre vacio y vuelve a pedirlo",
     probar_dato_vacio),
    ("6. Listado por categoria",
     "Catalogo con 1 laptop prestada",
     "Muestra laptop 1 de 2 y mouse 1 de 1 disponibles",
     probar_listado_por_categoria),
    ("7. Codigo duplicado",
     "Registrar de nuevo EQ001",
     "Rechaza el registro y no aumenta el catalogo",
     probar_codigo_duplicado),
]


def main():
    """Ejecuta todas las pruebas y muestra la tabla de resultados."""
    resultados = []
    for nombre, entrada, esperado, funcion in PRUEBAS:
        try:
            ok, obtenido, _texto = funcion()
        except Exception as error:  # una falla inesperada tambien es evidencia
            ok, obtenido = False, f"Excepcion: {error}"
        resultados.append((nombre, entrada, esperado, obtenido,
                           "OK" if ok else "FALLA"))

    print("\n" + "=" * 100)
    print("TABLA DE PRUEBAS - Sistema de prestamos LabTech")
    print("=" * 100)
    for nombre, entrada, esperado, obtenido, estado in resultados:
        print(f"\nPrueba: {nombre}  ->  {estado}")
        print(f"  Entrada usada        : {entrada}")
        print(f"  Resultado esperado   : {esperado}")
        print(f"  Resultado obtenido   : {obtenido}")

    fallas = sum(1 for fila in resultados if fila[4] == "FALLA")
    print("\n" + "-" * 100)
    print(f"Total: {len(resultados)} pruebas | "
          f"{len(resultados) - fallas} correctas | {fallas} fallidas")
    return 1 if fallas else 0


if __name__ == "__main__":
    raise SystemExit(main())
