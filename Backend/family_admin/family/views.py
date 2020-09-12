from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from .models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.mail import EmailMessage, BadHeaderError, send_mail, send_mass_mail
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def content(request):
    return render(request, 'views/contenido.html')
@login_required(login_url='/')
def view_eliminar_galeria(request):
    imagenes = Imagenes_galeria.objects.filter(id_galeria=1)#solo hay una galeria
    categorias = Categoria_Tema.objects.all()

    print(imagenes)
    return render(request, 'views/galeria/eliminar_galeria.html',{'imagenes':imagenes})
@login_required(login_url='/')
def eliminar_galeria(request):
    imagenes = Imagenes_galeria.objects.filter(id_galeria=1) #solo hay una galeria
    image = Imagenes_galeria.objects.get(id=request.POST['galeria_id'])   #solo hay una galeria
    image.delete()
    return redirect('hola')

   #return render(request, 'views/galeria/eliminar_galeria.html',{'imagenes':imagenes})
@login_required(login_url='/')
def vista_buzon_entrada(request):
    return render(request, 'notificaciones/buzon_entrada.html')


@login_required(login_url='/')
def vista_registrar_tema(request):
    categorias = Categoria_Tema.objects.all()
    if(request.method == 'POST'):
        try:
            #Esteado enum 1:Aprobado, 2:Pendiente
            cate_tema = Categoria_Tema.objects.get(nombre_categoria=request.POST['categoria'])
            tema = Tema(estado=request.POST['estado'],
                        titulo=request.POST['titulo'],
                        tema_categoria=cate_tema,
                        descripcion=request.POST['descripcion'],
                        )
            if request.POST['fecha'] != '' :
                tema.fecha=request.POST['fecha']   
            tema.save()
                        
            #Esta podria ser la imagen que se muestra en el index del portal web
            imagen_tema_1 = Imagenes_Tema(id_tema=tema)
            imagen_tema_1.image = request.FILES['imagen1']
            #imagen_tema_1.save()
            #Esta podria ser la imagen que se muestra una vez que le de click en el tema
            imagen_tema_2 = Imagenes_Tema(id_tema=tema)
            imagen_tema_2.image = request.FILES['imagen2']
            #imagen_tema_2.save()

            #Video: Este se muestra una vez que entre en el tema
            vide_tema = Videos_Tema(id_tema=tema)
            vide_tema.video = request.FILES['video']
            #vide_tema.save()


            #Que suba audio podria ser opcional (Casi a nadie le gusta estar oyendo audio de internet)
            messages.add_message(request, messages.SUCCESS, 'Tema guardado exitosamente.')
        except Exception as e :
            print("Errors -> ", e)
            messages.add_message(request,messages.ERROR,'Error al guardar el tema.')
        #notificaciones(request.POST['titulo'])
        return redirect('registrar_tema') #registrar_tema es la version corta de views/registros/registrar_tema.html

    return render(request, 'views/registros/registrar_tema.html',{'categorias':categorias,"estado":Tema.Estado})

@login_required(login_url='/')
def view_modificar_tema(request):
    All_temas = Tema.objects.all()
    categorias = Categoria_Tema.objects.all()
    return render(request, 'views/modificaciones/modificar_tema.html',{'temas':All_temas,'categorias':categorias,"estado":Tema.Estado})


# request.POST.get('categoria') retorna none si no contiene ningun elemento para option
# request.POST['categoria']
@csrf_exempt
@login_required(login_url='/')
def modificar_tema(request,pk):
    All_temas = Tema.objects.all()
    categorias = Categoria_Tema.objects.all()
    # print("X->",request.POST['categoria'])

    try:
        tema = Tema.objects.get(id_tema=pk)
        if request.method == 'POST':
            tema.titulo= request.POST['titulo']
            tema.descripcion=request.POST['descripcion']
            if request.POST.get('categoria')!=None:
                tema.tema_categoria= request.POST.get('categoria')
                print("cate->",request.POST['categoria'])
            if request.POST['fecha']!="":
                tema.fecha=request.POST['fecha']
                print("X->",request.POST['fecha'])
            if request.POST.get('estado')!=None:
                tema.estado=request.POST['estado']
            print("X->",request.POST.get('estado'))

        #Verifico si envian imagen, si existe procedo a guardar            
            if bool(request.FILES.get('imagen1')) == True :
                print("img1")
                imagenes_tema = Imagenes_Tema.objects.filter(id_tema=pk)[0]
                imagenes_tema.image=request.FILES['imagen1']
                imagenes_tema.save()
            if bool(request.FILES.get('imagen2')) == True :
                print("img2")
                imagenes_tema2 = Imagenes_Tema.objects.filter(id_tema=pk)[1]
                imagenes_tema2.image=request.FILES['imagen2']
                imagenes_tema2.save()
            tema.save()     
            messages.add_message(request, messages.SUCCESS, 'Modificacion exitosa.')
            return render(request, 'views/modificaciones/modificar_tema.html',{'temas':All_temas,'categorias':categorias,"estado":Tema.Estado,'tema':tema})
    except Exception as e:
        print("Error ->", e)
        messages.add_message(request, messages.ERROR, 'No se pudo realizar la modificacion.')

  
    return render(request, 'views/modificaciones/modificar_tema.html',{'temas':All_temas,'categorias':categorias,"estado":Tema.Estado,'tema':tema})

@login_required(login_url='/')
def view_eliminar_tema(request):
    All_temas = Tema.objects.all()
    categorias = Categoria_Tema.objects.all()
    return render(request, 'views/eliminacion/eliminar_tema.html',{'temas':All_temas,'categorias':categorias,"estado":Tema.Estado})
