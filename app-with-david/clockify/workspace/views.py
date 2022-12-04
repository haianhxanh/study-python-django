from django.shortcuts import render, redirect
# from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from datetime import date, time, datetime
from time import strftime, gmtime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import User,TimeRecord 
from .forms import RegistrationForm
from  workspace.serializers import ListUserSerializer, TimeRecordStartSerializer

# Create your views here.
# def say_hello(request):
#     return render(request, 'hello.html')

def home(request): 
  return render(request, 'workspace/home.html')

class RegistrationView(CreateView):
    template_name = 'workspace/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url


class ProfileView(UpdateView):
    model = User
    fields = ['name', 'phone', 'date_of_birth', 'picture']
    template_name = 'workspace/profile.html'

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        return self.request.user


def register(request): 
  if request.method == 'POST': 
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Hi {username}, your account was successfully created')
      return redirect('home')
  else:
    form = UserCreationForm()

  return render(request, 'workspace/register.html', {'form':form})


class TrackingStart(APIView):
  permission_classes = [IsAuthenticated]

  # {"id": 12}, [12, "test"]
  def post(self, request):
    serializer = TimeRecordStartSerializer(data=request.POST)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    start_time = strftime("%H:%M", gmtime())
    # start_time = datetime.now().time
    date_now = date.today()
    serializer.save(start_time=start_time, date=date_now, user=request.user)
    # TimeRecord.objects.create(**serializer.validated_data, start_time=start_time, date=date_now, user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# todo kill all running and start new
# todo stop currently running one

class ListAllUsers(ListAPIView):

  serializer_class = ListUserSerializer

  def get_queryset(self):
     return User.objects.all()
