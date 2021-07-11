from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.views import APIView 
from rest_framework.settings import api_settings
from rest_framework.response import Response
from user.serializers import UserSerializer, AuthTokenSerializer, QuizSerializer, \
                            QuestionSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from core.models import Quiz, Question
from datetime import timedelta
from django.utils import timezone 
import pytz 
import datetime




def get_current_time():
    today_date = datetime.datetime.now()
    # today_time = datetime.datetime.now().time()
    # print('date=', today_date, today_time)
    # res = today_date  + timedelta(days=1) - timedelta(seconds=1) 
    # print('This is res==',res)
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
    


class LiveQuizView(QuizView):

    #print('Live quiz=', today_date)
    queryset = Quiz.objects.filter(start_at__lte=today_date,
            end_at__gte=today_date,
            is_published=True)

class LiveQuizQuestion(APIView):

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
    

# class QuizViewSet(viewsets.ModelViewSet):
#     serializer_class = QuizSerializer
#     permission_classes =(permissions.IsAuthenticated,)

#     def get_queryset(self):
#         queryset = Quiz.objects.all()
#         return queryset
    

today_date = get_current_time()
# class PastQuizView(QuizViewSet):
#     queryset = Quiz.objects.filter(end_at__lt=today_date,
#                      is_published=True)


# class LiveQuizViewSet(viewsets.ModelViewSet):
#     serializer_class = QuizSerializer
#     permission_classes =(permissions.IsAuthenticated,)

#     #print('Live quiz=', today_date)

#     def get_queryset(self):

#         queryset = Quiz.objects.filter(start_at__lte=today_date,
#             end_at__gte=today_date,
#             is_published=True)
#         return queryset
   


# class AttemptLiveQuiz(APIView):
#     serializer_class = QuizSerializer
#     permission_classes =(permissions.IsAuthenticated,)
#     lookup_url_kwarg = 'pk'

#     def get(self, request, *args, **kwargs):
#         queryset = Question.objects.filter(quiz=pk)
#         serializer = QuizSerializer(queryset, many=True)
#         return Response(serializer.data)
    

# class UpcomingQuizView(QuizViewSet):
#     queryset = Quiz.objects.filter(start_at__gt=today_date,
#                     is_published=True)


