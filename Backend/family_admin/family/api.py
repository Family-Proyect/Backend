from django.shortcuts import render
# Create your api rest here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import *
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import ObtainJSONWebToken
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage, BadHeaderError, send_mail, send_mass_mail


def get_tips(request):
    if request.method == 'GET':
        tips = Tips.objects.filter(estado=1).order_by('-fecha')
        return JsonResponse(list(tips.values()),safe=False)

def get_profile(request):
    if request.method == 'GET':
        user= request.GET.get("id")
        #response = json.loads(request.body)
        #profile= UserProfile.objects.get(username=response['user'])
        profile= UserProfile.objects.filter(username=user)
        print(profile.values())
        dic = dict()
        lista = list()
        for i in profile:
            dic['Nombre']=i.first_name
            dic['Apellido']=i.last_name
            dic['Email']=i.email
            dic['Edad']=i.edad
            dic['Username']=i.username
            dic['Sexo']='Masculino'
            dic['Image']=i.image.url

            lista.append(dic)
        return JsonResponse(dic,safe=False)

@csrf_exempt
def update_profile(request):
    print(request)
    print(json.loads(request.body))
    if request.method=="POST":
        response = json.loads(request.body)
        print(response)
        try:
            profile= UserProfile.objects.filter(username=response['user'])[0]
            profile.first_name= response['nombre']
            profile.last_name= response['apellido']
            profile.edad= response['edad']
            print(response['edad'])
            profile.email= response['email']
            profile.save()
        except Exception as e:
            print(e)
        print(response)
        return HttpResponse(status=200)
    return HttpResponse(status=404)

@csrf_exempt
def update_password(request):
    if request.method=="POST":
        response = json.loads(request.body)
        print(response)
        try:
            profile= UserProfile.objects.filter(username=response['user'])[0]
            profile.set_password(response['password'])  # replace with your real password
            print(response['password'])
            profile.save()
        except Exception as e:
            print(e)
        print(response)
        return HttpResponse(status=200)
    return HttpResponse(status=404)

@csrf_exempt
def update_image_profile(request):
    if request.method=="POST":
        print(request.POST['user'])
        print(request.FILES['file'])
        try:
            profile= UserProfile.objects.filter(username=request.POST['user'])[0]
            profile.image= request.FILES['file']
            profile.save()
        except Exception as e:
            print(e)
        return HttpResponse(status=200)
    return HttpResponse(status=404)
   

def get_temasPrincipales(request):
    if request.method=='GET':
        response = dict()
        temas = Tema.objects.all()
        categorias = Categoria_Tema.objects.all()
        print(categorias)
        temas_recientes = list()
        for categoria in categorias:
            print(categoria)
            _tema = temas.filter(tema_categoria=categoria,estado=1).order_by('-fecha').first()
            print(_tema)
            if _tema != None:
                imagen=Imagenes_Tema.objects.filter(id_tema=_tema.id_tema)[0]
                res = dict()
                res['titulo']=_tema.titulo
                res['id']=_tema.id_tema
                res['id_categoria']=_tema.tema_categoria.id_categoria_tema
                res['categoria']=_tema.tema_categoria.nombre_categoria
                res['image']=imagen.image.url
                temas_recientes.append(res)
        print(temas_recientes)
        return JsonResponse(temas_recientes,safe=False)

def get_testimonios(request):
    if request.method=='GET':
        testimonios = Testimonios.objects.all().values()
        return JsonResponse(list(testimonios),safe=False)

def get_categorias(request):
    if request.method=='GET':
        cetegorias = Categoria_Tema.objects.all().values()
        return JsonResponse(list(cetegorias), safe=False)

def get_temaByID(request):
    if request.method=='GET':
        id= request.GET.get("id")
        tema = Tema.objects.filter(id_tema=id).values()

        return JsonResponse(list(tema), safe=False)

def get_temaByCategory(request):
    if request.method=='GET':
        id_categoria= request.GET.get("id")
        temas = Tema.objects.filter(tema_categoria=id_categoria).order_by('-fecha').values()
        temas2= Tema.objects.filter(tema_categoria=id_categoria)
        images = Imagenes_Tema.objects.all()
        return JsonResponse(list(temas), safe=False)

def get_temas_images(request):
    if request.method=='GET':
        id_categoria= request.GET.get("id")
        temas2= Tema.objects.filter(tema_categoria=id_categoria).order_by('-fecha')
        images = Imagenes_Tema.objects.all()
        list_tema=[]
        for i in temas2:
            res = dict()
            res['titulo']=i.titulo
            res['categoria']=i.tema_categoria.id_categoria_tema
            res['id_tema']=i.id_tema
            res['images']=images.filter(id_tema=i.id_tema).first().image.url
            res['descripcion']=i.descripcion
            res['fecha']=i.fecha

            list_tema.append(res)

        return JsonResponse(list_tema, safe=False)

def get_imageTema(request):
    if request.method=='GET':
        _id= request.GET.get("id")
        images = Imagenes_Tema.objects.filter(id_tema=_id).values()
        print(images)
        return JsonResponse(list(images), safe=False)

def get_videoTema(request):
    if request.method=='GET':
        _id= request.GET.get("id")
        videos = Videos_Tema.objects.filter(id_tema=_id).values()
        print(videos)
        return JsonResponse(list(videos), safe=False)

