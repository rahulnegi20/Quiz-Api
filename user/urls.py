from django.urls import path

from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

#router.register(r'quiz', views.LiveQuizViewSet, basename='quiz')
#router.register(r'quiz/<int:pk>', views.AttemptLiveQuiz, basename='live')

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('all_quiz/', views.QuizView.as_view(), name='all-quiz'),

    path('past/', views.PastQuizView.as_view(), name='past-quiz'),
    path('past/<int:pk>/', views.PastQuizQuestion.as_view(), name='past-question'),
    path('live/', views.LiveQuizView.as_view(), name='live-quiz'),
    path('live/<int:pk>/', views.LiveQuizQuestion.as_view(), name='live-question'),
    path('upcoming/', views.UpcomingQuizView.as_view(), name='future-quiz'),
    path('upcoming/<int:pk>/', views.LiveQuizQuestion.as_view(), name='future-question'),
  
  
] #+ router.urls