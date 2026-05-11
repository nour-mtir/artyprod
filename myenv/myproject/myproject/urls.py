"""
URL configuration for myproject project.

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
from  ArtyProd import views

from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path,include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/',include('customer.urls')),
    
    path('',views.home_view,name=''),
    path('logout/', LogoutView.as_view(template_name='ArtyProd/logout.html'), name='logout'),
     path('ArtyProd/aboutus/', views.aboutus_view, name='aboutus'),
    path('ArtyProd/contactus/', views.contactus_view, name='contactus'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    
    path('adminlogin/', LoginView.as_view(template_name='ArtyProd/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    
    path('admin-view-customer/', views.admin_view_customer_view, name='admin-view-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    
    path('admin-question/', views.admin_question_view,name='admin-question'),
    path('update-question/<int:pk>', views.update_question_view,name='update-question'),
    
    path('service-list/', views.service_list_view, name='service-list'),
    path('create-service/', views.create_service_view, name='create-service'),
    path('update-service<int:pk>/', views.update_service_view, name='update-service'),
    path('delete-service<int:pk>/', views.delete_service_view, name='delete-service'),

    path('projet-list/', views.projet_list_view, name='projet_list'),
    path('projet/<int:id>/', views.projet_detail_view, name='projet-detail'),


    path('projet/create/', views.projet_create_view, name='projet-create'),
    path('projet/<int:projet_id>/update/', views.projet_update_view, name='projet-update'),
    path('projet/<int:projet_id>/delete/', views.projet_delete_view, name='projet-delete'),

    path('equipe-list/', views.Equipe_List_View.as_view(), name='equipe-list'),
    path('ArtyProd/equipe-create', views.Equipe_Create_View.as_view(), name='ArtyProd/equipe-create'),
    path('equipe/<int:pk>/', views.Equipe_Detail_View.as_view(), name='equipe-detail'),
    path('equipe/<int:pk>/update/', views.Equipe_Update_View.as_view(), name='equipe-update'),
    path('equipe/<int:pk>/delete/', views.Equipe_Delete_View.as_view(), name='equipe-delete'),

    path('personnel-list/', views.Personnel_List_View.as_view(), name='personnel-list'),
    path('personnel-create/', views.Personnel_Create_View.as_view(), name='personnel_create'),
    path('personnel-detail/<int:pk>/',views.Personnel_Detail_View.as_view(), name='personnel_detail'),
    path('personnel/<int:pk>/update/', views.Personnel_Update_View.as_view(), name='personnel_update'),
    path('personnel/<int:pk>/delete/', views.Personnel_Delete_View.as_view(), name='personnel_delete'),

    path('tache-list/', views.TacheListView.as_view(), name='tache_list'),
    path('tache-detail/<int:pk>/', views.TacheDetailView.as_view(), name='tache_detail'),
    path('tache-create/', views.TacheCreateView.as_view(), name='tache_create'),
    path('tache/<int:pk>/update/', views.TacheUpdateView.as_view(), name='tache_update'),
    path('tache/<int:pk>/delete/', views.TacheDeleteView.as_view(), name='tache_delete'),









]














   
