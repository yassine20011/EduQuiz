from django.contrib import admin

# Register your models here.
from .models import Profile, DataRelatedToUser


admin.site.register(Profile)
admin.site.register(DataRelatedToUser)
