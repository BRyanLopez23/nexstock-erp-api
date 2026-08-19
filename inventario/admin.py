from django.contrib import admin
from .models import CategoriaProducto, LoteInventario


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activo", "creado_en")
    search_fields = ("nombre",)


@admin.register(LoteInventario)
class LoteInventarioAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_lote",
        "nombre_producto",
        "categoria",
        "cantidad_kg",
        "costo_unitario_usd",
        "estado",
        "ubicacion_bodega",
    )
    list_filter = ("estado", "categoria")
    search_fields = ("codigo_lote", "nombre_producto", "ubicacion_bodega")
