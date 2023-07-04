from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db.models import Sum, Count, Q
import datetime
from datetime import date, timedelta, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import (Attrezzatura, ManutenzioneStraordinaria,
                    ManutenzioneOrdinaria, Taratura
                    )
from .forms import AttrezzaturaModelForm, ManutenzioneOrdinariaModelForm, ManutenzioneStraordinariaModelForm, TaraturaModelForm
from .filters import AttrezzaturaFilter
from core.utils import get_records_with_upcoming_expiry
from human_resources.models import Ward



def dashboard_manutenzioni(request):
    attrezzature = Attrezzatura.objects.filter(is_dismesso=False)
    filter = AttrezzaturaFilter(request.GET, queryset=Attrezzatura.objects.all())
    manutenzioni_ordinarie = ManutenzioneOrdinaria.objects.all()
    manutenzioni_straordinarie = ManutenzioneStraordinaria.objects.all()
    tarature = Taratura.objects.all()
    fk_ward_records = Ward.objects.all()
    
    # Aggiungi manualmente l'opzione "tutti" all'inizio dell'elenco
    fk_ward_records = [('tutti', 'Tutti')] + [(ward.pk, ward.description) for ward in fk_ward_records]
    for ward in fk_ward_records:
        print(str(ward[0]) + ' ' + str(ward[1]))

    filterset_class = AttrezzaturaFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(attrezzature, 50)
    
    try:
        attrezzature_home = paginator.page(page)
    except PageNotAnInteger:
        attrezzature_home = paginator.page(1)
    except EmptyPage:
        attrezzature_home = paginator.page(paginator.num_pages)
    context={
        'attrezzature_home': attrezzature_home,
        'filter': filter,
        'manutenzioni_ordinarie': manutenzioni_ordinarie,
        'manutenzioni_straordinarie': manutenzioni_straordinarie,
        'tarature': tarature,
        'fk_ward_records': fk_ward_records,
    }
    return render(request, "manutenzioni/dashboard_manutenzioni.html", context)


def scadenzario(request):
    today = timezone.now().date()
    
    manutenzioni_ordinarie = ManutenzioneOrdinaria.objects.filter(Q(prossima_scadenza__gte=today)).order_by('prossima_scadenza')
    tarature = Taratura.objects.filter(Q(prossima_scadenza__gte=today)).order_by('prossima_scadenza')
    # nella prossima tupla mettiamo le scadenze e le dividiamo per quelle in scadenza entro 30 giorni e quelle successive
    # per dare un colore diverso nello scadenzario
    piano_tarature = []
    piano_manutenzioni = []
    for taratura in tarature:
        if taratura.prossima_scadenza < today + timedelta(days=30):
            piano_tarature.append((taratura, True))
            
        else:
            piano_tarature.append((taratura, False))

    for manutenzione in manutenzioni_ordinarie:
        if manutenzione.prossima_scadenza < today + timedelta(days=30):
            piano_manutenzioni.append((manutenzione, True))
            
            
        else:
            piano_manutenzioni.append((manutenzione, False))

    

    context = {
        'piano_tarature': piano_tarature,
        'piano_manutenzioni': piano_manutenzioni
    }

    return render(request, "manutenzioni/scadenzario.html", context)


class AttrezzaturaCreateView(LoginRequiredMixin,CreateView):
    model = Attrezzatura
    form_class = AttrezzaturaModelForm
    template_name = 'manutenzioni/attrezzatura.html'
    success_message = 'Attrezzatura aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):     
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('manutenzioni:dashboard_manutenzioni')
        
        pk_attrezzatura=self.object.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':pk_attrezzatura})   
        
        
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class AttrezzaturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Attrezzatura
    form_class = AttrezzaturaModelForm
    template_name = 'manutenzioni/attrezzatura.html'
    success_message = 'Attrezzatura modificata correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):          
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('manutenzioni:dashboard_manutenzioni')
        
        pk_attrezzatura=self.object.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':pk_attrezzatura})   
        
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk_attrezzatura = self.object.pk        
        context['elenco_man_straord'] = ManutenzioneStraordinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        context['elenco_tarature'] = Taratura.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        context['elenco_man_ord'] = ManutenzioneOrdinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 

        return context



