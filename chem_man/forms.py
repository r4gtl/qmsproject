from django import forms


from .models import ProdottoChimico
from anagrafiche.models import Fornitore


class FormProdottoChimico(forms.ModelForm):
    fk_fornitore = forms.ModelChoiceField(
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore'
    )
    
    class Meta:
        model = ProdottoChimico
        fields= '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci il nome del prodotto chimico'}),
            'solvente': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Nome Prodotto',
            'solvente': 'Solvente',
            'reparto': 'Reparto',
            'flame_class': 'classe di Infiammabilità',
            'zdhc_level': 'ZDHC Level',
            'note': 'Note'

        }