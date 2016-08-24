from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
# from models import User, Message, Comment
import bcrypt

def index(request):
    return render(request, 'user_poke/index.html')

def user_page(request):
    return render(request, 'user_poke/user.html')
