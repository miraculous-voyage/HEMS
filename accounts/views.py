from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Extrainfo

def signup(request):
    if request.method == 'POST':
        cp = request.FILES.get('image')
        if request.POST['password1']== request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'*Username has already been taken !'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                auth.login(request, user)
                user_extrainfo = Extrainfo()
                user_extrainfo.user_name = request.user
                if cp is not None:     
                    user_extrainfo.user_image = request.FILES['image'] 
                user_extrainfo.save()    
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'*Password didn\'t match !'})
    else:
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'accounts/signup.html')


@login_required(login_url="/accounts/signup")
def update(request):
    if request.method == 'POST':
        uname = request.user.username
        cp = request.POST.get('cp')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        propic = request.FILES.get('image')
        message = list(("You","have","successfully","updated"))
        count = 0
        print(cp)
        if cp is not None:
            user = auth.authenticate(username=request.user.username,password=cp)
            if user is not None:
                if request.POST['np1']== request.POST['np2']:
                # password update
                    request.user.set_password(request.POST['np1'])
                    request.user.save()
                    updated_user = auth.authenticate(username=uname,password=request.POST['np1'])
                    auth.login(request, updated_user)
                    count =1
                    message.append(" [Password]")
                else:
                #password doesn't match
                    return render(request, 'accounts/update.html', {'error':'*Password doesn\'t match !'})
            else:
                # Current password wrong
                return render(request, 'accounts/update.html', {'error':'*Current Password is wrong !'})
        #full name update
        if fname is not None:
            request.user.first_name = fname
            count =1
            message.append(" [First Name]")
        if lname is not None:
            request.user.last_name = lname
            count =1
            message.append(" [Last Name]")
        request.user.save()

        if propic is not None:
            #image update
            pic_info = Extrainfo.objects.get(user_name=request.user.username)
            pic_info.user_image = request.FILES["image"]
            pic_info.save()
            count =1
            message.append(" [Image]")
        match = request.user.username
        info = Extrainfo.objects.get(user_name=match)
        if count == 0:
            return render(request, 'accounts/update.html', {'error':'*There is nothing to update!', 'user': request.user, 'info': info})
        else:
            message.append(" Fields.")
            return render(request, 'accounts/update.html', {'messages':message, 'user': request.user, 'info': info})
    else:
        match = request.user.username
        info = Extrainfo.objects.get(user_name=match)
        return render(request, 'accounts/update.html', {'user': request.user, 'info': info})
            

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'*Username or password is incorrect!'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
