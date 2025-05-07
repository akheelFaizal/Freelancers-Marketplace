from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
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
        fields = ('skill',)
