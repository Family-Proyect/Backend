from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Tema)
admin.site.register(Imagenes_Tema)
admin.site.register(Videos_Tema)
admin.site.register(Audio_Tema)
admin.site.register(Categoria_Tema)
admin.site.register(Galeria)
admin.site.register(Imagenes_galeria)
admin.site.register(Videos_galeria)
admin.site.register(Tips)
