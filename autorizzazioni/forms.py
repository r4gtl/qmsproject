from django import forms

from .models import (Autorizzazione, 
                    DettaglioScadenzaAutorizzazione,
                    ParametroAutorizzazione, CampoApplicazione, DettaglioCampoApplicazione
                )


class AutorizzazioneModelForm(forms.ModelForm):
    class Meta:
        model = Autorizzazione
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione'}),
            'rilasciata_da': forms.TextInput(attrs={'placeholder': 'Ente/fornitore che rilascia l\'autorizzazione'}),
            'n_autorizzazione': forms.TextInput(attrs={'placeholder': 'Numero/Identificativo autorizzazione (protocollo, numero,...)'}),
            'data_autorizzazione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'frequenza_scadenza': forms.TextInput(attrs={'placeholder': 'Frequenza scadenza autorizzazione (annuale, biennale,...)'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'FInalità e campo di applicazione',
            'rilasciata_da': 'Rilasciata da',
            'n_autorizzazione': 'Identificativo autorizzazione',
            'data_autorizzazione': 'Data Primo rilascio Autorizzazione',
            'frequenza_scadenza': 'Frequenza Scadenza',
            'note': 'Annotazioni'

            
        }

class DettaglioScadenzaAutorizzazioneModelForm(forms.ModelForm):

    fk_autorizzazione = forms.ModelChoiceField(queryset=Autorizzazione.objects.all())

    class Meta:
        model = DettaglioScadenzaAutorizzazione
        fields = '__all__'
        
        
        widgets = {
            'n_rinnovo': forms.TextInput(attrs={'placeholder': 'Inserisci identificativo rinnovo (protocollo, numero,...)'}),            
            'data_rinnovo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'scadenza_rinnovo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            #'fk_autorizzazione': forms.ChoiceField()
        }
        labels = {
            'n_rinnovo': 'Numero Rinnovo',
            'data_rinnovo': 'Data Rinnovo',            
            'scadenza_rinnovo': 'Scadenza Rinnovo',
            'is_rinnovata': 'Rinnovata',
            'documento': 'Documento',
            'note': 'Annotazioni'
        }


class ParametroAutorizzazioneModelForm(forms.ModelForm):   

    class Meta:
        model = ParametroAutorizzazione
        fields = '__all__'
        
        
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci parametro'}),                        
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            
        }
        labels = {
            'descrizione': 'Descrizione',            
            'note': 'Annotazioni'
        }



class CampoApplicazioneModelForm(forms.ModelForm):
    fk_autorizzazione = forms.ModelChoiceField(queryset=Autorizzazione.objects.all(), required=False, empty_label='Seleziona Autorizzazione', label='Autorizzazione riferimento')

    class Meta:
        model = CampoApplicazione
        fields = '__all__'
        
        

        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Campo di applicazione (Scarichi idrici, Emissioni in Atmosfera...)'}),                        
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            
        }
        labels = {
            'fk_autorizzazione': 'Autorizzazione riferimento',
            'descrizione': 'Descrizione',            
            'is_applicabile': 'Applicabile',            
            'note': 'Annotazioni'
        }

class DettaglioCampoApplicazioneModelForm(forms.ModelForm):

    fk_parametro = forms.ModelChoiceField(queryset=ParametroAutorizzazione.objects.all())
    #fk_campoapplicazione = forms.ModelChoiceField(queryset=CampoApplicazione.objects.all())

    class Meta:
        model = DettaglioCampoApplicazione
        fields = '__all__'
        widgets = {
            #'fk_parametro': forms.ChoiceField(),            
            'um': forms.TextInput(),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            'fk_campoapplicazione': forms.HiddenInput()
        }
        labels = {
            'fk_parametro': 'Parametro',  
            'um': 'Unità di Misura',   
            'limite': 'Limite',
            'note': 'Annotazioni'
        }