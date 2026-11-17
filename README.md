# Laboratorio T6 — Sistema de préstamos LabTech

Práctica de laboratorio del curso **Fundamentos de Programación**, Tema N° 6:
*Introducción a la programación modular y reutilización*.
Programa de consola en **Python 3** para controlar el préstamo de equipos del
laboratorio ficticio **LabTech** (laptops, adaptadores, mouse, cables HDMI y kits),
organizado en módulos reutilizables y documentado con pruebas.

## Estructura del proyecto

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Menú principal y coordinación de los módulos |
| `equipos.py` | Catálogo: registrar, listar, contar y consultar disponibilidad por categoría |
| `prestamos.py` | Reglas de negocio: registrar préstamo y devolver equipo |
| `utilidades.py` | Validaciones reutilizadas por todos los módulos |
| `pruebas.py` | 7 pruebas automatizadas con `unittest.mock` |

Cada módulo tiene una responsabilidad única (alta cohesión) y se comunica con los
demás mediante parámetros e importaciones explícitas (bajo acoplamiento).

## Ejecución

```bash
python main.py      # programa interactivo (menú 1-6 y 0 para salir)
python pruebas.py   # ejecuta las pruebas; termina con código 0 si todo pasa
```

El catálogo de ejemplo (`EQ001`…`EQ006`) se carga automáticamente al iniciar;
los datos viven en memoria y se pierden al salir del programa.

## Reglas implementadas

- Registrar equipos con código, nombre, categoría y estado.
- Registrar préstamo indicando código de equipo, estudiante y fecha simple.
- Validar que el código de equipo exista antes de prestar.
- No prestar un equipo cuyo estado sea `No disponible`.
- Devolver un equipo y liberarlo para nuevos préstamos.
- Consultar la cantidad de equipos disponibles por categoría.
- Rechazar códigos duplicados en el registro de equipos.

## Reutilización

- `utilidades.validar_texto_no_vacio()` → se usa en `equipos.py`, `prestamos.py` y `utilidades.py`.
- `utilidades.solicitar_codigo_equipo()` → se usa en `prestamos.registrar_prestamo()` y `prestamos.devolver_equipo()`.
- `utilidades.buscar_equipo()` → se usa en cuatro puntos del programa.
- `equipos.contar_equipos_disponibles()` → se usa en el listado total y en el conteo por categoría.

## Pruebas

`python pruebas.py` cubre los seis casos exigidos por la guía más un caso adicional:

1. Préstamo válido 2. Devolución 3. Código inexistente 4. Equipo no disponible
5. Dato vacío 6. Listado por categoría 7. Código duplicado (adicional)

Cada prueba registra entrada usada, resultado esperado y resultado obtenido.
