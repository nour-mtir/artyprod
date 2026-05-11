from django.shortcuts import render, redirect, reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms as CFORM
from .import forms



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request, 'ArtyProd/index.html')

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):      
        return redirect('customer/customer-dashboard')
    else:
        return redirect('admin-dashboard')



#de l'admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        'total_project':models.Projet.objects.all().count(),
        'total_service':models.Service.objects.all().count(),
        'total_question':models.Question.objects.all().count(),
        'total_Equipe':models.Equipe.objects.all().count(),
        'total_Personnel':models.Personnel.objects.all().count(),
    }
    return render(request,'ArtyProd/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'ArtyProd/admin_view_customer.html',{'customers':customers})

@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=CFORM.CustomerUserForm(instance=user)
    customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CFORM.CustomerUserForm(request.POST,instance=user)
        customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'ArtyProd/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'ArtyProd/admin_question.html',{'questions':questions})

def update_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'ArtyProd/update_question.html',{'questionForm':questionForm})

def aboutus_view(request):
    return render(request,'ArtyProd/aboutus.html')

from django.core.mail import send_mail
from django.conf import settings


def contactus_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        message_body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"

        send_mail(
            'Contact Form Submission',
            message_body,
            settings.EMAIL_HOST_USER,  # Utilisation de l'adresse e-mail de l'hôte comme expéditeur
            ['nourmtir36@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'ArtyProd/contactussuccess.html')
    return render(request, 'ArtyProd/contactus.html')


from django.shortcuts import render
from .models import Service

def service_list_view(request):
    services = Service.objects.all()
    return render(request,'ArtyProd/service_list.html', {'services': services})

from django.shortcuts import render, redirect
from .forms import ServiceForm

def create_service_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service-list')  # Rediriger vers une vue d'affichage des services
    else:
        form = ServiceForm()
    return render(request, 'ArtyProd/create_service.html', {'form': form})

def update_service_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service-list')  # Rediriger vers une vue d'affichage des services
    else:
        form = ServiceForm(instance=service)
    return render(request, 'ArtyProd/update_service.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect, render
from .models import Service

def delete_service_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service-list')  # Rediriger vers la liste des services après la suppression
    return render(request, 'ArtyProd/delete_service.html', {'service': service})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Projet
from .forms import ProjetForm

def projet_list_view(request):
    projets = Projet.objects.all()
    return render(request, 'ArtyProd/projet_list.html', {'projets': projets})

def projet_detail_view(request, id):
    projet = get_object_or_404(Projet, id=id)
    return render(request, 'ArtyProd/projet_detail.html', {'projet': projet})


def projet_create_view(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projet_list')
    else:
        form = ProjetForm()
    return render(request, 'ArtyProd/projet_create.html', {'form': form})

def projet_update_view(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    if request.method == 'POST':
        form = ProjetForm(request.POST, request.FILES, instance=projet)
        if form.is_valid():
            form.save()
            return redirect('projet_list')
    else:
        form = ProjetForm(instance=projet)
    return render(request, 'ArtyProd/projet_update.html', {'form': form, 'projet': projet})

def projet_delete_view(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    if request.method == 'POST':
        projet.delete()
        return redirect('projet_list')
    return render(request, 'ArtyProd/projet_confirm_delete.html', {'projet': projet})

from django.views.generic import ListView
from .models import Equipe

class Equipe_List_View(ListView):
    model = Equipe
    template_name = 'ArtyProd/equipe_list.html'
    context_object_name = 'equipes'

from django.views.generic import DetailView
from .models import Equipe

class Equipe_Detail_View(DetailView):
    model = Equipe
    template_name = 'ArtyProd/equipe_detail.html'
    context_object_name = 'equipe'

from django.views.generic.edit import CreateView
from .models import Equipe
from django.urls import reverse

class Equipe_Create_View(CreateView):
    model = Equipe
    template_name = 'ArtyProd/equipe_create.html'
    fields = ['nom', 'description']

    def get_success_url(self):
        return reverse('equipe-detail', args=[self.object.pk])

from django.views.generic.edit import UpdateView
from .models import Equipe
from .forms import EquipeForm

class Equipe_Update_View(UpdateView):
    model = Equipe
    template_name = 'ArtyProd/equipe_update.html'
    form_class = EquipeForm
    success_url = '/equipe-list/'  # Remplacez l'URL avec celle souhaitée



from django.views.generic.edit import DeleteView
from .models import Equipe
from django.urls import reverse_lazy

class Equipe_Delete_View(DeleteView):
    model = Equipe
    template_name = 'ArtyProd/equipe_confirm_delete.html'
    success_url = reverse_lazy('equipe-list')


from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Personnel

class Personnel_List_View(LoginRequiredMixin, ListView):
    model = Personnel
    template_name = 'ArtyProd/personnel_list.html'
    context_object_name = 'personnel_list'
    # Optionnel : Spécifiez le contexte supplémentaire si nécessaire

class Personnel_Detail_View(DetailView):
    model = Personnel
    template_name = 'ArtyProd/personnel_detail.html'  # Assurez-vous d'avoir un template pour afficher les détails du personnel
    context_object_name = 'personnel'  # Nom du contexte pour accéder aux données du personnel dans le template

class Personnel_Create_View(LoginRequiredMixin, CreateView):
    model = Personnel
    template_name = 'ArtyProd/personnel_create.html'
    fields = ['user', 'equipe', 'poste', 'img']
    success_url = '/personnel-list/'  # URL de redirection après la création du personnel

    def form_valid(self, form):
        # Ajoutez un code supplémentaire si nécessaire avant de valider le formulaire
        return super().form_valid(form)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import Personnel


class Personnel_Update_View(LoginRequiredMixin, UpdateView):
    model = Personnel
    template_name = 'ArtyProd/personnel_update.html'
    fields = ['user', 'equipe', 'poste', 'img']


class Personnel_Delete_View(LoginRequiredMixin, DeleteView):
    model = Personnel
    template_name = 'ArtyProd/personnel_confirm_delete.html'
    success_url = reverse_lazy('personnel-list')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Tache

class TacheListView(LoginRequiredMixin, ListView):
    model = Tache
    template_name = 'ArtyProd/tache_list.html'
    context_object_name = 'tache_list'

class TacheDetailView(DetailView):
    model = Tache
    template_name = 'ArtyProd/tache_detail.html'
    context_object_name = 'tache'

class TacheCreateView(LoginRequiredMixin, CreateView):
    model = Tache
    template_name = 'ArtyProd/tache_create.html'
    fields = ['nom', 'personnel', 'description', 'projet', 'date_debut', 'date_fin', 'assignee_a', 'completee']
    success_url = reverse_lazy('tache_list')

    def form_valid(self, form):
        # Add additional code if needed before validating the form
        return super().form_valid(form)

class TacheUpdateView(LoginRequiredMixin, UpdateView):
    model = Tache
    template_name = 'ArtyProd/tache_update.html'
    fields = ['nom', 'personnel', 'description', 'projet', 'date_debut', 'date_fin', 'assignee_a', 'completee']
    context_object_name = 'tache'
    success_url = reverse_lazy('tache_list')

class TacheDeleteView(LoginRequiredMixin, DeleteView):
    model = Tache
    template_name = 'ArtyProd/tache_confirm_delete.html'
    context_object_name = 'tache'
    success_url = reverse_lazy('tache_list')






