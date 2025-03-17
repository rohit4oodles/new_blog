from django.contrib import admin
from .models import User,Profile,BlogPost,Comments
admin.site.register(User)

admin.site.register(Profile)

admin.site.register(BlogPost)
admin.site.register(Comments)



# Register your models here.
