from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackend
from django.contrib .auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser


def BASE(request):
    return render(request, 'base.html')

def LOGIN(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        backend = EmailBackend()
        user = backend.authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            user_type = user.user_type

            if user_type == '1':
                return redirect('Hod_Home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return HttpResponse("Student Dashboard")
            else:
                messages.error(request, "Invalid user type!")
                return redirect('login')

        else:
            messages.error(request, "Invalid email or password!")
            return redirect('login')

    return redirect('login')

def dologout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        'user': user
    }
    return render(request, 'profile.html', context)
@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            # Get the logged-in user instance
            user = CustomUser.objects.get(id=request.user.id)

            user.first_name = first_name
            user.last_name = last_name

            if password:
                user.set_password(password)

            if profile_pic:
                user.profile_pic = profile_pic

            user.save()

            messages.success(request, "Profile updated successfully")
            return redirect('profile')

        except Exception as e:
            print(e)
            messages.error(request, "Failed to update profile")
            return redirect('profile')

    return render(request, 'profile.html')


