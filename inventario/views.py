"""
Controladores de Vistas y Endpoints API REST / JSON con Autenticación y Seguridad.
Autor: Bryan Francisco López León
"""
import json
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from .models import CategoriaProducto, LoteInventario
from .services import InventarioService


def dashboard_view(request: HttpRequest) -> HttpResponse:
    """Renderiza la aplicación SPA (HTML5 + CSS3 Responsivo + Vue.js 3)."""
    InventarioService.inicializar_datos_demo()
    return render(request, "index.html")


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request: HttpRequest) -> JsonResponse:
    """Endpoint de autenticación de usuarios y seguridad de sesión."""
    try:
        body = json.loads(request.body.decode("utf-8"))
        username = body.get("username", "").strip()
        password = body.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                "ok": True,
                "mensaje": "Autenticación exitosa",
                "usuario": {"username": user.username, "es_admin": user.is_staff}
            })

        # Modo demostración para pruebas rápidas
        if username == "admin" and password == "nexstock2026":
            request.session["demo_authenticated"] = True
            request.session["demo_user"] = "admin"
            return JsonResponse({
                "ok": True,
                "mensaje": "Sesión iniciada correctamente (Modo Demo)",
                "usuario": {"username": "admin", "es_admin": True}
            })

        return JsonResponse({"ok": False, "error": "Credenciales inválidas."}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Formato JSON inválido."}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request: HttpRequest) -> JsonResponse:
    """Cierra la sesión activa del usuario."""
    logout(request)
    request.session.flush()
    return JsonResponse({"ok": True, "mensaje": "Sesión finalizada."})


@require_http_methods(["GET"])
def api_categorias(request: HttpRequest) -> JsonResponse:
    """Retorna la lista de categorías disponibles en formato JSON."""
    InventarioService.inicializar_datos_demo()
    categorias = [cat.to_dict() for cat in CategoriaProducto.objects.filter(activo=True)]
    return JsonResponse({"ok": True, "categorias": categorias})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_lotes_coleccion(request: HttpRequest) -> JsonResponse:
    """
    GET: Lista todos los lotes aplicando filtros de búsqueda, categoría y estado + KPIs.
    POST: Registra un nuevo lote validando tipos y reglas de negocio.
    """
    if request.method == "GET":
        busqueda = request.GET.get("q", "").strip()
        estado = request.GET.get("estado", "").strip()
        categoria_id = request.GET.get("categoria_id", "").strip()

        lotes = InventarioService.listar_lotes(busqueda, estado, categoria_id)
        kpis = InventarioService.calcular_resumen_kpis()
        return JsonResponse({
            "ok": True,
            "kpis": kpis,
            "total_resultados": len(lotes),
            "lotes": lotes,
        })

    # POST: Crear nuevo lote
    try:
        payload = json.loads(request.body.decode("utf-8"))
        nuevo_lote = InventarioService.validar_y_guardar_lote(payload)
        return JsonResponse({
            "ok": True,
            "mensaje": "Lote registrado exitosamente.",
            "lote": nuevo_lote.to_dict()
        }, status=201)
    except ValueError as err:
        return JsonResponse({"ok": False, "error": str(err)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Cuerpo JSON mal formado."}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_lote_detalle(request: HttpRequest, lote_id: int) -> JsonResponse:
    """
    GET: Obtiene el detalle de un lote por ID.
    PUT: Actualiza los datos de un lote existente.
    DELETE: Elimina un lote del inventario.
    """
    lote = LoteInventario.objects.select_related("categoria").filter(id=lote_id).first()
    if not lote:
        return JsonResponse({"ok": False, "error": "Lote no encontrado."}, status=404)

    if request.method == "GET":
        return JsonResponse({"ok": True, "lote": lote.to_dict()})

    if request.method == "PUT":
        try:
            payload = json.loads(request.body.decode("utf-8"))
            lote_actualizado = InventarioService.validar_y_guardar_lote(payload, lote_id=lote_id)
            return JsonResponse({
                "ok": True,
                "mensaje": "Lote actualizado correctamente.",
                "lote": lote_actualizado.to_dict()
            })
        except (ValueError, LookupError) as err:
            return JsonResponse({"ok": False, "error": str(err)}, status=400)

    # DELETE
    codigo = lote.codigo_lote
    lote.delete()
    return JsonResponse({
        "ok": True,
        "mensaje": f"Lote {codigo} eliminado correctamente."
    })
