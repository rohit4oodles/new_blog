from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth.hashers import make_password
from main import settings

class User(AbstractUser):

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(primary_key=True)
    user_bio=models.CharField(max_length=50)
    # password=models.CharField(max_length=1000)
    user_profile_image=models.ImageField(upload_to="profilfe/", null=True, blank=True)
    USERNAME_FIELD='email'
    is_active=models.BooleanField(default=False)
    username=models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateField(auto_now_add=True)
    REQUIRED_FIELDS = ['first_name', 'last_name'] 
    objects = UserManager()
    def __str__(self):
        return self.email
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
            


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE ,related_name="profile")
    
    verification_token=models.CharField(max_length=6,blank=True,null=True)
    verification_token_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user

class BlogPost(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    def get_author_image(self):
        if self.author.user_profile_image and hasattr(self.author.user_profile_image, 'url'):
            return self.author.user_profile_image.url
        else:
            return  settings.STATIC_URL+'images/avatar.png'
    

class Comments(models.Model):
    id=models.AutoField(primary_key=True)
    blog=models.ForeignKey(BlogPost,related_name="commments",on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateField(auto_now_add=True)
    def get_author_image(self):
        if self.author.user_profile_image and hasattr(self.author.user_profile_image, 'url'):
            return self.author.user_profile_image.url
        else:
            return  settings.STATIC_URL+'images/avatar.png'
    def __str__(self):
        return f"coment by{self.author} on {self.blog}"
# Create your models here.

