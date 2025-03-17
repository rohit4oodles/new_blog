from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist   
from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework.decorators import api_view,permission_classes
from .models import User,Profile,BlogPost,Comments
from .Serializers import UserSerializer,TokenSerializer,ProfileSerializer,BlogSerializer,User_profile,contnet,commentserializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
import random
import string
from main import settings
from rest_framework import generics
def genrate_token():
    return "".join(random.choices(string.ascii_letters+string.digits,k=6))

def send_verification_email(request,user):
    token=genrate_token()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    
    try:
        with transaction.atomic():
            profile, created = Profile.objects.get_or_create(user=user) 
            profile_data = {'user': user.email, 'verification_token': token}
            serializer = ProfileSerializer( profile, data=profile_data)
            print(">>>>>>>>>>>>>>>>>>>>>>....")

            if serializer.is_valid():
                serializer.save()
                print(">>>>>>...")
                subject = 'Your email verification code'
                message = f'Your email verification code is: {token}'
                print(user.email)

                res=send_mail(subject, message,None, [user.email])
                if res>0:
                    return 200
                else:
                    serializer.instance.delete()
        
            else:
                
                print("Error saving the token:", serializer.errors)
    except Exception as e:
        print(e)


@api_view(['POST'])
def create_user(request):
    user=User.objects.filter(is_active=False)
    user.delete()
    if User.objects.filter(email=request.data['email']).exists():
        
        return Response({"message":"user already exits"},status=400)
    else:
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
        
            user = user_serializer.save()
            print("User created successfully:", user)

            
            res = send_verification_email(request, user)
            
            if res == 200:
                
                print("Verification email sent successfully.")
                return Response({"message": "User created and verification email sent."}, status=200)
            else:
                user.delete()
                print("Failed to send verification email.")
                return Response({"message": "Failed to send verification email."}, status=400)
        else:
            print("Serializer validation failed. Errors:", user_serializer.errors)
            return Response({"message":user_serializer.errors}, status=400)

@api_view(['POST'])
def verify_token(request):
    if request.method=="POST":
        data=request.data
        token=data['token']
        user=data['email']
        print(user)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
        try:
            print("in")
            user=User.objects.get(email=user)
            print(user)
            print(user.profile.verification_token,token)

            if user.profile.verification_token==token:
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
                user.is_active=True
                user.save()
                refresh = RefreshToken.for_user(user)
                user=User.objects.filter(is_active=False)
                user.delete()
                print(">>>>>>>>>>>>>>...")
                return Response(TokenSerializer({'refresh': str(refresh), 'access': str(refresh.access_token)}).data,status=200)

            else:
                user=User.objects.filter(is_active=False)
                user.delete()
                return HttpResponse('Invalid token, please try again.')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=User.objects.filter(is_active=False)
            user.delete()
            return HttpResponse('Invalid link, please try again.')


@api_view(['POST'])
def Login(request):
    
    if request.user.is_authenticated:
        
        return Response(status=200)
    else:
        print(">>>>>>>>>>>>.")
        detail=request.data
        if 'email'  not in detail and 'password' not in detail:
            return Response({"message":"error email and password is required"})

        try:
            print(">>>>>>>>>>###")
            user=User.objects.get(email=detail['email'])
            if user.is_active==False:
                return Response({"message":"please verify your email"},status=401)
            print("333333333333333")
            if user.check_password(detail['password']):
                print(">>>>>>>>>>")
                
                refresh = RefreshToken.for_user(user)
                print(">>>>>>>>>>????")
                
                return Response(TokenSerializer({'refresh': str(refresh), 'access': str(refresh.access_token)}).data,status=200)
            else:
                return Response({'message':"invalid credinatials"},status=400)  
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=404)
            

@api_view(['POST'])
def forgot(request):
    if request.method=="POST":
        data=request.data
        if 'email' not in data:
            return Response({"plese enter the email"})
        else:
            try:
                user=User.objects.get(email=data['email'])
                print(">>>>>>>>>>>>>")
                if user.is_active==True:
                    send_verification_email(request,user)
                    return Response(status=200)
                else:
                    return Response({'user is not registerd'})
            except:
                pass

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    if request.user.is_authenticated:
        if request.method=="PUT":
            data=request.data
            user=request.user
            user.set_password(data['password'])
            user.save()
            return Response({"password reset "},status=200)
    else:
        return Response({"not AUthenticated"})


