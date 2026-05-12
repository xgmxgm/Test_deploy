from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Student
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def hello(request):
    return HttpResponse("Добро пожаловать на сайт колледжа!")

@login_required
def student_list(request):
    students = Student.objects.all()  # получаем всех студентов из БД
    return render(request, 'students/index.html', {'students': students})

@login_required
def profile(request):
    return render(request, "students/profile.html")

def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        group = request.POST.get("group")
        photo = request.FILES.get("photo")

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            group=group,
            photo=photo
        )
        return redirect("student_list")

    return render(request, "students/add_student.html")

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "students/detail.html", {"student": student})

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.age = request.POST.get("age")
        student.group = request.POST.get("group")
        student.save()
        return redirect("student_list")

    return render(request, "students/edit_student.html", {"student": student})

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect("student_list")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "students/register.html", {"form": form})