from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from .models import Project,Outline,Task
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Now
import json

@login_required
def home(request):

    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)
    outlines = Outline.objects.filter(created_by=userid)

    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    #start = datetime.combine(today, time())
    end = datetime.combine(tomorrow, time())

    tasks        = Task.objects.filter(created_by=userid,status=False,deadline__lte=end).order_by('deadline')
    completed    = Task.objects.filter(created_by=userid,status=True,deadline__lte=end).order_by('deadline')[:5]

    return render(request, 'home.html',{'projects': projects, 'outlines' : outlines, 'tasks': tasks,'latest': completed, 'head': 'Today 🔥'})

@login_required
def week(request):

    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)
    outlines = Outline.objects.filter(created_by=userid)

    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end   = start + timedelta(7)

    print(start,end)

    tasks    = Task.objects.filter(created_by=userid,status=False,deadline__range=[start,end]).order_by('deadline')
    completed    = Task.objects.filter(created_by=userid,status=True,deadline__range=[start,end]).order_by('deadline')[:5]

    return render(request, 'home.html',{'projects': projects, 'outlines' : outlines, 'tasks': tasks,'latest': completed, 'head': 'This Week 🌟'})

@login_required
def project(request,project_id):

    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)
    outlines = Outline.objects.filter(created_by=userid)

    tasks        = Task.objects.filter(created_by=userid,status=False,outline__project=project_id).order_by('deadline')
    completed    = Task.objects.filter(created_by=userid,status=True,outline__project=project_id).order_by('deadline')[:5]

    project  = get_object_or_404(Project, pk=project_id)
    return render(request, 'home.html',{'projects': projects,'outlines' : outlines,'latest': completed, 'tasks': tasks,'head': project.name })

    
@login_required
def outline(request,oid):

    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)
    outlines = Outline.objects.filter(created_by=userid)

    tasks       = Task.objects.filter(status=False,outline=oid).order_by('deadline')
    completed    = Task.objects.filter(status=True,outline=oid).order_by('deadline')[:5]
    project     = get_object_or_404(Outline, pk=oid)
    return render(request, 'home.html',{'projects': projects,'outlines' : outlines,'latest': completed, 'tasks': tasks,'head': project.name })


@login_required
def new_outline(request):
   
    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)

    if request.method == 'POST':
        name      = request.POST['name']
        deadline  = request.POST['deadline']
        project   = request.POST['project']
        
        if not name or not deadline or not project:          
              return render(request, 'new_outline.html',{'projects': projects, 'message': 'Please fill all fields..!'})
        
        
        outline_count = Outline.objects.filter(created_by=userid).count()
        if outline_count>=5:
             return render(request, 'new_outline.html',{'projects': projects, 'message': 'You already have too much work..!'})              

        user = User.objects.get(id=request.user.id)

        outline = Outline.objects.create(
            name = name,
            deadline = deadline,
            created_by = user,
            project = Project.objects.get(pk=project)
        )
        return redirect('/outline/{id}'.format(id=outline.id))

    return render(request, 'new_outline.html',{'projects': projects})

@login_required
def new_project(request):

    userid = request.user.id
    if request.method == 'POST':
        name      = request.POST['name']
        desc     = request.POST['description']
        is_fav   = request.POST.get('favourite',False)
        fav      = (is_fav == 1) and True or False

        if not name:          
              return render(request, 'new_project.html',{'message': 'Please fill all fields ..!'})
        
        project_count = Project.objects.filter(created_by=userid).count()
        if project_count>=2:
             return render(request, 'new_project.html',{'message': 'You already have too much work..!'}) 
       
        user = User.objects.get(id=request.user.id)

        project = Project.objects.create(
            name = name,
            description = desc,
            created_by = user,
            favourite = fav
        )
        return redirect('home')
   
    return render(request, 'new_project.html')

@login_required
def finished(request):

    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)
    outlines = Outline.objects.filter(created_by=userid)
    tasks    = Task.objects.filter(created_by=userid,status=True).order_by('-closed_at')
    return render(request, 'home.html',{'projects': projects,'outlines' : outlines,'tasks': tasks,'head': 'Finished Tasks ✔' })
 
@login_required
def urgent(request):

    userid = request.user.id
    projects = Project.objects.filter(created_by=userid)
    outlines = Outline.objects.filter(created_by=userid)
    tasks        = Task.objects.filter(created_by=userid,status=False,priority=1).order_by('closed_at')
    completed    = Task.objects.filter(created_by=userid,status=True,priority=1).order_by('closed_at')
    return render(request, 'home.html',{'projects': projects,'outlines' : outlines,'latest': completed, 'tasks': tasks,'head': 'Urgent ⚡' })   

@login_required 
@csrf_exempt
def new_task(request):   
     if request.is_ajax():
         
        input_data = request.POST
        if input_data['name']:

             user = User.objects.get(id=request.user.id)
             if input_data['outline']:
                 outline = Outline.objects.get(pk=input_data['outline'])
             else:
                 outline = None
             task = Task.objects.create(
                  name = input_data['name'],
                  deadline = input_data['deadline'],
                  priority = input_data['priority'],
                  created_by = user,
                  status = False,
                  outline = outline
                    )
             task_data = Task.objects.filter(id=task.id).values()
             response = { 'status': 'ok' ,'data' : list(task_data) }
     else:         
         response = {'status' : 'error', 'data' : "Invalid request type" }

     return JsonResponse(response,safe=False)

@login_required 
@csrf_exempt
def finish_task(request):   
     if request.is_ajax():
         
        taskid = request.POST['id']
        if taskid:        

             Task.objects.filter(id = taskid).update(status = True,closed_at=Now())
             response = { 'status': 'ok' ,'data' : 'Task completed' }
        else:         
             response = {'status' : 'error', 'data' : "Invalid request type" }
         
     return JsonResponse(response,safe=False)

@login_required 
@csrf_exempt
def restore_task(request):   
     if request.is_ajax():
         
        taskid = request.POST['id']
        if taskid:        

             Task.objects.filter(id = taskid).update(status = False)
             response = { 'status': 'ok' ,'data' : 'Task completed' }
        else:         
             response = {'status' : 'error', 'data' : "Invalid request type" }
         
     return JsonResponse(response,safe=False)

@login_required 
@csrf_exempt
def delete_task(request):   
    if request.is_ajax():
         
        taskid = request.POST['id']
        if taskid:        

             Task.objects.filter(id = taskid).delete()
             response = { 'status': 'ok' ,'data' : 'Task deleted'}
        else:         
             response = {'status' : 'error', 'data' : "Invalid request type" }
         
    return JsonResponse(response,safe=False)


    