from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime    

# Create your models here.

#class customUser(AbstractUser):
#   rol = models.CharField(max_length=2,default='e')#A: administrador, E:editor, C:consejero


class UserProfile(AbstractUser):
    tipo = models.CharField(max_length=2,null=False,blank=False,default='E',verbose_name='Tipos de usuario')# A:administrador, E: editor, C: consejero

    def say_hello(self):
        return "Hello, my name is {}".format(self.first_name)
    
    def __str__(self):           
        return self.username  

class Categoria_Tema(models.Model):
    id_categoria_tema=models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=200,null=False,blank=True,verbose_name="Nombre de la categoria")
    
    def __str__(self):              
        return self.nombre_categoria

class Tema(models.Model):
    #Enum
    class Estado(models.IntegerChoices):
        REVISADO = 1
        PENDIENTE = 2
    
    id_tema = models.AutoField(primary_key=True)
    tema_categoria = models.ForeignKey(Categoria_Tema,on_delete=models.CASCADE,null=True,blank=True)
    estado = models.IntegerField(choices=Estado.choices)
    titulo = models.CharField(max_length=100,null=False,blank=False,verbose_name="Titulo del tema")
    descripcion = models.TextField(max_length="900",null=False,blank=True,verbose_name="Descripcion del tema")
    fecha= models.DateField(null=False, blank=True, default=datetime.now)
    estado= models.SmallIntegerField(default=1)
    def __str__(self):              
        return self.titulo



class Imagenes_Tema(models.Model):
    image = models.ImageField(upload_to='image/',null=False,blank=True,verbose_name="Imagen del tema")
    id_tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

class Videos_Tema(models.Model):
    video = models.FileField(upload_to="video/",null=False,blank=True,verbose_name="Video del tema")
    id_tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    url = models.CharField(max_length=200,null=False,blank=True)

    
class Audio_Tema(models.Model):
    audio = models.FileField(upload_to="audio/",null=False,blank=True,verbose_name="Audio del tema")
    id_tema = models.ForeignKey(Tema, on_delete=models.CASCADE)


class Galeria(models.Model):
    id_galeria = models.AutoField(primary_key=True)
    descripcion= models.CharField(max_length=100,null=True,blank=True)

class Imagenes_galeria(models.Model):
    image = models.ImageField(upload_to='image/',null=False,blank=True,verbose_name="Imagen del tema")
    id_galeria = models.ForeignKey(Galeria, on_delete=models.CASCADE)

class Videos_galeria(models.Model):
    video = models.FileField(upload_to="video/",null=False,blank=True,verbose_name="Video del tema")
    
    id_galeria = models.ForeignKey(Galeria, on_delete=models.CASCADE)

class Testimonios(models.Model):
    usuario = models.CharField(max_length=150,null=False,blank=False)
    fecha= models.DateField(null=False, blank=True, default=datetime.now)
    titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(max_length=100,null=False,blank=True)
    image = models.ImageField(upload_to='image/',null=False,blank=True)
    estado= models.SmallIntegerField(default=1)

class Tips(models.Model):
    usuario = models.CharField(max_length=150,null=False,blank=False)
    fecha= models.DateField(null=False, blank=True, default=datetime.now)
    titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(max_length=300,null=False,blank=True)
    image = models.ImageField(upload_to='image/',null=False,blank=True)
    estado= models.SmallIntegerField(default=1)

class Contactanos(models.Model):
    usuario = models.CharField(max_length=150,null=False,blank=False)
    fecha= models.DateField(null=False, blank=True, default=datetime.now)
    titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(max_length=300,null=False,blank=True)
    correo = models.CharField(max_length=150,null=False,blank=False)
    estado= models.SmallIntegerField(default=1)

class Consejeria(models.Model):
    usuario = models.CharField(max_length=150,null=False,blank=False)
    empieza= models.DateTimeField(null=False, blank=True)
    termina= models.DateTimeField(null=False, blank=True)
    tema = models.CharField(max_length=100,null=False,blank=False)
    correo = models.CharField(max_length=150,null=False,blank=False)
    estado= models.SmallIntegerField(default=1)


