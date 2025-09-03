from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habit
from .forms import HabitForm

def habit_list(request):
    habit = Habit.objects.filter(user=request.user).order_bu('title')
    return render(request, 'main/habit_list.html', {'habit': habit})

def habit_creat(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user # ← владелец — текущий пользователь
            habit.save()
            messages.success('Привычка успешно создана')
            return redirect('habit_list')
        else:
            messages.success('Ошибка при создании привычки')
    else:
        form = HabitForm()
    return render(request, 'main/habit_creat.html', {'form': form})

def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user) # ← защита: чужие не редактируем
    if request.method == 'POST':
        form = HabitForm(request.POST ,instance=Habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Привычка обновлена')
            return redirect('habit_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'main/habit_update.html', {'form': form})

def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Привычка удалена')
        return redirect('habit_list')
    return render(request, 'main/habit_delete.html', {'habit': habit})