from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.views import APIView 
from rest_framework.settings import api_settings
from rest_framework.response import Response
from user.serializers import UserSerializer, AuthTokenSerializer, QuizSerializer, \
                            QuestionSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from core.models import Quiz, Question, QuizTakers
from datetime import timedelta
from django.utils import timezone 
import datetime


def get_current_time():
    today_date = datetime.datetime.now()
    return today_date


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class QuizView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes =(permissions.IsAuthenticated,)


today_date = get_current_time()
class PastQuizView(QuizView):
    queryset = Quiz.objects.filter(end_at__lt=today_date,
                     is_published=True)


class PastQuizQuestion(APIView):

    def get(self, request, format=None, **kwargs):
        queryset = Question.objects.filter(quiz__pk=kwargs['pk'])
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)
    

class UpcomingQuizView(QuizView):
    queryset = Quiz.objects.filter(start_at__gt=today_date,
                    is_published=True)


class UpcomingQuizQuestion(APIView):

    def get(self, request, format=None, **kwargs):
        queryset = Question.objects.filter(quiz__pk=kwargs['pk'])
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)
    

class LiveQuizView(APIView):

    def get(self, request, fromat=None ,  *args, **kwargs):
        user = request.user
        quiz_taker = QuizTakers.objects.filter(user=user).values('quiz')
        print('quiz_', quiz_taker)
        taken = []
        for key, value in enumerate(quiz_taker):
           # print(key, value['quiz'])
            taken.append(value['quiz'])
        print('taken', taken)

       # print('OOOOOOOOOOOK', taken['quiz'], type(taken))
        queryset = Quiz.objects.filter(start_at__lte=today_date,
                end_at__gte=today_date,
                is_published=True).exclude(pk__in=taken)
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data)

class LiveQuizQuestion(APIView):

    def get(self, request, format=None, **kwargs):
        quiz = Question.objects.filter(quiz__pk=kwargs['pk'])
        serializer = QuestionSerializer(quiz, many=True)
        return Response(serializer.data)
    


