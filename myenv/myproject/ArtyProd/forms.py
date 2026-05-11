from ArtyProd import models
from ArtyProd.models import Service,Detail,Projet,Question,Personnel
from django import forms


from django import forms
from .models import Equipe

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nom', 'description']


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'description', 'categorie', 'img']

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['service', 'fichier']

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['nom', 'description', 'client', 'date_debut', 'date_fin', 'services', 'equipe', 'fichier', 'customer']

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text="Sélectionnez les services associés à ce projet."
    )

    fichier = forms.FileField(
        required=False,
        help_text="Joindre un fichier si nécessaire."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['services'].initial = self.instance.services.all()
            self.fields['fichier'].initial = self.instance.fichier

def save(self, commit=True):
    projet = super().save(commit=False)
    if commit:
        projet.save()
    services = self.cleaned_data.get('services')
    if services:
        projet.services.set(services)
        if self.cleaned_data.get('fichier'):
            for service in services:
                Detail.objects.create(
                    projet=projet,
                    service=service,
                    fichier=self.cleaned_data['fichier']
                )
    return projet


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }
