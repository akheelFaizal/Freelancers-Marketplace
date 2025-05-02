import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

# Create your views here.

@api_view(['POST'])
def createUser(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_client = request.data.get('is_client', False)
        is_freelancer = request.data.get('is_freelancer', False)

        User = get_user_model()
        user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_client=is_client,
                is_freelancer=is_freelancer
            )
        return Response(
            {"message": f"Custom User {user.username} created successfully!"},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
