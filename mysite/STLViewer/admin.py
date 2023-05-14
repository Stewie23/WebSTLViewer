from django.contrib import admin

# Register your models here.
from .models import Items,Taggins,Collection

admin.site.register(Items)

admin.site.register(Collection)
