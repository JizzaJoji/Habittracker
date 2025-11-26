from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, CheckIn
from .forms import HabitForm, CheckInForm
from django.db.models import Count
from django.db.models.functions import TruncWeek


from django.db.models import Q

def index(request):
    search_query = request.GET.get("search", "")
    category_filter = request.GET.get("category", "")
    sort_by = request.GET.get("sort", "name") 

    habits = Habit.objects.all()

    if search_query:
        habits = habits.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    if category_filter:
        habits = habits.filter(category=category_filter)

    if sort_by == "name":
        habits = habits.order_by("name")
    elif sort_by == "date":
        habits = habits.order_by("-start_date")
    elif sort_by == "category":
        habits = habits.order_by("category")

    return render(request, "index.html", {
        "habits": habits,
        "search": search_query,
        "category": category_filter,
        "sort_by": sort_by,
    })

def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    checkins = habit.checkin_set.order_by('-date')

    if request.method == "POST":
        form = CheckInForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.habit = habit
            checkin.save()
    
            return redirect('detail', pk=pk)

    else:
        form = CheckInForm()

    return render(request, "habit_details.html", {
        "habit": habit,
        "checkins": checkins,
        "form": form,
    })

def add_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = HabitForm()
    return render(request, "habit_form.html", {"form": form})


def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect("habit_detail", pk=pk)
    else:
        form = HabitForm(instance=habit)
    return render(request, "habit_form.html", {"form": form})

def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == "POST":
        habit.delete()
        return redirect("index")
    return render(request, "habit_delete.html", {"habit": habit})

from django.shortcuts import render, get_object_or_404
from .models import Habit

def analytics(request, pk):
    habit = get_object_or_404(Habit, pk=pk)

    context = {
        "habit": habit,
        "success_rate": habit.success_rate(),
        "streak": habit.streak(),
        "best_day": habit.best_day(),
        "weekly_data": habit.weekly_summary(),
    }

    return render(request, "analytics.html", context)

def analytics_overall(request):
    habits = Habit.objects.all()
    checkins = CheckIn.objects.all()

    total_habits = habits.count()
    total_checkins = checkins.count()

    best_habit = habits.annotate(check_count=Count("checkin")).order_by("-check_count").first()

    weekly_summary = (
        CheckIn.objects.annotate(week=TruncWeek("date"))
        .values("week")
        .annotate(count=Count("id"))
        .order_by("week")
    )

    category_counts = habits.values("category").annotate(count=Count("id"))

    context = {
        "total_habits": total_habits,
        "total_checkins": total_checkins,
        "best_habit": best_habit,
        "weekly_summary": weekly_summary,
        "category_counts": category_counts,
    }

    return render(request, "analytics_overall.html", context)
