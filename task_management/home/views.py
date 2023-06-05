from django.shortcuts import render

def home_view(request):
    #check if user is logged in or not and conditionally render the home page 
    
    if request.user.is_authenticated:    
        return render(request,'home.html',context={"logged_in":True,"user":request.user})
    else:
        return render(request,'home.html',context={"logged_in":False})