def get_imagesGaleria(request):
    if request.method=='GET':
        img_galeria= Imagenes_galeria.objects.all().values('image')
        print(img_galeria)
        return JsonResponse(list(img_galeria), safe=False)



def get_Consejerias(request):
    if request.method=='GET':
        consejeria = Consejeria.objects.all()
        consejeria2 = Consejeria.objects.filter(estado=1).values()

        

        return JsonResponse(list(consejeria2), safe=False)



@csrf_exempt
def post_contactanos(request):
    if request.method=="POST":
        response = json.loads(request.body)
        try:
            contacanos= Contactanos(estado=False,titulo=response['title'],descripcion=response['description'],
            correo=response['email'],usuario=response['name'])
            contacanos.save()
        except Exception as e:
            print(e)
        print(response)
        return HttpResponse(status=200)
    return HttpResponse(status=404)

@csrf_exempt
def post_testimonios(request):
    if request.method=="POST":
        response = json.loads(request.body)
        try:
            testimonio= Testimonios(usuario=response['name'],titulo=response['title'],
            descripcion=response['description'],estado=0)
            testimonio.save()
        except Exception as e:
            print(e)
        print(response)
        return HttpResponse(status=200)
    return HttpResponse(status=404)

#API de Servicios de sugerencias
@csrf_exempt
def postCreateTipoSugerencia(request):
    if request.method=='POST':
        response = json.loads(request.body)
        #Aqui creo el elemento de tipo sugerencia
        tipo = Tipo_sugerencia(sugerencia=response["nuevaSugerencia"])
        tipo.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)

#API de Servicios de registrar ususario
@csrf_exempt
def register(request):
    if request.method=='POST':
        response = json.loads(request.body)
        #Aqui creo el usuario
        print(response["password"])
        user = UserProfile(username=response["username"],first_name=response["nombre"],last_name=response["apellido"],email=response["correo"],tipo="U")
        user.set_password(response["password"])
        user.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)

@csrf_exempt
def login(request):
    if request.method == "POST":
        response = json.loads(request.body)
        username = response["username"]
        password = response["password"]
        if(username!=None and password!=None):
            usuario = authenticate(username=username, password=password)
            if(usuario):
                return JsonResponse({"status":"true","usuario":usuario.first_name+" "+usuario.last_name}, safe=False)
            else:
                return JsonResponse({"status":"false"}, safe=False)
            return HttpResponse(status=404)
        return HttpResponse(status=404)
    return HttpResponse(status=404)

@csrf_exempt
def get_scrollGaleria(request):
    if request.method=='GET':
        page = int(request.GET.get("_page"))
        limit = int(request.GET.get("_limit"))
        img_galeria= Imagenes_galeria.objects.all().values('image')[page:limit]
        return JsonResponse(list(img_galeria), safe=False)

@csrf_exempt
def recuperar_contrasenia(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        correo = response["correo"]
        try:
            usuario = UserProfile.objects.get(email=correo)
            print(usuario)
        except UserProfile.DoesNotExist:
            usuario = None
            messages.add_message(request,messages.ERROR,'El correo ingresado no existe.!!')
            return JsonResponse({"status":"false"}, safe=False)
        
        new_password = UserProfile.objects.make_random_password()
        usuario.set_password(new_password)
        usuario.save()

        asunto = 'Cambio de contraseña Familias Unidas Ec'
        mensaje = 'Usted ha solicitado recuperación de contraseña su contraseña nueva es la siguiente: '+ new_password +" asegurese de cambiarla luego."
        nombres = usuario.username

        if nombres != '' and len(correo.split('@')) == 2 and mensaje != '':
            textomensaje = '<br>'
            lista = mensaje.split('\n')
            c = 0
            for i in lista:
                textomensaje += i+'</br>'
                c+=1
                if len(lista)  > c :
                    textomensaje += '<br>'
            msj = '<p><strong>IPSP :</strong>'+nombres+'</p><p><strong>Correo: </strong>'+correo+'</p><strong>Mensaje: </strong>'+textomensaje+'</p>'
            msj2 = msj+'<br/><br/><br/><p>Usted esta realizando el proceso de recuperacion de contraseña.</p><p><strong>NO RESPONDER A ESTE MENSAJE</strong>, nosotros nos pondremos en conacto con usted de ser necesario.</p><br/>'
            try:
                
                send_mail('Contactanos: '+asunto, msj,'familias.unidasEC@gmail.com', ['familias.unidasEC@gmail.com'], fail_silently=False, html_message = '<html><body>'+msj+'</body></html>')
                send_mail('Correo enviado: '+asunto, msj2, 'familias.unidasEC@gmail.com', [correo], fail_silently=False, html_message= '<html><body>'+msj2+'</body></html>')
            except BadHeaderError:
                return JsonResponse({"status":"false"}, safe=False)
            return JsonResponse({"status":"true"}, safe=False)

    return JsonResponse({"status":"false"}, safe=False)

@csrf_exempt
def registro(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        #verificar ususario
        if UserProfile.objects.filter(username=response["usuario"]).exists() or UserProfile.objects.filter(email=response["correo"]).exists():
            return JsonResponse({"status":"false"}, safe=False)
        else:
            user = UserProfile(username=response["usuario"],email=response["correo"],tipo="U")
            user.set_password(response["contraseña"])
            user.save()
            print(response)
        return JsonResponse({"status":"true"}, safe=False)
    return JsonResponse({"status":"false"}, safe=False)
