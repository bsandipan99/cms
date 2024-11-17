from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from rest_framework import status

def authenticate_user( request ):
    """
    A utility function to authenticate the user using JWT from the session.
    Returns:
        user (User): The authenticated user if successful.
        redirect_url (str): URL to redirect to if authentication fails.
    """
    access_token = request.session.get('access_token')

    if not access_token:
        return None, 'login'

    from django.http import HttpRequest
    request_with_token = HttpRequest()
    request_with_token.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

    jwt_auth = JWTAuthentication()

    try:
        user, token = jwt_auth.authenticate(request_with_token)
        return user, None  # Return user and token if successful
    except AuthenticationFailed:
        return None, 'refresh'  # Invalid token, redirect to refresh


def dashboard( request ):
    user, redirect_url = authenticate_user(request)

    if user is not None:
        posts = Post.objects.filter( author=user )
        return render(request, 'contents/dashboard.html', {'posts':posts})
    else:
        return redirect(redirect_url)


def post_content( request ):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')

    return render(request, 'contents/post_content.html', {'access_token':access_token})


def post_detail( request, pk ):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')

    return render(request, 'contents/post_detail.html', {'access_token':access_token, 'pk': pk})


def post_edit( request, pk ):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')

    return render(request, 'contents/post_edit.html', {'access_token':access_token, 'pk': pk})


@api_view(['POST'])
def create_post(request):
    """
    Create a post with data received from user
    """
    user, redirect_url = authenticate_user(request)

    data = request.data
    data['author'] = user.id
    data['created_date'] = timezone.now()
    data['published_date'] = timezone.now()
    
    serializer = PostSerializer( data=data )
    if serializer.is_valid():
        serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def read_post(request, pk):
    """
    Retrieve a single post by its primary key (pk)
    """
    post = Post.objects.get(pk=pk)
    serializer = PostSerializer(post)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_post(request, pk):
    """
    Update a single post by its primary key (pk)
    """
    post = get_object_or_404(Post, pk=pk)
    request.data['published_date'] = timezone.now()
    serializer = PostSerializer(post, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_post(request, pk):
    """
    Delete a single post by its primary key (pk)
    """
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'message': 'Invalid primary key'}, status=status.HTTP_400_BAD_REQUEST)