from datetime import date

from django import forms
from django.db.models import Max

from .models import *


class EstintoreModelForm(forms.ModelForm):
    
    
    class Meta:
        model = Estintore
        fields= '__all__'
        widgets = {
            'tipo_estinguente': forms.TextInput(attrs={'placeholder': 'Inserisci il tipo estinguente (polvere, idrico, ...)'}),
            'classe': forms.TextInput(attrs={'placeholder': 'Inserisci la classe (113B, 34A233BC, ...)'}),
            'peso': forms.TextInput(attrs={'placeholder': 'Inserisci il peso'}),
            'matricola': forms.TextInput(attrs={'placeholder': 'Inserisci il numero di matricola'}),
            'anno': forms.TextInput(attrs={'placeholder': 'Inserisci l\'anno di fabbricazione'}),
            'ubicazione': forms.TextInput(attrs={'placeholder': 'Inserisci la posizione o il reparto'}),
            'data_dismissione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'numero_posizione': forms.TextInput(attrs={'placeholder': 'Inserisci il numero assegnato'}),
            'scadenza_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'scadenza_collaudo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'tipo_estinguente': 'Tipo estinguente',
            'classe': 'Classe',
            'peso': 'Peso',
            'matricola': 'Matricola',            
            'anno': 'Anno di fabbricazione',            
            'ubicazione': 'Ubicazione',            
            'data_dismissione': 'Data Dismissione',            
            'numero_posizione': 'Numero/Posizione',            
            'scadenza_revisione': 'Scadenza Revisione',            
            'scadenza_collaudo': 'Scadenza Collaudo',            
            'note': 'Note'

        }



class IdranteModelForm(forms.ModelForm):   
    
    
    class Meta:
        model = Idrante
        fields= '__all__'
        widgets = {
            'numero_posizione': forms.TextInput(attrs={'placeholder': 'Inserisci il numero assegnato'}),
            'tipo_idrante': forms.Select(),
            'uni': forms.TextInput(attrs={'placeholder': 'Uni'}),
            'metri': forms.TextInput(attrs={'placeholder': 'Metri'}),
            'anno': forms.TextInput(attrs={'placeholder': 'Inserisci l\'anno di fabbricazione'}),
            'data_dismissione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'scadenza_schiuma': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'scadenza_collaudo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'ubicazione': forms.TextInput(attrs={'placeholder': 'Inserisci la posizione o il reparto'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'numero_posizione': 'Numero/Posizione',            
            'tipo_idrante': 'Tipo Idrante',
            'uni': 'Uni',
            'metri': 'Metri',
            'anno': 'Anno di fabbricazione',            
            'data_dismissione': 'Data Dismissione',            
            'scadenza_schiuma': 'Scadenza Schiuma',            
            'scadenza_collaudo': 'Scadenza Collaudo',            
            'ubicazione': 'Ubicazione',            
            'note': 'Note'
                     

        }


class PortaUscitaModelForm(forms.ModelForm):   
    
    class Meta:
        model = PortaUscita
        fields= '__all__'
        widgets = {
            'numero_posizione': forms.TextInput(attrs={'placeholder': 'Inserisci il numero assegnato'}),
            'tipo_porta': forms.Select(),
            #'marcatura_ce': forms.TextInput(attrs={'placeholder': 'Uni'}),
            'maniglia': forms.Select(),
            'anta': forms.Select(),
            'matricola': forms.TextInput(attrs={'placeholder': 'Inserisci il numero di matricola'}),
            'ubicazione': forms.TextInput(attrs={'placeholder': 'Inserisci la posizione o il reparto'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
            
        }
        labels = {
            'numero_posizione': 'Numero/Posizione',            
            'tipo_porta': 'Tipo Porta',
            'marcatura_ce': 'Marcata CE',
            'maniglia': 'Maniglia',
            'anta': 'Anta',            
            'matricola': 'Matricola',            
            'ubicazione': 'Ubicazione',            
            'note': 'Note'
        }
        

class AttrezzaturaAntincendioModelForm(forms.ModelForm):   
    
    class Meta:
        model = AttrezzaturaAntincendio
        fields= '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci la descrizione'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
            
        }
        labels = {
            'descrizione': 'Descrizione', 
            'note': 'Note'
        }

class ImpiantoSpegnimentoModelForm(forms.ModelForm):   
    
    class Meta:
        model = ImpiantoSpegnimento
        fields= '__all__'
        widgets = {
            'numero_posizione': forms.TextInput(attrs={'placeholder': 'Inserisci numero/posizione'}),            
            'ubicazione': forms.TextInput(attrs={'placeholder': 'Inserisci la posizione o il reparto'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
            
        }
        labels = {
            'numero_posizione': 'Numero/Posizione',
            'ubicazione': 'Ubicazione',          
            'note': 'Note'
        }



class RegistroControlliAntincendioModelForm(forms.ModelForm):   
    fk_fornitore = forms.ModelChoiceField(
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore',
        required=False
    )
    fk_operatore = forms.ModelChoiceField(
        queryset=HumanResource.objects.all(),
        label='Operatore', 
        required=False
    )

    class Meta:
        model = RegistroControlliAntincendio
        fields= '__all__'
        widgets = {
            'interno_esterno': forms.Select(),
            'numero_intervento': forms.TextInput(attrs={'placeholder': 'Inserisci il numero intervento, se presente...'}),
            
            'data_intervento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'prossima_scadenza': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
            
        }
        labels = {
            'interno_esterno': 'Interno/Esterno',            
            'numero_intervento': 'Numero intervento',
            'data_intervento': 'Data intervento',
            'prossima_scadenza': 'Prossima scadenza',                      
            'note': 'Note'
        }


