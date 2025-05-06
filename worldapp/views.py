from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from worldapp.serializer import *

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

@api_view(['GET'])
def userView(request):
    User = get_user_model()
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDetails(request):
    User = get_user_model()
    matching_key = request.query_params.get('user_type')
    if matching_key == 'client':
        users = User.objects.filter(is_client=True)
    elif matching_key == 'freelancer':
        users = User.objects.filter(is_freelancer=True)
    else:
        users = User.objects.filter(is_freelancer=False, is_client=False)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authUser(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def authUserUpdate(request):
    data = request.data
    us_nm = data.get('username', request.user.username)
    em = data.get('email', request.user.email)
    is_cl = data.get('is_client', request.user.is_client)
    is_fl = data.get('is_freelancer', request.user.is_freelancer)
    User = get_user_model()
    User.objects.filter(pk=request.user.id).update(username=us_nm, email=em, is_client=is_cl, is_freelancer=is_fl)
    return Response({"message": "user updated succesfully!"})

@api_view(['POST'])
def userProfileComplete(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "user updated succesfully!"})
    return Response("could add data!!", status=status.HTTP_400_BAD_REQUEST)
