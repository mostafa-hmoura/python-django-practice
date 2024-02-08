from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer


@api_view(['GET'])
def index(request):
    return Response({'Success': 'This is an Test of Get Method on DJANGO'})


@api_view(['GET'])
def get_all_posts(request):
    get_posts = Post.objects.all()
    serializer = PostSerializer(get_posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_post(request):
    data = request.data
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success": "The post was created !"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_post(request):
    post_id = request.data.get("post_id")

    if not post_id:
        return Response({"error": "post_id is required in request data."}, status=status.HTTP_400_BAD_REQUEST)

    post = get_object_or_404(Post, id=post_id)

    try:
        post.delete()
        return Response({"Success": "The post was deleted successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"An error occurred while deleting the post: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_post(request):
    post_id = request.data.get("post_id")

    if not post_id:
        return Response({"error": "post_id is required in request data."}, status=status.HTTP_400_BAD_REQUEST)

    post = get_object_or_404(Post, id=post_id)

    try:
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"An error occurred while deleting the post: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_post(request):
    post_id = request.data.get("post_id")
    new_title = request.data.get("title")
    new_content = request.data.get("content")

    if not post_id or not new_content or not new_title:
        return Response({"error": "post_id is required in request data."}, status=status.HTTP_400_BAD_REQUEST)

    post = get_object_or_404(Post, id=post_id)

    try:
        post.title = new_title
        post.content = new_content
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"An error occurred while deleting the post: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
