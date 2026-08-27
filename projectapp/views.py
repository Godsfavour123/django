from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from projectapp.models import Post, Student
from projectapp.forms import PostForm, StudentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request, "index.html")

def about(request):
    about_message = "This is a message for the about page from the backend"

    best_players = ["Ororo", "Bellingham", "Mbappe", "Neymar", "Dembele"]
    GOAT = "Messi"

    context = {"taofeek":about_message,
               "programmer_name":"Awele",
               "age":"22",
               "best_players":best_players,
               "GOAT":GOAT,

               }

    return render(request, "about.html", context)


def profile(request):
    me ={"name":"Caleb", "class": "Python", "age": 24}
    return JsonResponse(me)

def posts(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "post.html", context)

def post(request, pk):
    # the_post = Post.objects.get(pk=pk)
    the_post = get_object_or_404(post, pk=pk)
    context = {"post": the_post}
    return render(request, "post.html", context)

def display_form(request):
    return render(request, "user_form.html")


def submit_form(request):
    if request.method == "POST":

        name = request.POST.get("name")
        dept = request.POST.get("department")

        values = {"name": name, "department": dept}
        return JsonResponse(values)

    return redirect("user_form")


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()

    context = {"post_form": form}
    return render(request, "post_form.html", context)

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm(instance=post)
    
    context = {"post_form":form}
    return render(request, "post_form.html", context)

def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created Successfully")
    
    else:
        form = UserCreationForm()
   
    context = {"form": form}

    return render(request, "create_user.html", context)

def custom_create_user(request):
    if request.method == "POST":
       
    # else:
    #     form = UserCreationForm()
       username = request.POST.get("username")
       email = request.POST.get("email")
       password = request.POST.get("password")
       confirm_password = request.POST.get("confirm_password")

       if not(username and email and password and confirm_password):
           messages.error(request, "All field are required")
           return redirect("custom_create_user")

       if User.objects.filter(username=username).exists():
           messages.error(request, "Username taken")
           return redirect ("custom_create_user")

       if password != confirm_password:
           messages.error(request, "Passwords do not match")
           return redirect("custom_create_user")

       User.objects.create_user(
           username=username,
           email=email,
           password=password,
       )
       messages.success(request, "User created successfully")
       return redirect("custom_create_user")

   
    return render(request, "custom_create_user.html")


def student_login(request):
    if request.user.is_authenticated:
        return redirect("student_list")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("student_list")

        messages.error(request, "Invalid username or password.")

    return render(request, "students/auth/login.html")


def student_signup(request):
    if request.user.is_authenticated:
        return redirect("student_list")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created. Please log in.")
            return redirect("student_login")

    return render(request, "students/auth/signup.html")


def student_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect("student_login")


def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html", {"students": students})


def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "students/custom_user_create.html", {"form": form, "page_title": "Add Student"})


@login_required(login_url="student_login")
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "students/custom_user_create.html", {
        "form": form,
        "student": student,
        "page_title": "Edit Student",
    })


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})









