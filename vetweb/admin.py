from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'stock', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['stock', 'fecha_creacion']
    fieldsets = [
        (None, {'fields': ['nombre', 'descripcion']}),
        ('Archivos', {'fields': ['imagen', 'pdf']}),
        ('Inventario', {'fields': ['stock']}),
    ]
    