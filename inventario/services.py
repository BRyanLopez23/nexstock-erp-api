"""
Módulo de Servicios y Lógica de Negocio (POO + Estructuras de Datos).
Implementa validaciones, filtros, estadísticas y serialización para la API REST.
"""
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from .models import CategoriaProducto, LoteInventario


class InventarioService:
    """
    Clase de servicio que encapsula las operaciones CRUD, consultas SQL/ORM
    y métricas analíticas del inventario empresarial.
    """

    @staticmethod
    def inicializar_datos_demo() -> None:
        """Crea categorías y productos de demostración si la base de datos está vacía."""
        if CategoriaProducto.objects.exists():
            return

        cat_hardware = CategoriaProducto.objects.create(
            nombre="Equipos & Hardware TI",
            descripcion="Laptops corporativas, servidores, monitores y periféricos"
        )
        cat_redes = CategoriaProducto.objects.create(
            nombre="Infraestructura & Redes",
            descripcion="Routers, switches gestionables, cableado estructurado y sensores IoT"
        )
        cat_suministros = CategoriaProducto.objects.create(
            nombre="Almacén & Logística",
            descripcion="Insumos operativos, lectores de código de barras y consumibles"
        )

        lotes_iniciales = [
            {
                "codigo_lote": "SKU-2026-101",
                "nombre_producto": "Workstation Laptop Pro 16GB RAM / 512GB NVMe",
                "categoria": cat_hardware,
                "cantidad_kg": Decimal("42.00"),
                "stock_minimo_kg": Decimal("15.00"),
                "costo_unitario_usd": Decimal("980.00"),
                "estado": "DISPONIBLE",
                "ubicacion_bodega": "Almacén Central - Rack A1",
            },
            {
                "codigo_lote": "SKU-2026-102",
                "nombre_producto": "Switch Gigabit Administrable L3 24 Puertos PoE",
                "categoria": cat_redes,
                "cantidad_kg": Decimal("18.00"),
                "stock_minimo_kg": Decimal("10.00"),
                "costo_unitario_usd": Decimal("340.50"),
                "estado": "DISPONIBLE",
                "ubicacion_bodega": "Almacén Central - Rack B2",
            },
            {
                "codigo_lote": "SKU-2026-103",
                "nombre_producto": "Terminal Escáner Láser Inalámbrico Industrial",
                "categoria": cat_suministros,
                "cantidad_kg": Decimal("8.00"),
                "stock_minimo_kg": Decimal("12.00"),
                "costo_unitario_usd": Decimal("145.00"),
                "estado": "EN_PROCESO",
                "ubicacion_bodega": "Zona Control Calidad - C1",
            },
            {
                "codigo_lote": "SKU-2026-104",
                "nombre_producto": "Monitor IPS UltraWide 27'' FHD Ergonómico",
                "categoria": cat_hardware,
                "cantidad_kg": Decimal("9.00"),
                "stock_minimo_kg": Decimal("15.00"),
                "costo_unitario_usd": Decimal("215.00"),
                "estado": "DISPONIBLE",
                "ubicacion_bodega": "Centro Distribución Norte - D4",
            },
        ]

        for data in lotes_iniciales:
            LoteInventario.objects.create(**data)

    @classmethod
    def listar_lotes(cls, busqueda: str = "", estado: str = "", categoria_id: str = "") -> list[dict]:
        """Consulta filtrada de ítems utilizando ORM / SQL."""
        cls.inicializar_datos_demo()
        queryset = LoteInventario.objects.select_related("categoria").all()

        if busqueda:
            queryset = queryset.filter(
                Q(codigo_lote__icontains=busqueda)
                | Q(nombre_producto__icontains=busqueda)
                | Q(ubicacion_bodega__icontains=busqueda)
            )
        if estado:
            queryset = queryset.filter(estado=estado)
        if categoria_id and categoria_id.isdigit():
            queryset = queryset.filter(categoria_id=int(categoria_id))

        return [lote.to_dict() for lote in queryset]

    @classmethod
    def calcular_resumen_kpis(cls) -> dict:
        """Calcula indicadores clave (KPIs) recorriendo la colección de inventario."""
        lotes = cls.listar_lotes()
        total_lotes = len(lotes)
        total_unidades = round(sum(item["cantidad_kg"] for item in lotes), 2)
        valor_inventario = round(sum(item["valor_total_usd"] for item in lotes), 2)
        alertas_stock = sum(1 for item in lotes if item["alerta_stock_bajo"])

        return {
            "total_lotes": total_lotes,
            "total_kg": total_unidades,
            "valor_inventario_usd": valor_inventario,
            "alertas_stock_bajo": alertas_stock,
        }

    @staticmethod
    def validar_y_guardar_lote(payload: dict, lote_id: int | None = None) -> LoteInventario:
        """Valida los campos del JSON recibido y crea o actualiza un registro."""
        campos_requeridos = ["codigo_lote", "nombre_producto", "categoria_id", "cantidad_kg", "costo_unitario_usd"]
        for campo in campos_requeridos:
            if campo not in payload or str(payload[campo]).strip() == "":
                raise ValueError(f"El campo '{campo}' es obligatorio.")

        try:
            cantidad = Decimal(str(payload["cantidad_kg"]))
            costo = Decimal(str(payload["costo_unitario_usd"]))
            stock_min = Decimal(str(payload.get("stock_minimo_kg", "10.00")))
        except (InvalidOperation, TypeError) as exc:
            raise ValueError("Los valores numéricos de cantidad o costo no son válidos.") from exc

        if cantidad < 0 or costo < 0:
            raise ValueError("La cantidad y el costo unitario no pueden ser negativos.")

        categoria = CategoriaProducto.objects.filter(id=int(payload["categoria_id"])).first()
        if not categoria:
            raise ValueError("La categoría seleccionada no existe.")

        if lote_id:
            lote = LoteInventario.objects.filter(id=lote_id).first()
            if not lote:
                raise LookupError("El registro solicitado no fue encontrado.")
        else:
            if LoteInventario.objects.filter(codigo_lote=payload["codigo_lote"].strip()).exists():
                raise ValueError("Ya existe un producto con ese código SKU/Lote.")
            lote = LoteInventario()

        lote.codigo_lote = payload["codigo_lote"].strip().upper()
        lote.nombre_producto = payload["nombre_producto"].strip()
        lote.categoria = categoria
        lote.cantidad_kg = cantidad
        lote.stock_minimo_kg = stock_min
        lote.costo_unitario_usd = costo
        lote.estado = payload.get("estado", "DISPONIBLE")
        lote.ubicacion_bodega = payload.get("ubicacion_bodega", "Almacén Central - Rack A1").strip()
        lote.save()
        return lote
