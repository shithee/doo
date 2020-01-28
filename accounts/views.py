from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo.models import Project,Outline,Task
from django.contrib import auth as admin_auth
from django.contrib.auth.decorators import login_required


def signup(request):
  
    if request.method == 'POST':
        email         = request.POST['email']
        username      = request.POST['username']
        password      = request.POST['password']
        cpassword     = request.POST['cpassword']
        
        if((password != cpassword) or (not email) or (not username)):
            return render(request,'signup.html',{'message': "Please fill the form correctly..!"})
        else:
            user = User.objects.create_user(
                email= email,
                username=username,
                password=password
            )
            return redirect('home')

    return render(request,'signup.html')

def login(request):

    if request.method == 'POST':

        username  = request.POST['username']
        password  = request.POST['password']
        nextview  = request.POST['next']

        if( not username or not password):
            return render(request,'login.html',{'message': "Please fill all fields...!"})
        
        user = admin_auth.authenticate(username=username,password=password)

        if user is not None:
            admin_auth.login(request,user)
            redirection = nextview and nextview or 'home' 
            return redirect(redirection)

        return render(request,'login.html',{'message': "Invalid login data ..!"})
        

    return render(request,'login.html')

@login_required
def password(request):
    
    if request.method == 'POST':

        cur_pass  = request.POST['password']
        new_pas1  = request.POST['password1']
        new_pas2  = request.POST['password2']
        username  = request.user.username

        if((new_pas1 != new_pas2) or not cur_pass):
            return render(request,'password.html',{'message': "Please fill all fields ..!"})
        
        u = User.objects.get(username__exact=username)
        is_ok = request.user.check_password(cur_pass)

        if is_ok:
            u.set_password(new_pas1)
            u.save()
            return render(request,'password.html',{'message': "Password changed successfully ...!"})
        else:            
            return render(request,'password.html',{'message': "Wrong Password ...!"})

    return render(request,'password.html')

@login_required
def profile(request):
    
    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)
    outlines = Outline.objects.filter(created_by=userid)

    return render(request,'profile.html',{'projects' : projects, 'outlines' : outlines })

@login_required
def edit_profile(request):

    if request.method == 'POST':

        userid = request.user.id
        username = request.POST['username']
        email = request.POST['email']
        bio = request.POST['bio']

        if (not username or not email):
             return render(request,'edit_profile.html',{'message': "Please fill all fields ..!"})
        else :    
             user = User.objects.get(pk=userid)
             user.username = username
             user.email  = email
             user.profile.bio = bio
             if len(request.FILES) != 0:
                 profile = request.FILES['profile']
                 user.profile.image = profile
             user.save()

        return render(request,'edit_profile.html',{'message': "Profile updated successfully..!"})

    return render(request,'edit_profile.html')