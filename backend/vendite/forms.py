from anagrafiche.models import Cliente
from django import forms
from django.db.models import Sum

from .models import (DettaglioOrdineCliente, OrdineCliente, SchedaLavorazione,
                     XRScelteSchede)


class OrdineClienteModelForm(forms.ModelForm):
    class Meta:
        model = OrdineCliente
        fields = '__all__'


        widgets = {
            'numero_ordine': forms.TextInput(attrs={'placeholder': 'Inserisci Numero ordine riferimento'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        
class DettaglioOrdineClienteModelForm(forms.ModelForm):
    class Meta:
        model = DettaglioOrdineCliente
        fields = '__all__'

        widgets = {
            'riferimento': forms.TextInput(attrs={'placeholder': 'Inserisci riferimento del cliente'}),    
            'fk_articolo': forms.Select(attrs={'class': 'form-select select-articolo'}),
            'fk_colore': forms.Select(attrs={'class': 'form-select select-colore'}),
            'um': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'class': 'form-control'}),    
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),  
            'fk_ordine': forms.HiddenInput()  
        }

class SchedaLavorazioneModelForm(forms.ModelForm):
    class Meta:
        model = SchedaLavorazione
        fields = '__all__'

        widgets = {
            'fk_dettaglio_ordine_cliente': forms.Select(attrs={'class': 'form-select select-dettaglioordinecliente'}),    
            'fk_articolo': forms.Select(attrs={'class': 'form-select select-articolo'}),
            'fk_colore': forms.Select(attrs={'class': 'form-select select-colore'}),            
            'tot_pelli': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'class': 'form-control'}),    
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),  
            
        }


class XRScelteSchedeModelForm(forms.ModelForm):
    class Meta:
        model = XRScelteSchede
        fields = ['fk_sceltalotto', 'fk_schedalavorazione', 'quantity', 'note']
        widgets = {
            'fk_sceltalotto': forms.HiddenInput(),
            'fk_schedalavorazione': forms.HiddenInput(),
            'note': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        scelta = self.cleaned_data['fk_sceltalotto']

        used = scelta.xrscelteschede.aggregate(tot=Sum('quantity'))['tot'] or 0
        available = scelta.pezzi - used

        if qty > available:
            raise forms.ValidationError(f"La quantità inserita supera quella disponibile ({available}).")
        return qty