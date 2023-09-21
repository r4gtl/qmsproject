from django import forms
from datetime import date
from django.db.models import Max


from .models import *
from articoli.models import Articolo




class OperazioneRicetteModelForm(forms.ModelForm):
    
    
    class Meta:
        model = OperazioneRicette
        fields= '__all__'
        
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione operazione'}),
            'ward_ref': forms.Select(),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
        }
        labels = {
            'descrizione': 'Descrizione',
            'ward_ref': 'Reparto',
            'note': 'Note'

        }


class RicettaRifinizioneModelForm(forms.ModelForm):
    
    
    class Meta:
        model = RicettaRifinizione
        fields= '__all__'
        fk_articolo = forms.ModelChoiceField(
            queryset=Articolo.objects.all(),            
            widget=forms.Select
            )
        
        
        widgets = {
            'numero_ricetta': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
            'data_ricetta': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),            
            'numero_revisione': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
            'data_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),            
            'ricetta_per_pelli': forms.NumberInput(attrs={'class': 'form-control text-end'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
        }
        labels = {
            'fk_articolo': 'Articolo',
            'numero_ricetta': 'Numero Ricetta',
            'data_ricetta': 'Data Ricetta',
            'numero_revisione': 'Numero Revisione',
            'data_revisione': 'Data Revisione',
            'ricetta_per_pelli': 'Ricetta per n. pelli',
            'note': 'Note'

        }
        
# class RicettaRifinizioneModelForm(forms.ModelForm):
#     class Meta:
#         model = RicettaRifinizione
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(RicettaRifinizioneModelForm, self).__init__(*args, **kwargs)       
#         self.fields['numero_ricetta'].widget.attrs['readonly'] = True
#         self.fields['numero_revisione'].widget.attrs['readonly'] = True
            
#         # Nascondi i campi "created_by" se sono già impostati
#         if self.instance.created_by:
#             self.fields['created_by'].widget = forms.HiddenInput()

    # def clean(self):
    #     cleaned_data = super(RicettaRifinizioneModelForm, self).clean()
        
    #     # Imposta numero_ricetta solo se stai creando un nuovo record
    #     if not self.instance.pk:
    #         max_numero_ricetta = RicettaRifinizione.objects.aggregate(Max('numero_ricetta'))['numero_ricetta__max']
    #         cleaned_data['numero_ricetta'] = max_numero_ricetta + 1 if max_numero_ricetta else 1
    #         cleaned_data['numero_revisione'] = 1

    #     return cleaned_data
