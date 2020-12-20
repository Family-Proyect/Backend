from django.urls import path,include
from .views import *
from .api import *
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

api_patterns = [
    path('categorias_temas/',get_categorias),
    path('tema_by_id/',get_temaByID),
    path('tema_by_category/',get_temaByCategory),
    path('image_by_tema/',get_imageTema),
    path('videos_by_tema/',get_videoTema),
    path('temas_images_categoy/',get_temas_images),
    path('images_galeria/',get_imagesGaleria),
    path('contactanos/',post_contactanos),
    path('get_consejerias/',get_Consejerias),
    path('register/',register),
    path('tips/',get_tips),
    path('send_testimonios/',post_testimonios),
    path('get_testimonios/',get_testimonios),
    path('get_profile/', get_profile),
    path('update_profile/', update_profile),
    path('update_password/', update_password),

    path('updateImage/', update_image_profile),
    path('getNosotros/',get_nosotros ),


    path('login/',login),
    path('getPrincipalesTemas/',get_temasPrincipales),
    path('galeria_scroll/',get_scrollGaleria),
    path('recuperar_contrasenia/', recuperar_contrasenia,name='reset_pass'),
    path('registro/', registro,name='registro'),
]


urlpatterns = [
     path('', signup),
     path('index', content, name ='index'),
     path('signup', signup, name='signup'),
     path('logout', logout_view, name='logout'),
     path('recuperar-password', forgot_password,name='password'),#template
     path('recuperar_contrasenia_admin', recuperar_contrasenia_admin,name='reset_pass_admin'),#method
     #tema
     path('tema', vista_registrar_tema, name='registrar_tema'),
     path('tema_modificar', view_modificar_tema, name='modificar_tema'),
     path('tema_modificar/<int:pk>', modificar_tema, name='modificar_tema_pk'),
     path('tema_eliminar', view_eliminar_tema, name='eliminar_tema'),
     path('eliminar_tema_p', eliminar_tema_p, name='eliminar_tema_p'),
    #Tipos-Recomendaciones
     path('tips', view_registrar_tips, name='registrar_tips'),
     path('tips_modificar', view_modificar_tips, name='modificar_tips'),
     path('tips_modificar/<int:pk>', modificar_tips, name='modificar_tips_pk'),
     path('tips_eliminar', view_eliminar_tips, name='eliminar_tips'),
     path('eliminar_tips_p', eliminar_tips_p, name='eliminar_tips_p'),
     #galeria
     path('galeria', view_galeria, name='galeria'),
     path('galeria_eliminar', view_eliminar_galeria, name='hola'),
     path('eliminar_galeria_pk', eliminar_galeria, name='eliminar_galeria_p'),
     path('buzon', vista_buzon_entrada, name='buzon_entrada'),
     path('response_msg', send_email, name='response_contact'),
     path('eliminar_msg', eliminar_mensaje_buzon, name='eliminar_mensaje'),
     path('eliminar_consejeria', eliminar_consejeria, name='eliminarConsejeria'),

    #testimonios
    path('eliminar_testimonio', eliminar_testimonios, name='eliminarTestimonio'),
     path('eliminar_testimonio_pk', eliminar_testimonio_p, name='eliminar_testimonio_p'),
     path('validar_testimonio', validarTestimonio, name='response_testimonio'),

    


    #consejeria
     path('consjeria', vista_registrar_consejeria, name='registrar_consejeria'),
     path('modificar_consejeria', vista_modificar_consejeria, name='modificarConsejeria'),
     path('modificar_consejeria_dates', modificar_consejeria, name='moodifyconsejeria'),

     #Nosotros
     path('nosotros', view_registrar_nosotros, name='registrar_nosotros'),



     path('recibir_imagenes', recibir_imagenes),
     path('recibir_video', recibir_video, name='recibir_video'),
     #Api para el consumo en el frontend
     path('getPrincipalesTemas/', get_temasPrincipales),
     #autenticacion
     path(r'api-token-auth/', CustomAuthToken.as_view()),
     path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
     #api
     path('api/',include(api_patterns)),

]