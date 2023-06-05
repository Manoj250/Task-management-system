from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Tasks
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


def sort_results(user_name,sort_by_date,reverse_result,complete):
    '''
        This function is used to sort the results in specified order,
        either based on priority or due date
    '''
   
    priority_dict = {"Low":1,"Medium":2,"High":3}
    tasks = Tasks.objects.filter(username=user_name,completed=complete)
    if sort_by_date:
        tasks = sorted(tasks,key=lambda x:x.due_date.timestamp(),reverse=True if reverse_result else False)
    else:
        tasks = sorted(tasks,key=lambda x:priority_dict[x.priority],reverse=True if reverse_result else False)
    return tasks

def delete_or_update(username,card_details,delete):
    '''
        This function is used to delete the object or update the object
    '''
    
    task = card_details[0]
    assigned_to = card_details[1]
    desc = card_details[2]
    due_date = card_details[3]
    priority = card_details[4]
    
    t = Tasks.objects.filter(
                                username=username,
                                desc=desc,
                                task=task,
                                assigned_to=assigned_to,
                                priority=priority
                            )[0]
    
    if delete:
        t.delete()
    else:
        t.completed = "Completed"
        t.save()
        

#login required decorator is used when you want to restrict users from accessing a page which requires authetication

@login_required(login_url="/login/")
def user_view(request,u_name):
        
    username = request.user
    email_status=0
    to_mail = None
    
    #checking if the current user name matches with the logged in user name
    
    if u_name!=str(username):
        return HttpResponse(f"please logout of the \"{username}\" account and log into \"{u_name}\" account")
    
    sort_by_date = True
    reverse_result = False
    
    if request.method == "GET":
        
        
        sort_by = request.GET.get("sort_by",None)
        order_by = request.GET.get("order_by",None)
        status = request.GET.get("status",None)
        mail_details = request.GET.get("mail_details",None)
        
        #if sort by option is specified then sort according to that
        if sort_by is not None:
            if sort_by == "due_date":
                sort_by_date = True
            else:
                sort_by_date = False
            
            if order_by == "ascending":
                reverse_result = False
            else:
                reverse_result = True
        
        
        #show completed tasks
        if status is not None and status == "completed":
            tasks = sort_results(request.user,sort_by_date,reverse_result,"Completed")
            return render(request,"user_page.html",context={"tasks":tasks,"username":username,"sort_by":"due_date" if sort_by_date else "priority","order_by":"descending" if reverse_result else "ascending","completed":"Pending"})
        
        #functionality for sending email
        if mail_details is not None:
            card_details = mail_details.split("&")
            task = card_details[0]
            assigned_to = card_details[1]
            desc = card_details[2]
            due_date = card_details[3]
            priority = card_details[4]
            to_mail = card_details[5]
            
            email_status = send_mail(f"{task} notification",f"This is to notify that your task {task} is nearing deadline of {due_date}, \n task details are as below :\n {desc} \n take this task as a {priority} priority",settings.EMAIL_HOST_USER,[to_mail],fail_silently=False)
       
       #get the tasks
        tasks = sort_results(request.user,sort_by_date,reverse_result,"Not completed")
        return render(request,"user_page.html",context={"tasks":tasks,"username":username,"sort_by":"due_date" if sort_by_date else "priority","order_by":"descending" if reverse_result else "ascending","completed":"completed","email":True if mail_details is not None else False,"email_status":"successfully sent" if email_status>0 else "failed to send","sent_to":to_mail})
    
    elif request.method == "POST":
        mark_as_done = request.POST.get("mark_as_done",None)
        delete = request.POST.get("delete",None)
    
        #functionality for marking a task as done
        if mark_as_done is not None:
            card_details = request.POST["card_details"].split("&")
            delete_or_update(username,card_details,False)
            tasks = sort_results(request.user,sort_by_date,reverse_result,"Not completed")
            return render(request,"user_page.html",context={"tasks":tasks,"username":username,"sort_by":"due_date" if sort_by_date else "priority","order_by":"descending" if reverse_result else "ascending","completed":"completed"})

        #functionality for deleting the task
        if delete is not None:
            card_details = request.POST["card_details"].split("&")
            delete_or_update(username,card_details,True)
            tasks = sort_results(request.user,sort_by_date,reverse_result,"Not completed")
            return render(request,"user_page.html",context={"tasks":tasks,"username":username,"sort_by":"due_date" if sort_by_date else "priority","order_by":"descending" if reverse_result else "ascending","completed":"completed"})
    
        task = request.POST["task"]
        due_date = request.POST["due_date"]
        desc = request.POST["desc"]
        priority = request.POST["priority"]
        assigned_to = request.POST["assigned_to"]
        resource_mail = request.POST["rmail"]
        
        # datetime(year, month, day, hour, minute, second, microsecond)
        # 2023-05-26T14:16
        #making python datetime object to store date in database
        dt = datetime(int(due_date.split("-")[0]),
              int(due_date.split("-")[1]),
              int(due_date.split("-")[2].split("T")[0]),
              int(due_date.split("-")[2].split("T")[1].split(":")[0]),
              int(due_date.split("-")[2].split("T")[1].split(":")[1]),
              )
        
        #check if task already exists
        t = Tasks.objects.filter(username=username,desc=desc,task=task,due_date=dt,priority=priority,assigned_to=assigned_to,assigned_mail=resource_mail)
        
        if not t:
            t = Tasks(username=username,desc=desc,task=task,due_date=dt,priority=priority,assigned_to=assigned_to,assigned_mail=resource_mail)
            t.save()
        else:
            messages.info(request, 'Task already exists!')

        
        tasks = sort_results(request.user,sort_by_date,reverse_result,"Not completed")
        return render(request,"user_page.html",context={"tasks":tasks,"username":username,"sort_by":"due_date" if sort_by_date else "priority","order_by":"descending" if reverse_result else "ascending","completed":"completed"})
    else:
        return HttpResponse("Wrong method!")