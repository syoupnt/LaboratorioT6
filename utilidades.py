"""
utilidades.py - Validaciones reutilizables del sistema de prestamos LabTech.

Este modulo concentra las funciones que se usan en mas de una parte del
programa. Al guardarlas aqui se evita duplicar codigo (buena practica:
"evitar la duplicacion de codigo") y cualquier correccion se aplica una
sola vez y beneficia a todas las partes que lo importan.
"""


def validar_texto_no_vacio(mensaje):
    """Solicita un dato al usuario hasta que la entrada no este vacia.

    Entrada: mensaje que se muestra al usuario.
    Salida: texto escrito sin espacios al inicio/final.

    Se reutiliza en: registrar_equipo, registrar_prestamo y devolver_equipo.
    """
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  [Error] El dato no puede estar vacio. Intente de nuevo.")


def buscar_equipo(codigo, equipos):
    """Busca un equipo por su codigo (sin distinguir mayusculas/minusculas).

    Entrada: codigo escrito por el usuario y lista de equipos.
    Salida: el diccionario del equipo, o None si no existe.
    """
    for equipo in equipos:
        if equipo["codigo"].lower() == codigo.strip().lower():
            return equipo
    return None


def codigo_equipo_existe(codigo, equipos):
    """Indica si un codigo de equipo ya esta registrado en el catalogo.

    Se reutiliza para impedir codigos duplicados en el registro de equipos.
    """
    return buscar_equipo(codigo, equipos) is not None


def solicitar_codigo_equipo(equipos, mensaje="Codigo del equipo: "):
    """Pide un codigo de equipo y valida que exista en el catalogo.

    Entrada: lista de equipos y mensaje personalizado.
    Salida: tupla (codigo normalizado, diccionario del equipo).
    Repite la pregunta mientras el codigo no exista.

    Se reutiliza en: registrar_prestamo y devolver_equipo.
    """
    while True:
        codigo = validar_texto_no_vacio(mensaje)
        equipo = buscar_equipo(codigo, equipos)
        if equipo is not None:
            return codigo, equipo
        print("  [Error] El codigo no existe. Revise el listado de equipos.")


def seleccionar_opcion(mensaje, opciones_validas):
    """Valida que la opcion elegida este dentro del menu permitido.

    Entrada: mensaje y lista/tupla de opciones validas.
    Salida: la opcion elegida (texto).
    """
    while True:
        opcion = validar_texto_no_vacio(mensaje)
        if opcion in opciones_validas:
            return opcion
        print("  [Error] Opcion no valida. Opciones: "
              + ", ".join(opciones_validas))


def pedir_categoria(equipos, mensaje="Categoria: "):
    """Pide una categoria y muestra las existentes si el usuario no la sabe.

    Se reutiliza en el registro de equipos y en la consulta por categoria.
    """
    categorias = obtener_categorias(equipos)
    if categorias:
        print("  Categorias existentes: " + ", ".join(categorias))
    return validar_texto_no_vacio(mensaje)


def obtener_categorias(equipos):
    """Devuelve la lista ordenada de categorias distintas del catalogo."""
    return sorted({equipo["categoria"].lower() for equipo in equipos})
