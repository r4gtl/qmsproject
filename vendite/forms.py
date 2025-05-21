from anagrafiche.models import Cliente
from django import forms

from .models import DettaglioOrdineCliente, OrdineCliente


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