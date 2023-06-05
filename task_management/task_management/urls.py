"""
URL configuration for task_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as home_views
from auth_page import views as auth_views
from user_page import views as user_views


#these are the url routes mapped to functions(also called as views)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_views.home_view),
    path('login/',auth_views.login_session),
    path('create_account/',auth_views.create_account),
    path('logout/',auth_views.logout_session),
    path('user/<str:u_name>/',user_views.user_view)
]
