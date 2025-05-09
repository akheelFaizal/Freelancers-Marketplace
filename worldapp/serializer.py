from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError 


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'is_client',
            'is_freelancer'
        )

class UserProfileSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all(),
        required=False
    )
    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'bio',
            'skills',
            'rating'
        )
    def update_or_create(self, user, validated_data):
        skills = validated_data.pop('skills', None)

        profile, created = Profile.objects.update_or_create(user=user, defaults=validated_data)
        print(created)

        if skills:
            profile.skills.set(skills) 
        return profile

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'skill',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
    def validate(self, data):
        client = data.get('client')
        if not client.is_client:
            raise ValidationError("Provided client is not a valid client.")
        else:
            return data
        
class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
    def validate(self, data):
        freelancer = data.get('freelancer')
        if not freelancer.is_freelancer:
            raise ValidationError("Provided client is not a valid client.")
        else:
            return data
