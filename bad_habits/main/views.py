from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Habit
from .forms import HabitForm, RegisterForm

@login_required
def habit_list(request):
    habit = Habit.objects.filter(user=request.user).order_by('title')
    return render(request, 'main/habit_list.html', {'habit': habit})

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user # ← владелец — текущий пользователь
            habit.save()
            messages.success(request, 'Привычка успешно создана')
            return redirect('habit_list')
        else:
            messages.error(request, 'Ошибка при создании привычки')
    else:
        form = HabitForm()
    return render(request, 'main/habit_creat.html', {'form': form})

@login_required
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user) # ← защита: чужие не редактируем
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Привычка обновлена')
            return redirect('habit_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'main/habit_update.html', {'form': form})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Привычка удалена')
        return redirect('habit_list')
    return render(request, 'main/habit_delete.html', {'habit': habit})

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('habit_list')

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # сразу логиним после регистрации
            messages.success(request,'Аккаунт успешно создан! 🎉')
            return redirect('habit_list')
        else:
            messages.error(request, 'Ошибка при регистрации. Исправьте форму!')
    else:
        form = RegisterForm()
    return render(request, 'main/user_register.html', {'form': form})
