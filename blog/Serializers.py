from rest_framework import serializers
from .models import User,Profile,BlogPost,Comments
from django.contrib.auth.hashers import make_password
from main import settings
from django.contrib.auth.password_validation import validate_password
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    user_profile_image = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','user_bio','password','user_profile_image','is_active','created_at']
    def create(self, validated_data):
        password = validated_data.pop('password') 
        user = User(**validated_data)  
        user.set_password(password)  
        user.save()  
        return user
    
class User_profile(serializers.ModelSerializer):
    user_profile_image=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['first_name','last_name','email','user_bio','user_profile_image','created_at']
    def get_user_profile_image(self,obj):
        if obj.user_profile_image and hasattr(obj.user_profile_image, 'url'):
            print(">>>>>>>>>>>>>>")
            return settings.LOCAL_HOST+str(obj.user_profile_image.url)
        else:
            print("88888888888888")
            return settings.LOCAL_HOST+settings.STATIC_URL+'images/avatar.png'
         
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['user','verification_token']

class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    class Meta:
        fields = ['refresh', 'access']

class BlogSerializer(serializers.ModelSerializer):
    author_image=serializers.SerializerMethodField()
   
    class Meta:
        model=BlogPost
        fields=['id','title','description','author','author_image','image','created_at']
    def get_author_image(self,obj):
        return settings.LOCAL_HOST+str(obj.get_author_image())
   
class contnet(BlogSerializer):
    image=serializers.SerializerMethodField()
    class Meta(BlogSerializer.Meta):
        fields=['id','title','description','author','author_image','image','created_at']
    def get_image(self,obj):
        return settings.LOCAL_HOST + str(obj.image.url)
class commentserializer(serializers.ModelSerializer):
    author_image=serializers.SerializerMethodField()
    class Meta:
        model=Comments
        fields=['id','blog','author','content','created_at','author_image']
        read_only_fields=['blog','author']
    def get_author_image(self,obj):
        return settings.LOCAL_HOST + str(obj.get_author_image())