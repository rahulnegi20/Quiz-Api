import uuid
import os 

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _ 


def question_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/question/', filename)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user
        """
        if not email:
            raise ValueError("Users must have an email address!")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and saves a new superuser
        """
        user =self.create_user(email, password)
        user.is_staff =True 
        user.is_superuser =True 
        user.save(using=self._db)

        return user   

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports email instead 
    of username
    """
    email       = models.EmailField(max_length=255, unique=True)
    name        = models.CharField(max_length=255)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email' 


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    question_count = models.IntegerField(default=1)
    is_published = models.BooleanField(default=False)
    start_at = models.DateTimeField(auto_now_add=False, auto_now=False, unique=True)
    end_at = models.DateTimeField(auto_now_add=False, auto_now=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['created_at',]
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')
    
    def __str__(self):
        return '{}'.format(str(self.title))


    def quiz_state(self):
        """Defining the Quiz state"""
        if self.is_published == False:
            pass


class Question(models.Model):
    quiz = models.ForeignKey(Quiz,
                          related_name='question',  
                          on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    image = models.ImageField(upload_to=question_image_file_path, blank=True)

    class Meta:
        ordering =['id',]
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
    
    def __str__(self):
        return '{}'.format(str(self.question))


class Answer(models.Model):
    question = models.ForeignKey(Question,
                                 related_name='answer', 
                                 on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering =['id',]
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
    
    def __str__(self):
        return '{}'.format(str(self.answer))
    
