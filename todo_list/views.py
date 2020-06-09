from django.shortcuts import render, redirect
from . models import List
from . forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import re
# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(
                request, 'Invalid username or password! Please try again.')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'logout.html')


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        # password regx
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, password)

        if mat:
            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username already exists.")
                    return redirect('registration')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exist.')
                    return redirect('registration')

                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    messages.info(
                        request, 'User registered successfully!')
                    return redirect('registration')
            else:
                messages.info(request, 'Password does not match!')
                return redirect('registration')
        else:
            messages.error(
                request, 'Password must contain at least one uppercase and lowercase letter.')
            messages.error(
                request, 'Password must contain at least one number.')
            messages.error(
                request, 'Password must contain at least one special symbol.')
            messages.error(
                request, 'Password should be between 6 to 20 characters long.')
            return redirect('registration')
    else:
        return render(request, 'registration.html')


@login_required()
def home(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)
        print(form)
        if form.is_valid():
            form.save()
            all_items = List.objects.filter(username=request.user)
            messages.success(request, ('Item has been added to list!'))
            return render(request, 'home.html', {'all_items': all_items})
        else:
            return HttpResponse('Form fails to validate.')
    else:
        all_items = List.objects.filter(username=request.user)
        return render(request, 'home.html', {'all_items': all_items})


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def delete(request, list_id):
    item = List.objects.get(id=list_id)
    item.delete()
    messages.success(request, ('Item has been deleted from your list!'))
    return redirect('home')


@login_required
def cross_off(request, list_id):
    item = List.objects.get(id=list_id)
    item.completed = True
    item.save()
    return redirect('home')


@login_required
def uncross(request, list_id):
    item = List.objects.get(id=list_id)
    item.completed = False
    item.save()
    return redirect('home')


@login_required
def edit(request, list_id):
    if request.method == 'POST':
        item = List.objects.get(pk=list_id)
        form = ListForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, ('Item has been edited!'))
            return redirect('home')

    else:
        item = List.objects.get(pk=list_id)
        return render(request, 'edit.html', {'item': item})
