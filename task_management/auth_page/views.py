from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User


def login_session(request):
    #this function controls the login functionality
    
    #render the login form on get request
    
    if request.method == "GET":
        return render(request,"login.html",{"error":False})
    
    #if the method is post then validate the login request
    
    elif request.method == "POST":
        u_name = request.POST["user_name"]
        password = request.POST["password"]
        
        user = authenticate(request, username=u_name, password=password)
        if user is not None:
            login(request=request,user=user)
            return redirect(f"/user/{u_name}")
            
        #if username authentication fails try with email 
        
        elif User.objects.filter(email=u_name).exists():            
            u_name = User.objects.get(email=u_name).username
            user = authenticate(request, username=u_name, password=password)
            if user is not None:
                login(request=request,user=user)
                return redirect(f"/user/{u_name}")
            else:                
                return render(request,"login.html",{"error":True,"error_message":"Invalid username/email or password"})
        else:        
            return render(request,"login.html",{"error":True,"error_message":"Invalid username/email or password"})
    else:
        #any other method other than get and put is not allowed
        return HttpResponse("Method not allowed on this url")

def create_account(request):
    
    #on get request display the create account form
    if request.method == "GET":
        return render(request,'create_account.html',{"error":False})
    
   #on post request validate the account credentials
    elif request.method == "POST":
        context = {"error":False}
        
        email = request.POST["email"]
        u_name = request.POST["user_name"]
        password = request.POST["password"]
        c_password = request.POST["confirm_password"]
        
        #if passwrod and confirm passowrds dont match display error
        if password != c_password:
            context["error"] = True
            context["error_message"] = "Your passwords do not match!"
            return render(request,'create_account.html',context)
        
        #if the account already exists display error
        if User.objects.filter(email=email).exists() or User.objects.filter(username=u_name).exists():
            context["error"] = True
            context["error_message"] = "This email or user name already exists!"
            return render(request,'create_account.html',context)
        
        user = User.objects.create_user(username=u_name,email=email,password=password)
        user.save()
        #login the user after account creation
        login(request,user)
        return redirect(f"/user/{u_name}")

    else:
        return HttpResponse("Method not allowed on this url")
    
def logout_session(request):
    #logout the user and render logout page
    logout(request)
    return render(request,'logout.html')
