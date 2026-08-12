from django.db import models
from django.core.validators import MinValueValidator


class CategoriaProducto(models.Model):
    """Modelo POO que representa una categoría de productos o insumos."""
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True, default="")
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categorias_producto"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo,
        }


class LoteInventario(models.Model):
    """
    Modelo POO para control de lotes, stock, trazabilidad y estados.
    Encapsula reglas de negocio como cálculo de valor total y alerta de stock crítico.
    """
    ESTADOS = [
        ("DISPONIBLE", "Disponible"),
        ("EN_PROCESO", "En Proceso / Control Calidad"),
        ("DESPACHADO", "Despachado"),
    ]

    codigo_lote = models.CharField(max_length=30, unique=True)
    nombre_producto = models.CharField(max_length=120)
    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.PROTECT,
        related_name="lotes"
    )
    cantidad_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock_minimo_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=50.00,
        validators=[MinValueValidator(0)]
    )
    costo_unitario_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="DISPONIBLE")
    ubicacion_bodega = models.CharField(max_length=60, default="Cámara Frigorífica A1")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lotes_inventario"
        ordering = ["-fecha_registro"]

    def __str__(self) -> str:
        return f"[{self.codigo_lote}] {self.nombre_producto}"

    @property
    def valor_total_usd(self) -> float:
        """Calcula el valor económico del lote aplicando POO."""
        return round(float(self.cantidad_kg) * float(self.costo_unitario_usd), 2)

    @property
    def alerta_stock_bajo(self) -> bool:
        """Determina si el lote está por debajo del stock mínimo."""
        return float(self.cantidad_kg) <= float(self.stock_minimo_kg)

    def to_dict(self) -> dict:
        """Serializa la instancia a formato compatible con JSON / API REST."""
        return {
            "id": self.id,
            "codigo_lote": self.codigo_lote,
            "nombre_producto": self.nombre_producto,
            "categoria_id": self.categoria_id,
            "categoria_nombre": self.categoria.nombre if self.categoria_id else "General",
            "cantidad_kg": float(self.cantidad_kg),
            "stock_minimo_kg": float(self.stock_minimo_kg),
            "costo_unitario_usd": float(self.costo_unitario_usd),
            "valor_total_usd": self.valor_total_usd,
            "alerta_stock_bajo": self.alerta_stock_bajo,
            "estado": self.estado,
            "ubicacion_bodega": self.ubicacion_bodega,
            "fecha_registro": self.fecha_registro.strftime("%Y-%m-%d %H:%M") if self.fecha_registro else "",
        }
