from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('habit_list')
    else:
        return render(request, 'main/landing.html')

urlpatterns = [
    path('', home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('main/', include('main.urls'))
]