def delete_attrezzatura(request, pk): 
        deleteobject = get_object_or_404(Attrezzatura, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('manutenzioni:dashboard_manutenzioni')
        return redirect(url_match)


# Manutenzione Ordinaria

class ManutenzioneOrdinariaCreateView(LoginRequiredMixin,CreateView):
    model = ManutenzioneOrdinaria
    form_class = ManutenzioneOrdinariaModelForm
    template_name = 'manutenzioni/manutenzione_ordinaria.html'
    success_message = 'Manutenzione ordinaria aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        fk_attrezzatura = self.object.fk_attrezzatura.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        for key, value in self.kwargs.items():
            print(f"Chiave: {key}, Valore: {value}")
        fk_attrezzatura = self.kwargs["fk_attrezzatura"]
        created_by = self.request.user
        return {
            'created_by': created_by,
            'fk_attrezzatura': fk_attrezzatura
        }

class ManutenzioneOrdinariaUpdateView(LoginRequiredMixin, UpdateView):
    model = ManutenzioneOrdinaria
    form_class = ManutenzioneOrdinariaModelForm
    template_name = 'manutenzioni/manutenzione_ordinaria.html'
    success_message = 'Manutenzione modificata correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):        
        fk_attrezzatura = self.object.fk_attrezzatura.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        #pk_attrezzatura = self.object.pk        
        #context['elenco_man_straord'] = ManutenzioneStraordinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        #context['elenco_tarature'] = Taratura.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        #context['elenco_man_ord'] = ManutenzioneOrdinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 

        return context



def delete_manutenzione_ordinaria(request, pk): 
        deleteobject = get_object_or_404(ManutenzioneOrdinaria, pk = pk)                 
        fk_attrezzatura = deleteobject.fk_attrezzatura.pk
        deleteobject.delete()
        url_match = reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
        return redirect(url_match)


# Manutenzione Straordinaria

class ManutenzioneStraordinariaCreateView(LoginRequiredMixin,CreateView):
    model = ManutenzioneStraordinaria
    form_class = ManutenzioneStraordinariaModelForm
    template_name = 'manutenzioni/manutenzione_straordinaria.html'
    success_message = 'Manutenzione ordinaria aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        fk_attrezzatura = self.object.fk_attrezzatura.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        for key, value in self.kwargs.items():
            print(f"Chiave: {key}, Valore: {value}")
        fk_attrezzatura = self.kwargs["fk_attrezzatura"]
        created_by = self.request.user
        return {
            'created_by': created_by,
            'fk_attrezzatura': fk_attrezzatura
        }

class ManutenzioneStraordinariaUpdateView(LoginRequiredMixin, UpdateView):
    model = ManutenzioneStraordinaria
    form_class = ManutenzioneStraordinariaModelForm
    template_name = 'manutenzioni/manutenzione_straordinaria.html'
    success_message = 'Manutenzione modificata correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):        
        fk_attrezzatura = self.object.fk_attrezzatura.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        #pk_attrezzatura = self.object.pk        
        #context['elenco_man_straord'] = ManutenzioneStraordinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        #context['elenco_tarature'] = Taratura.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        #context['elenco_man_ord'] = ManutenzioneOrdinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 

        return context



def delete_manutenzione_straordinaria(request, pk): 
        deleteobject = get_object_or_404(ManutenzioneStraordinaria, pk = pk)                 
        fk_attrezzatura = deleteobject.fk_attrezzatura.pk
        deleteobject.delete()
        url_match = reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
        return redirect(url_match)


# Taratura

class TaraturaCreateView(LoginRequiredMixin,CreateView):
    model = Taratura
    form_class = TaraturaModelForm
    template_name = 'manutenzioni/taratura.html'
    success_message = 'Manutenzione ordinaria aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        fk_attrezzatura = self.object.fk_attrezzatura.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):        
        fk_attrezzatura = self.kwargs["fk_attrezzatura"]
        created_by = self.request.user
        return {
            'created_by': created_by,
            'fk_attrezzatura': fk_attrezzatura
        }

class TaraturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Taratura
    form_class = TaraturaModelForm
    template_name = 'manutenzioni/taratura.html'
    success_message = 'Manutenzione modificata correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):        
        fk_attrezzatura = self.object.fk_attrezzatura.pk
        return reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        #pk_attrezzatura = self.object.pk        
        #context['elenco_man_straord'] = ManutenzioneStraordinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        #context['elenco_tarature'] = Taratura.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        #context['elenco_man_ord'] = ManutenzioneOrdinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 

        return context



def delete_taratura(request, pk): 
        deleteobject = get_object_or_404(Taratura, pk = pk)                 
        fk_attrezzatura = deleteobject.fk_attrezzatura.pk
        deleteobject.delete()
        url_match = reverse_lazy('manutenzioni:modifica_attrezzatura', kwargs={'pk':fk_attrezzatura})
        return redirect(url_match)

# Stampe
def piano_tarature(request):
    
    if request.method == 'GET':
        
        data_inizio = request.GET.get('data_inizio')  # Assumi che il campo del modal si chiami 'data_inizio'
        data_fine = request.GET.get('data_fine')  # Assumi che il campo del modal si chiami 'data_fine'
        fk_ward_id = request.GET.get('fk_ward_id')  # Assumi che l'ID del campo 'fk_ward' selezionato nel modal venga passato come parametro 'fk_ward_id'
        
        # Effettua il parsing delle date in oggetti datetime
        data_inizio = datetime.strptime(data_inizio, '%Y-%m-%d').date()
        data_fine = datetime.strptime(data_fine, '%Y-%m-%d').date()
    
        # Esegui la query per ottenere i record di Taratura filtrati per intervallo di date e fk_ward
        if fk_ward_id == 'tutti':
            tarature = Taratura.objects.filter(
                prossima_scadenza__range=(data_inizio, data_fine)
            ).order_by('-prossima_scadenza')
        else:
            tarature = Taratura.objects.filter(
                prossima_scadenza__range=(data_inizio, data_fine),
                fk_attrezzatura__fk_ward=fk_ward_id
            ).order_by('-prossima_scadenza')
        
        print("request: " + str(request))
        
        context = {
            'tarature': tarature,
            
        }
        
    return render(request, 'manutenzioni/reports/piano_tarature.html', context)
    
    