from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, request
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import FileResponse
from .forms import CustomUserCreationForm
from functools import wraps
from .models import Producto, Carrito, CarritoItem, Orden, OrdenItem, UserProfile, ListaDeseos
from .decorators import admin_required
from django.http import JsonResponse
import os
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Producto, ListaDeseos
from django.shortcuts import render
from .models import Producto
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    static_root = settings.STATIC_ROOT
    static_dirs = settings.STATICFILES_DIRS
    css_path = os.path.join(settings.BASE_DIR, 'vetweb', 'static', 'vetweb', 'css', 'style.css')
    print(f"STATIC_ROOT: {static_root}")
    print(f"STATICFILES_DIRS: {static_dirs}")
    print(f"CSS Path exists: {os.path.exists(css_path)}")
    print(f"Full CSS Path: {css_path}")
    return render(request, 'vetweb/index.html')


def lista_productos(request):
    try:
        # Productos estáticos predefinidos
        productos_estaticos = [
            {
                'id': 1,
                'nombre': 'HV-COA 7100',
                'descripcion': 'Analizador de Coagulación Veterinaria',
                'imagen': 'producto1.png',
                'caracteristicas': [
                    'Rápido y Preciso',
                    'Resultados en minutos'
                ]
            },
             {
                'id': 2,
                'nombre': 'HV-FIA 3000',
                'descripcion': 'Analizador de Inmunofluorescencia Cuantitativo',
                'imagen': 'producto2.jpg',
                'caracteristicas': [
                    'T4, TSH, Cortisol, Hormonas',
                    'Resultados en 3-15 minutos',
                    'Almacena 1000 resultados'
                ]
            },
            {
                'id': 3,
                'nombre': 'Pointcare® PCR V1',
                'descripcion': 'Analizador PCR en tiempo real',
                'imagen': 'producto3.png',
                'caracteristicas': [
                    'Extracción libre de DNA/RNA',
                    'Resultados en 60 minutos',
                    '6 wells de procesamiento'
                ]
            },
            {
                'id': 4,
                'nombre': 'Test Rápidos',
                'descripcion': 'Diagnóstico Veterinario',
                'imagen': 'producto4.png',
                'caracteristicas': [
                    'CPV/CDV/FPV/FIV/otras pruebas',
                    'Resultados en 5-10 minutos',
                    'Alta sensibilidad y especificidad'
                ]
            },
            {
                'id': 5,
                'nombre': 'Pointcare V3',
                'descripcion': 'Analizador de Química Clínica y Electrolitos',
                'imagen': 'producto5.jpeg',
                'caracteristicas': [
                    'Perfil Hepático y Renal',
                    'Resultados en 7 minutos',
                    'Pantalla táctil 4.3"'
                ]
            }
        ]
        
            # ... resto de tus productos estáticos ...
        
        
        nombres_estaticos = ['HV-COA 7100', 'HV-FIA 3000', 'Pointcare® PCR V1', 'Test Rápidos', 'Pointcare V3']
        productos_dinamicos = Producto.objects.exclude(nombre__in=nombres_estaticos)
        
        # Obtener lista de deseos del usuario
        productos_en_deseos = []
        if request.user.is_authenticated:
            productos_en_deseos = ListaDeseos.objects.filter(
                user=request.user
            ).values_list('producto_id', flat=True)

        context = {
            'productos_estaticos': productos_estaticos,
            'productos_dinamicos': productos_dinamicos,
            'productos_en_deseos': list(productos_en_deseos),  # Convertir a lista
        }
        
        return render(request, 'vetweb/productos.html', context)
    except Exception as e:
        print(f"Error en lista_productos: {e}")
        return render(request, 'vetweb/productos.html', {'error': 'Ha ocurrido un error'})
   
def quienes_somos(request):
    return render(request, 'vetweb/quienes_somos.html') 