@login_required(login_url='/')
def eliminar_tema_p(request):
    try:
        tema = Tema.objects.get(id_tema=request.POST['tema'])
        imagenes = Imagenes_Tema.objects.filter(id_tema=tema.id_tema)
        for imagen in imagenes:
            imagenes.delete()
        videos = Videos_Tema.objects.filter(id_tema=tema)
        videos.delete()
        tema.delete()
        print(imagenes)
        messages.add_message(request, messages.SUCCESS, 'Tema eliminado exitosamente.')
    except Exception as e:
        print(e)
        messages.add_message(request,messages.ERROR,'Error al eliminar el tema.')

        categorias = Categoria_Tema.objects.all()
    return redirect('eliminar_tema')

@login_required(login_url='/')
def view_galeria(request):
    return render(request, 'views/galeria/view_galeria.html')



@csrf_exempt
def recuperar_contrasenia(request):
    if request.method == 'POST':
        #response = json.loads(request.body)
        try:
            usuario = UserProfile.objects.get(email=request.POST['correo'])
            print("validando correo")
        except UserProfile.DoesNotExist:
            usuario = None
            messages.add_message(request,messages.ERROR,'El correo ingresado no existe.!!')
            return redirect('password')

        new_password = UserProfile.objects.make_random_password()
        usuario.set_password(new_password)
        usuario.save()

        asunto = 'Cambio de contraseña Familias Unidas Ec'
        mail = request.POST['correo']
        mensaje = 'Usted ha solicitado recuperación de contraseña su contraseña nueva es la siguiente: '+ new_password +" asegurese de cambiarla luego."
        nombres = usuario.username

        if nombres != '' and len(mail.split('@')) == 2 and mensaje != '':
            textomensaje = '<br>'
            lista = mensaje.split('\n')
            c = 0
            for i in lista:
                textomensaje += i+'</br>'
                c+=1
                if len(lista)  > c :
                    textomensaje += '<br>'
            msj = '<p><strong>IPSP :</strong>'+nombres+'</p><p><strong>Correo: </strong>'+mail+'</p><strong>Mensaje: </strong>'+textomensaje+'</p>'
            msj2 = msj+'<br/><br/><br/><p>Usted esta realizando el proceso de recuperacion de contraseña.</p><p><strong>NO RESPONDER A ESTE MENSAJE</strong>, nosotros nos pondremos en conacto con usted de ser necesario.</p><br/>'
            try:
                
                send_mail('Contactanos: '+asunto, msj,'familias.unidasEC@gmail.com', ['familias.unidasEC@gmail.com'], fail_silently=False, html_message = '<html><body>'+msj+'</body></html>')
                send_mail('Correo enviado: '+asunto, msj2, 'familias.unidasEC@gmail.com', [mail], fail_silently=False, html_message= '<html><body>'+msj2+'</body></html>')
            except BadHeaderError:
                return redirect('password')
            messages.add_message(request, messages.SUCCESS, 'Se ha enviado su contraseña temporal, revise su correo.')
            return redirect('password')
    return redirect('password')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #Con esto crean los tipos de usarios mientras tanto para que vayan probando los diferentes tipos de usuarios
        #new = UserProfile.objects.create_user('john', 'lennon@thebeatles.com', '23198')
        #new.tipo = "A"
        #new.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                #redirect('index')
                try:
                    usuario = UserProfile.objects.get(username=username)
                    print(usuario.username)
                    pass
                except expression as identifier:
                    pass
                if usuario.tipo == "E": #Editor
                    return redirect('registrar_tema')
                elif usuario.tipo == "A": #Administrador
                    return redirect('registrar_tema')
                elif usuario.tipo == "C": #Consejero
                    return redirect('index')
            else:
                # Return a 'disabled account' error message
                messages.add_message(request,messages.ERROR,'Creedenciales incorrectas, intentelo de nuevo...')
                return render(request, 'views/login.html', {})
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request,messages.ERROR,'Usuario o contraseña incorrectas, intentelo de nuevo...')
            return render(request, 'views/login.html', {})
    else:
        return render(request, 'views/login.html', {})


def logout_view(request):
    logout(request)
    return redirect('/')
    # Redirect to a success page.
    # try:
    #     del request.session['username']
    # except:
    #  pass
    # return render(request, 'app_foldername/login.html', {})
def forgot_password(request):
    return render(request, 'views/forgot-password.html', {})


@csrf_exempt
@login_required(login_url='/')
def recibir_imagenes(request):
    if request.method == "POST":
        galeria = Galeria.objects.get(id_galeria=1)
        for k,v in request.FILES.items():
            imagen = Imagenes_galeria(id_galeria=galeria,image=v)
            imagen.save()
            
        return JsonResponse(200,safe=False)
    return JsonResponse(400,safe=False)
    # return redirect('views/galeria/view_galeria.html')
@login_required(login_url='/')
def recibir_video(request):
    if request.method == "POST":
        galeria = Galeria.objects.get(id_galeria=1)
        for k,v in request.FILES.items():
            video = Videos_galeria(id_galeria=galeria,video=v)
            video.save()
        return render(request, 'views/galeria/view_galeria.html')
    return render(request, 'views/galeria/view_galeria.html')


@login_required(login_url='/')
def notificaciones(informacion):
    usuarios = UserProfile.objects.all();
    asunto = 'Actualizacion de contenido Familias Unidas Ec'
    mensaje = "Se ha actualizado el contenido "+informacion +", puede revisarlo en el administrador"
    correos=[]
    for user in usuarios:
        if user.tipo != "U":
            correos.append(user.email)
    print(correos)
    message1 = (asunto, mensaje, 'familias.unidasEC@gmail.com',correos)
    try:
        send_mass_mail((message1,), fail_silently=False)
        print("mensaje exitoso")
    except BadHeaderError:
        print("error")
    