from cProfile import label
from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from .models import (HumanResource, Ward, Role,
                    AreaFormazione, CorsoFormazione,
                    )


class HumanResourceModelForm(forms.ModelForm):
    class Meta:
        model = HumanResource
        fields = '__all__'
        exclude = ['created_at', 'updated_at']
        country = CountryField().formfield()
        
        widget = {
            
            'cognomedipendente': forms.TextInput(attrs={'class': 'form-control'}),
            'nomedipendente': forms.TextInput(attrs={'class': 'form-control'}),
            'country': CountrySelectWidget(),
            'immagine': forms.ImageField(),
            'gender': forms.ChoiceField(),
            'dataassunzione': forms.DateInput(),
            'datadimissioni': forms.DateInput(),
            'fk_mansione': forms.ChoiceField(),
            'fk_reparto': forms.ChoiceField(),
            'qualifica': forms.TextInput(attrs={'class': 'form-control'}),
            'commenti': forms.Textarea(attrs={'class': 'form-control'}),
            
        },
        labels = {
            'cognomedipendente': 'Cognome',
            'nomedipendente': 'Nome',
            'country': 'Nazionalità',
            'immagine': 'Foto',
            'gender': 'Genere',
            'dataassunzione': 'Data Assunzione',
            'datadimissioni': 'Data Dimissioni',
            'fk_mansione': 'Mansione',
            'fk_reparto': 'Reparto',
            'qualifica': 'Qualifica',
            'commenti': 'Commenti',

        }

class WardModelForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = '__all__'

class RoleModelForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        
class AreaFormazioneModelForm(forms.ModelForm):
    class Meta:
        model = AreaFormazione
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Area Formazione'}),            
            'created_by': forms.HiddenInput()
        }
        
class CorsoFormazioneModelForm(forms.ModelForm):
    class Meta:
        model = CorsoFormazione
        fields = '__all__'
        fk_areaformazione = forms.ModelChoiceField(queryset=AreaFormazione.objects.all())
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Corso Formazione'}),
            'fk_areaformazione': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Corso di Formazione',
            'fk_areaformazione': 'Area Formazione',
            

        }
        