from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('customer-dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('customerclick', views.customerclick_view,name='customerclick'),
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customerlogin', LoginView.as_view(template_name='ArtyProd/adminlogin.html'),name='customerlogin'),

    path('ask-question', views.ask_question_view,name='ask-question'),
    path('question-history', views.question_history_view,name='question-history'),
]