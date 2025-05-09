"""
URL configuration for freelancersPlatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from . import views
urlpatterns = [
    path('create/user/', views.createUser),
    path('view/users/', views.userView),
    path('view/user-details/', views.userDetails),
    path('profile/me/', views.authUser),
    path('profile/update/', views.authUserUpdate),
    path('profile/complete/', views.userProfileComplete),
    path('add/skills/', views.addSkill),
    path('list/freelancers/', views.listFreelancers),
    path('project/', views.project),
    path('open/project/', views.listOpenProjects),
    path('closed/project/', views.listClosedProjects),
    path('bid/', views.bids),
    path('bid/close/', views.closeProject),
    path('contract/completed/<int:project_id>', views.completeProject),
    path('bid/<int:project_id>', views.projectWiseBid),
] 
