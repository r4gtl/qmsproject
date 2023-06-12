from django import forms
from .models import (Procedura, SezioneLWG, RevisioneProcedura, Modulo, RevisioneModulo
                     )




class ProceduraModelForm(forms.ModelForm):
    class Meta:
        model = Procedura
        fields = '__all__'
        fk_lwgsection = forms.ModelChoiceField(queryset=SezioneLWG.objects.all())

        widget = {
            'identificativo': forms.TextInput(attrs={'placeholder': 'Inserisci identificativo procedura'}),            
            'data_procedura': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci breve Descrizione/Titolo'}),   
            'is_eliminata' : forms.CheckboxInput(),
            'fk_lwgsection': forms.ChoiceField(),     
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'identificativo': 'Identificativo',
            'data_procedura': 'Data Procedura',
            'descrizione': 'Titolo/Descrizione',
            'is_eliminata': 'Eliminata',
            'fk_lwgsection': 'Sezione LWG',            
            'note': 'Annotazioni'
        }


class RevisioneProceduraModelForm(forms.ModelForm):
    class Meta:
        model = RevisioneProcedura
        fields = '__all__'
        
        fk_procedura = forms.ModelChoiceField(queryset=Procedura.objects.all())
        widget = {
            'n_revisione': forms.TextInput(attrs={'placeholder': 'Inserisci identificativo procedura'}),            
            'data_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            'fk_procedura': forms.HiddenInput()
        }
        labels = {
            'n_revisione': 'Numero Revisione',
            'data_revisione': 'Data Revisione',            
            'note': 'Annotazioni'
        }

class ModuloModelForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = '__all__'
        

        widget = {
            'identificativo': forms.TextInput(attrs={'placeholder': 'Inserisci identificativo procedura'}),            
            'data_modulo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci breve Descrizione/Titolo'}),                  
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            'fk_procedura': forms.HiddenInput()
        }
        labels = {
            'identificativo': 'Identificativo',
            'data_modulo': 'Data Modulo',
            'descrizione': 'Titolo/Descrizione',
            'note': 'Annotazioni'
        }
        
class RevisioneModuloModelForm(forms.ModelForm):
    class Meta:
        model = RevisioneModulo
        fields = '__all__'
        

        widget = {
            'n_revisione': forms.NumberInput(),            
            'data_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            'fk_modulo': forms.HiddenInput()
        }
        labels = {
            'n_revisione': 'Numero revisione',
            'data_revisione': 'Data Revisione',            
            'note': 'Annotazioni'
        }
