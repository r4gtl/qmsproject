from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages


from .models import Autorizzazione, DettaglioScadenzaAutorizzazione
from .filters import AutorizzazioneFilter
from .forms import AutorizzazioneModelForm, DettaglioScadenzaAutorizzazioneModelForm
# Create your views here.

def autorizzazioni_home(request):
    autorizzazioni = Autorizzazione.objects.all()
    autorizzazione_filter = AutorizzazioneFilter(request.GET, queryset=Autorizzazione.objects.all())
    page = request.GET.get('page', 1)
    paginator = Paginator(autorizzazioni, 50)
    
    try:
        autorizzazioni_home = paginator.page(page)
    except PageNotAnInteger:
        autorizzazioni_home = paginator.page(1)
    except EmptyPage:
        autorizzazioni_home = paginator.page(paginator.num_pages)
    context={
        'autorizzazioni_home': autorizzazioni_home,
        'filter': autorizzazione_filter,
        
    }
    return render(request, "autorizzazioni/autorizzazioni_home.html", context)


class AutorizzazioneCreateView(LoginRequiredMixin,CreateView):
    model = Autorizzazione
    form_class = AutorizzazioneModelForm
    template_name = 'autorizzazioni/autorizzazione.html'
    success_message = 'Autorizzazione aggiunta correttamente!'
    

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('autorizzazioni:autorizzazioni_home')
        
        pk_autorizzazione=self.object.pk
        return reverse_lazy('autorizzazioni:modifica_autorizzazione', kwargs={'pk':pk_autorizzazione})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class AutorizzazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = Autorizzazione
    form_class = AutorizzazioneModelForm
    template_name = 'autorizzazioni/autorizzazione.html'
    success_message = 'Autorizzazione modificata correttamente!'
        
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('autorizzazioni:autorizzazioni_home')
        
        pk_autorizzazione=self.object.pk
        return reverse_lazy('autorizzazioni:modifica_autorizzazione', kwargs={'pk':pk_autorizzazione})
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk_autorizzazione = self.object.pk        
        context['elenco_dettaglio_scadenze'] = DettaglioScadenzaAutorizzazione.objects.filter(fk_autorizzazione=pk_autorizzazione)          

        return context



def delete_autorizzazione(request, pk): 
        deleteobject = get_object_or_404(Autorizzazione, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('autorizzazioni:autorizzazioni_home')
        return redirect(url_match)


class DettaglioScadenzaAutorizzazioneCreateView(LoginRequiredMixin,CreateView):
    model = DettaglioScadenzaAutorizzazione
    form_class = DettaglioScadenzaAutorizzazioneModelForm
    template_name = 'autorizzazioni/dettaglio_autorizzazione.html'
    success_message = 'Dettaglio aggiunto correttamente!'
    

    def get_success_url(self):   
        fk_autorizzazione=self.object.fk_autorizzazione.pk
        return reverse_lazy('autorizzazioni:modifica_autorizzazione', kwargs={'pk':fk_autorizzazione})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_autorizzazione = self.kwargs['fk_autorizzazione']

        return {
            'created_by': created_by,
            'fk_autorizzazione': fk_autorizzazione
        }

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_autorizzazione']       
        context['fk_autorizzazione'] = Autorizzazione.objects.get(pk=pk) 
        return context

class DettaglioScadenzaAutorizzazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioScadenzaAutorizzazione
    form_class = DettaglioScadenzaAutorizzazioneModelForm
    template_name = 'autorizzazioni/dettaglio_autorizzazione.html'
    success_message = 'Dettaglio modificato correttamente!'
    
    
    def get_success_url(self):              
        fk_autorizzazione=self.object.fk_autorizzazione.pk        
        return reverse_lazy('autorizzazioni:modifica_autorizzazione', kwargs={'pk':fk_autorizzazione})
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk_autorizzazione = self.kwargs['fk_autorizzazione'] 
        pk_revisione = self.kwargs['pk']       
        context['fk_autorizzazione'] = Autorizzazione.objects.get(pk=pk_autorizzazione)
        return context



def delete_dettaglio_autorizzazione(request, pk): 
        deleteobject = get_object_or_404(DettaglioScadenzaAutorizzazione, pk = pk) 
        fk_autorizzazione = deleteobject.fk_autorizzazione.pk                
        deleteobject.delete()
        url_match = reverse_lazy('autorizzazioni:modifica_autorizzazione', kwargs={'pk':fk_autorizzazione,})
        return redirect(url_match)


# Stampe

def get_prossima_scadenza(autorizzazione):
    prossima_scadenza = autorizzazione.dettaglioscadenzaautorizzazione_set.order_by('-data_rinnovo').first()
    if prossima_scadenza:
        return prossima_scadenza.data_rinnovo
    return '-'


def stampa_registro_autorizzazioni(request):
    autorizzazioni_query = Autorizzazione.objects.all()
    #max_data_rinnovo = RevisioneProcedura.objects.aggregate(Max('data_revisione'))['data_revisione__max']
    
    context = {
        'autorizzazioni_query': autorizzazioni_query,
        'get_prossima_scadenza': get_prossima_scadenza,
        #'max_data_revisione': max_data_revisione
        
    }
    return render(request, "autorizzazioni/reports/stampa_registro_autorizzazioni.html", context)