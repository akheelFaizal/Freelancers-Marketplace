from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from worldapp.serializer import *
from rest_framework.exceptions import ValidationError


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
@permission_classes([IsAuthenticated])
def userProfileComplete(request):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    serializer = UserProfileSerializer(instance=profile, data=request.data, partial=True)

    if serializer.is_valid():
        # Use the `update_or_create` method of the serializer
        updated_profile = serializer.update_or_create(user=user, validated_data=serializer.validated_data)
        return Response(UserProfileSerializer(updated_profile).data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def addSkill(request):
    try: 
        serializer = SkillsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Skill Added!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def listFreelancers(request):
    try:
        user = get_user_model()
        skill = request.query_params.get('skill')
        print(skill)
        if skill :
            freelancers = Profile.objects.select_related('user').prefetch_related('skills').filter(skills__skill=skill, user__is_freelancer=True)
        else :
            freelancers = Profile.objects.select_related('user').prefetch_related('skills').filter(user__is_freelancer=True)

        serializer = UserProfileSerializer(freelancers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET','POST','PUT'])
def project(request):
    if request.method == 'POST':
        try:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Project added successffully!!"}, status=status.HTTP_201_CREATED)
            else :
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e :
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    elif request.method == 'GET':
         projects = Project.objects.all()
         serializer = ProjectSerializer(projects, many=True)
         return Response(serializer.data)
    else :
        project_id = request.query_params.get('pid')
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({"error": f"Project with id {project_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = ProjectSerializer(instance=project, data=request.data, partial=True)
        if serializer.is_valid():
             serializer.save()
             return Response(f"project with id {project_id} is updated successfully!!", status=status.HTTP_200_OK)
        else :
             return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
          
@api_view(['GET'])
def listOpenProjects(request):
    try:
        openProjects = Project.objects.filter(is_open=True)
        serializer = ProjectSerializer(openProjects, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e :
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])
def listClosedProjects(request):
    try:
        openProjects = Project.objects.filter(is_open=False)
        serializer = ProjectSerializer(openProjects, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e :
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
@api_view(['GET'])
def placeBid(request):
    try:
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
             serializer.save
    except ValidationError as e :
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    





