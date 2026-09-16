"""
Suite de Algoritmos, Estructuras de Datos y Programación Orientada a Objetos (POO).
Autor: Bryan Francisco López León (github.com/BRyanLopez23)

Este módulo demuestra la resolución práctica de problemas de lógica,
estructuras de datos en memoria (Cola FIFO, Árbol Binario de Búsqueda y Tabla Hash)
y organización limpia del código para gestión de lotes.
"""
from dataclasses import dataclass
from collections import deque


@dataclass
class NodoLote:
    """Representa un lote dentro de una estructura de datos."""
    codigo: str
    producto: str
    cantidad_kg: float
    prioridad: int = 1


class ColaDespachoFIFO:
    """
    Estructura de Datos: Cola (Queue - FIFO) para gestionar el orden de despacho
    de lotes garantizando trazabilidad (First-In, First-Out).
    """

    def __init__(self) -> None:
        self._cola: deque[NodoLote] = deque()

    def encolar_lote(self, lote: NodoLote) -> None:
        self._cola.append(lote)

    def atender_siguiente(self) -> NodoLote | None:
        if not self._cola:
            return None
        return self._cola.popleft()

    def total_pendientes(self) -> int:
        return len(self._cola)


def busqueda_binaria_lote(lotes_ordenados: list[dict], codigo_objetivo: str) -> dict | None:
    """
    Algoritmo de Búsqueda Binaria O(log n) sobre una lista de lotes
    ordenada alfabéticamente por 'codigo_lote'.
    """
    izquierda = 0
    derecha = len(lotes_ordenados) - 1
    objetivo = codigo_objetivo.strip().upper()

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        actual = lotes_ordenados[medio]["codigo_lote"].upper()

        if actual == objetivo:
            return lotes_ordenados[medio]
        if actual < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None


def agrupar_stock_por_categoria(lotes: list[dict]) -> dict[str, dict]:
    """
    Algoritmo de agregación O(n) utilizando tablas hash (diccionarios)
    para resumir kilogramos y valor total por categoría.
    """
    resumen: dict[str, dict] = {}
    for lote in lotes:
        cat = lote.get("categoria_nombre", "Sin Categoría")
        if cat not in resumen:
            resumen[cat] = {"cantidad_lotes": 0, "total_kg": 0.0, "valor_usd": 0.0}

        resumen[cat]["cantidad_lotes"] += 1
        resumen[cat]["total_kg"] = round(resumen[cat]["total_kg"] + float(lote["cantidad_kg"]), 2)
        resumen[cat]["valor_usd"] = round(resumen[cat]["valor_usd"] + float(lote["valor_total_usd"]), 2)

    return resumen


if __name__ == "__main__":
    # Ejecución rápida de prueba y verificación (Debugging)
    muestra = [
        {"codigo_lote": "LOT-2026-001", "categoria_nombre": "Congelados", "cantidad_kg": 500, "valor_total_usd": 2700},
        {"codigo_lote": "LOT-2026-002", "categoria_nombre": "Congelados", "cantidad_kg": 300, "valor_total_usd": 1950},
        {"codigo_lote": "LOT-2026-003", "categoria_nombre": "Insumos", "cantidad_kg": 80, "valor_total_usd": 144},
    ]
    encontrado = busqueda_binaria_lote(muestra, "LOT-2026-002")
    print("Resultado búsqueda binaria O(log n):", encontrado)
    print("Resumen agrupado O(n):", agrupar_stock_por_categoria(muestra))
