from django import forms


from .models import ProdottoChimico, PrezzoProdotto, SchedaTecnica
from anagrafiche.models import Fornitore


class ProdottoChimicoModelForm(forms.ModelForm):
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
        

class PrezzoProdottoModelForm(forms.ModelForm):
    
    
    class Meta:
        model = PrezzoProdotto
        fields= '__all__'
        widgets = {
            'data_inserimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'prezzo': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'fk_prodottochimico': forms.HiddenInput()
        }
        labels = {
            'data_inserimento': 'Data Inserimento',
            'prezzo': 'Prezzo',            
            'note': 'Note'

        }
        

class SchedaTecnicaModelForm(forms.ModelForm):
    
    
    class Meta:
        model = SchedaTecnica
        fields= '__all__'
        widgets = {
            'data_inserimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'fk_prodottochimico': forms.HiddenInput()
        }
        labels = {
            'data_inserimento': 'Data Inserimento',
            'documento': 'Documento',
            'note': 'Note'

        }