from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _ 
from rest_framework import serializers
from core.models import Quiz, Question, Answer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only':True, 'min_length':5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)    


    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication  object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'}, 
        trim_whitespace = False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user 
        return attrs  
    

class QuizSerializer(serializers.ModelSerializer):
    """Serializing the Quiz Model"""
    question = serializers.StringRelatedField(many=True) 
    class Meta:
        model = Quiz
        fields = ('id', 'title','question', )
        read_only_fields = ('id',)
        depth = 1
        

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'answer', 'is_correct',)


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    quiz = serializers.StringRelatedField() 
    class Meta:
        model = Question
        fields = ('quiz','id', 'question', 'answer',)
        depth =1