def contacto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
            asunto = request.POST.get('asunto')
            mensaje = request.POST.get('mensaje')
            
            mensaje_completo = f"""
            Nuevo mensaje de contacto:
            
            Nombre: {nombre}
            Email: {email}
            Asunto: {asunto}
            Mensaje: {mensaje}
            """
            
            send_mail(
                subject=f'Nuevo contacto: {asunto}',
                message=mensaje_completo,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            messages.success(request, '¡Gracias por contactarnos! Hemos recibido tu mensaje. Nuestro equipo se pondrá en contacto contigo lo antes posible.')
            return HttpResponseRedirect(reverse('vetweb:contacto') + '#')  # Agregamos # al final
            
        except Exception as e:
            messages.error(request, 'Error al enviar el mensaje. Por favor, intenta nuevamente.')
    
    return render(request, 'vetweb/contacto.html')


def policies_view(request):
    return render(request, 'vetweb/policies.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and hasattr(user, 'userprofile') and user.userprofile.role == 'ADMIN':
            login(request, user)
            return redirect('vetweb:admin_dashboard')
        else:
            messages.error(request, 'Credenciales inválidas o no tienes permisos de administrador')
            
    return render(request, 'vetweb/admin/login.html')

@login_required
def admin_dashboard(request):
    productos = Producto.objects.all()
    return render(request, 'vetweb/admin/dashboard.html', {'productos': productos})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Redirección basada en el tipo de usuario
                if user.is_staff or user.is_superuser:
                    return redirect('vetweb:admin_dashboard')
                return redirect('vetweb:index')
            else:
                messages.error(request, 'Tu cuenta está desactivada.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'vetweb/auth/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada exitosamente. Por favor revisa tu correo para activar tu cuenta.')
            return redirect('vetweb:login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'vetweb/auth/register.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Usuario registrado exitosamente! Puedes iniciar sesión ahora.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('vetweb:index')

@login_required
def profile_view(request):
    return render(request, 'vetweb/cliente/perfil.html')

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    context = {
        'producto': producto,
        'page_type': 'detalle_producto',  # Añadimos esto para identificar que estamos en la página de detalles
        'MEDIA_URL': settings.MEDIA_URL
    }
    
    return render(request, 'vetweb/detalle_producto.html', context)
  
@admin_required
def admin_dashboard(request):
    total_productos = Producto.objects.count()
    productos_sin_stock = Producto.objects.filter(stock=0).count()
    ultimos_productos = Producto.objects.order_by('-fecha_creacion')[:5]
    
    context = {
        'total_productos': total_productos,
        'productos_sin_stock': productos_sin_stock,
        'ultimos_productos': ultimos_productos,
    }
    
    return render(request, 'vetweb/admin/dashboard.html', context)

def download_pdf(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if not producto.pdf:
        raise Http404("PDF no disponible")
    
    response = FileResponse(
        producto.pdf.open(),
        filename=producto.pdf.name.split('/')[-1]
    )
    # Forzar el modo "inline" para visualización
    response['Content-Disposition'] = f'inline; filename="{producto.pdf.name.split("/")[-1]}"'
    return response

# ========= CORRECCIONES CRUD =========
@admin_required
def admin_productos(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'vetweb/admin/productos_admin.html', {'productos': productos})

@admin_required
def admin_producto_crear(request):
    if request.method == 'POST':
        try:
            # Crear el producto con los datos del formulario
            producto = Producto.objects.create(
                nombre=request.POST.get('nombre'),
                descripcion=request.POST.get('descripcion'),
                stock=request.POST.get('stock', 0),
                es_estatico=False  # Aseguramos que no sea estático
            )
            
            # Manejar la imagen si se proporcionó una
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
                producto.save()
            
            messages.success(request, 'Producto creado exitosamente')
            # Redirigir a la página de detalles del producto
            return redirect('vetweb:detalle_producto', producto_id=producto.id)
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')
            
    return render(request, 'vetweb/admin/producto_form.html', {
        'title': 'Nuevo Producto',
        'producto': None
    })
@admin_required
def admin_producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        try:
            producto.nombre = request.POST.get('nombre')
            producto.descripcion = request.POST.get('descripcion')
            producto.stock = request.POST.get('stock', 0)
            
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
            if 'pdf' in request.FILES:
                producto.pdf = request.FILES['pdf']
                
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('vetweb:admin_productos')
        except Exception as e:
            messages.error(request, f'Error al actualizar el producto: {str(e)}')
    return render(request, 'vetweb/admin/producto_form.html', {'producto': producto})

@admin_required
def admin_producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    try:
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
    except Exception as e:
        messages.error(request, f'Error al eliminar el producto: {str(e)}')
    return redirect('vetweb:admin_productos')

# ========= FIN CORRECCIONES CRUD =========

# Resto de tu código original intacto
@login_required
def carrito_ver(request):
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    return render(request, 'vetweb/cliente/carrito.html', {'carrito': carrito})

@login_required
def carrito_agregar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    
    carrito_item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )
    
    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()
    
    messages.success(request, 'Producto agregado al carrito')
    return redirect('vetweb:carrito_ver')

@login_required
def carrito_eliminar(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__user=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('vetweb:carrito_ver')

@login_required
def historial_compras(request):
    ordenes = Orden.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'vetweb/cliente/historial.html', {'ordenes': ordenes})


@login_required
def agregar_a_deseos(request, producto_id):
    print(f"DEBUG: Intento de agregar/quitar producto {producto_id}")
    
    if request.method == 'POST':
        try:
            producto = get_object_or_404(Producto, id=producto_id)
            deseo_existente = ListaDeseos.objects.filter(user=request.user, producto=producto).first()
            
            if deseo_existente:
                print(f"DEBUG: Eliminando producto {producto_id} de lista de deseos")
                deseo_existente.delete()
                in_wishlist = False
            else:
                print(f"DEBUG: Agregando producto {producto_id} a lista de deseos")
                ListaDeseos.objects.create(user=request.user, producto=producto)
                in_wishlist = True
            
            return JsonResponse({
                'success': True,
                'in_wishlist': in_wishlist
            })
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            return JsonResponse({'success': False}, status=400)
    
    return JsonResponse({'success': False}, status=405)
    
@login_required
def lista_deseos_view(request):
    deseos = ListaDeseos.objects.filter(user=request.user)
    return render(request, 'vetweb/cliente/lista_deseos.html', {
        'deseos': deseos
    })

@login_required
def quitar_de_deseos(request, producto_id):
    if request.method == 'POST':
        ListaDeseos.objects.filter(
            user=request.user,
            producto_id=producto_id
        ).delete()
        messages.success(request, 'Producto eliminado de tu lista de deseos')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Producto eliminado de tu lista de deseos'
            })
        
        return redirect('vetweb:lista_deseos_view')
    return redirect('vetweb:lista_deseos_view')

@login_required
def profile_view(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, role='CLIENT')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('vetweb:profile')
        
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'vetweb/cliente/perfil.html', context)