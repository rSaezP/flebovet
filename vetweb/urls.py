from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'vetweb'

urlpatterns = [
    # URLs principales
    path('', views.index, name='index'),
    path('productos/', views.lista_productos, name='productos'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('contacto/', views.contacto, name='contacto'),
    path('policies/', views.policies_view, name='policies'),
    
    # Autenticación y perfil
    path('auth/login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Productos y detalles
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('download/pdf/<int:producto_id>/', views.download_pdf, name='download_pdf'),
    
    # URLs del panel de administración
    path('panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('panel/productos/', views.admin_productos, name='admin_productos'),
    path('panel/productos/crear/', views.admin_producto_crear, name='admin_producto_crear'),
    path('panel/productos/<int:producto_id>/editar/', views.admin_producto_editar, name='admin_producto_editar'),
    path('panel/productos/<int:producto_id>/eliminar/', views.admin_producto_eliminar, name='admin_producto_eliminar'),
 
    # URLs de lista de deseos
    path('lista-deseos/', views.lista_deseos_view, name='lista_deseos_view'),
    
    path('lista-deseos/agregar/<int:producto_id>/', views.agregar_a_deseos, name='agregar_a_deseos'),
    path('lista-deseos/quitar/<int:producto_id>/', views.quitar_de_deseos, name='quitar_de_deseos'),
    
    # Reset de contraseña
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='vetweb/auth/password_reset_form.html',
            email_template_name='vetweb/auth/password_reset_email.html',
            success_url='/password_reset/done/'
        ),
        name='password_reset'),
    
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='vetweb/auth/password_reset_done.html'
        ),
        name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='vetweb/auth/password_reset_confirm.html',
            success_url='/password_reset/complete/'
        ),
        name='password_reset_confirm'),
    
    path('password_reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='vetweb/auth/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]