@api_view(["POST","PUT"])
# @permission_classes([IsAuthenticated])
def addpost(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            print(">>>>>>>>>>>>>>>>>>>>>>")

            serializer=BlogSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                print(">>>>>>>..")
                instance=serializer.save()
                return Response({"message":"blog uploaded"},status=200)
            else:
                
                return Response({"message":"not vaild data"},status=401)

            
        else:
            
            return Response({"message":"please log in again"},status=400)
    elif request.method=="PUT":
        if request.user.is_authenticated:
                user=request.user
                id=request.data.get('id')
                blog=BlogPost.objects.get(id=id)
                if blog.author==user:
                    title=request.data.get('title',blog.title)
                    description=request.data.get('description',blog.description)
                    blog.title=title
                    blog.description=description
                    blog.save()
                    return Response({"message":"updated successfully"},status=201)
                else:
                    print("nooooo")
                    Response({"message":"you can edit only your post"},status=400)
        else:
            return Response(status=400)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

@api_view(['GET'])
def post(request):
    if request.method=="GET":
        posts=BlogPost.objects.order_by("?")[:6]
        serial=contnet(posts,many=True)
        
        return Response(serial.data,status=200)
    else:
        return Response(status=400)

@api_view(["GET"])
def blog_list(request):
    blog=BlogPost.objects.all()
    
    
    page_no=request.GET.get('PAGE',1)
    page_size=request.GET.get('limit',6)
    
    paginator=Paginator(blog,page_size)
    
    page=paginator.get_page(page_no)
    serial=contnet(page.object_list,many=True)
    print(page_no)
    return JsonResponse({
        'blogs':serial.data,
        'current_page':page_no,
        "total_page":paginator.num_pages,
        "total_blogs":paginator.count
    })

@api_view(['GET'])
def profile_pic(request):
    if request.user.is_authenticated:
        try:
            print(">>>>>>>>>>")
            user_email=request.user.email
            user=User.objects.get(email=user_email)
            print(user)
        
            
            
           
            if user.user_profile_image:
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..")
                image_url=user.user_profile_image.url
                return JsonResponse({
                    "image_url":settings.LOCAL_HOST+ str(image_url)
                },status=200)
            else:
                print("*********************")
                return JsonResponse({
                    "image_url":settings.LOCAL_HOST+settings.STATIC_URL+'images/avatar.png'
                },status=200)
        except:
            return Response(status=400)

    else:
        return Response({"message":"user is not authenticated"},status=400)    


@api_view(['GET','PUT'])
def profile(request):
    if request.user.is_authenticated and request.method=="GET":
        user=request.user.email
        data=User.objects.get(email=user)
        data=User_profile(data)
        return Response(data.data,status=200)
    elif request.method=="PUT" and request.user.is_authenticated:
        user=request.user

        
        user_bio=request.data.get('user_bio',user.user_bio)
        first_name=request.data.get('first_name',user.first_name)
        last_name=request.data.get('last_name',user.last_name)
        user.user_bio=user_bio
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        return Response(status=201)

    else:
        return Response(status=400)
    
@api_view(['GET'])
def user_post(request):
    if request.user.is_authenticated:
        user_email=request.user.email
        user = User.objects.get(email=user_email)
        blogs=BlogPost.objects.filter(author=user)
        
        if blogs.exists():
                print("................")
                user_data = []
                for blog in blogs:
                    user_data.append({
                        "id":blog.id,
                        "title": blog.title,
                        "description": blog.description,
                        "image_url": settings.LOCAL_HOST+str(blog.image.url),
                        "created_at": blog.created_at,
                        "author":user_email
                        
                    })
        return Response(user_data,status=200)
    else:
        return Response({"message":"not authenticated"},status=400)
    
@api_view(['GET'])
def search(request):

    query=request.GET.get('query')
    blogs=BlogPost.objects.all()
    if(query):
        blog=blogs.filter(description__icontains=query)
            
        
        if len(blog)>0:
        
            page_no=request.GET.get('PAGE',1)
            page_size=request.GET.get('limit',6)
            
            paginator=Paginator(blog,page_size)
            
            page=paginator.get_page(page_no)
            serial=contnet(page.object_list,many=True)
            print(page_no)
            return JsonResponse({
                'blogs':serial.data,
                'current_page':page_no,
                "total_page":paginator.num_pages,
                "total_blogs":paginator.count
            },status=200)
        else:
            return Response({"message":"not found"},status=400)
    else:
        return Response({"message":"not found"},status=400)
    
class commentListView(generics.ListCreateAPIView):
    serializer_class=commentserializer
    # permission_classes = [IsAuthenticated] 
    def get_queryset(self):
        post_id=self.kwargs['post_id']
        return Comments.objects.filter(blog=post_id)
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            post_id=self.kwargs['post_id']
            print(">>>>>>>>>>>>>>>....")
            blog=BlogPost.objects.get(id=post_id)
            print(blog)
            serializer.save(author=self.request.user,blog=blog)
    def get_permissions(self):
    
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request,cmt_id):
    print(">>>>>>>>>>>>>>>>>>>>")
    if request.user.is_authenticated:
        print(">>>>>>>>>>>>>>>>>>..")
        try:
            print("$$$$$$$$$$$$$$$")
            id=cmt_id
            print("###############")
            comment=Comments.objects.get(id=id)
            if comment:
                if comment.author==request.user:
                    comment.delete()
                    return Response({"message":"comment deleted successfuly"},status=200)
                else:
                    return Response({"message":"you can delete only your msg"},status=400)
            else:
                return Response({"message":"comment not found"})
        except:
            return Response({"message":"comment does not exist"},status=400)
    else:
        return Response({"message":"not authenticated"},status=400)