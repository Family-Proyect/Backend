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
                return JsonResponse({"status":"true"}, safe=False)
            else:
                return JsonResponse({"status":"false"}, safe=False)
            return HttpResponse(status=404)
        return HttpResponse(status=404)
    return HttpResponse(status=404)