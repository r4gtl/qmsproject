from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, DecimalField

from datetime import date, timedelta, datetime


from .models import (CodiceCER, 
                    CodiceSmaltRec, 
                    MovimentoRifiuti,
                    )
from .filters import MovimentoRifiutiFilter

from .forms import (MovimentoRifiutiModelForm,
                    CodiceCERModelForm,
                    CodiceSmaltRecModelForm
                    
                    )


from .utils import somma_quantita_per_anno_smaltimento_recupero

def gestione_rifiuti_home(request): 

    movimenti_rifiuti = MovimentoRifiuti.objects.all()
    
    movimenti_rifiuti_filter = MovimentoRifiutiFilter(request.GET, queryset=movimenti_rifiuti)
    
    current_date = date.today()
    begin_date = current_date - timedelta(days=365)
    
    
    movimenti_recupero = MovimentoRifiuti.objects.filter(Q(**{f"data_movimento__lte": current_date}) & Q(**{f"data_movimento__gte": begin_date})).filter(car_scar="carico").filter(fk_smaltrec__smalt_rec="recupero").aggregate(total=Sum('quantity'))['total']
    movimenti_smaltimento = MovimentoRifiuti.objects.filter(Q(**{f"data_movimento__lte": current_date}) & Q(**{f"data_movimento__gte": begin_date})).filter(car_scar="carico").filter(fk_smaltrec__smalt_rec="smaltimento").aggregate(total=Sum('quantity'))['total']

    
    
    
    
    page = request.GET.get('page', 1)
    paginator = Paginator(movimenti_rifiuti_filter.qs, 50)  # Utilizza lotti_filter.qs per la paginazione
    
        
    try:
        movimenti_rifiuti_paginator = paginator.page(page)
    except PageNotAnInteger:
        movimenti_rifiuti_paginator = paginator.page(1)
    except EmptyPage:
        movimenti_rifiuti_paginator = paginator.page(paginator.num_pages)
        
    context = {
        'dati_paginator': movimenti_rifiuti_paginator,
        'filter': movimenti_rifiuti_filter,
        'movimenti_recupero': movimenti_recupero,
        'movimenti_smaltimento': movimenti_smaltimento,
        
    }
    
    return render(request, 'gestionerifiuti/gestione_rifiuti_home.html', context)




def tabelle_generiche(request):
    codici_cer = CodiceCER.objects.all()
    codici_smaltrec = CodiceSmaltRec.objects.all()

    context = {'codici_cer': codici_cer, 
               'codici_smaltrec': codici_smaltrec,                           
                }
    
    return render(request, "gestionerifiuti/tabelle_generiche.html", context)



class MovimentoRifiutiCreateView(LoginRequiredMixin,CreateView):
    model = MovimentoRifiuti
    form_class = MovimentoRifiutiModelForm
    template_name = 'gestionerifiuti/movimento_rifiuti.html'
    success_message = 'Carico/scarico aggiunto correttamente!'
    

    def get_success_url(self):
        
        return reverse_lazy('gestionerifiuti:gestione_rifiuti_home')
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class MovimentoRifiutiUpdateView(LoginRequiredMixin, UpdateView):
    model = MovimentoRifiuti
    form_class = MovimentoRifiutiModelForm
    template_name = 'gestionerifiuti/movimento_rifiuti.html'
    success_message = 'Carico/scarico modificato correttamente!'
    
    
    def get_success_url(self):        
        
        return reverse_lazy('gestionerifiuti:gestione_rifiuti_home')
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context


def delete_movimento_rifiuti(request, pk): 
        deleteobject = get_object_or_404(MovimentoRifiuti, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('gestionerifiuti:gestione_rifiuti_home')
        return redirect(url_match)
    

# Crea, modifica, cancella Codice CER
class CodiceCERCreateView(LoginRequiredMixin,CreateView):
    model = CodiceCER
    form_class = CodiceCERModelForm
    template_name = 'gestionerifiuti/codice_cer.html'
    success_message = 'Codice CER aggiunto correttamente!'
    

    def get_success_url(self):        
        return reverse_lazy('gestionerifiuti:tabelle_generiche')
    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }



class CodiceCERUpdateView(LoginRequiredMixin, UpdateView):
    model = CodiceCER
    form_class = CodiceCERModelForm
    template_name = 'gestionerifiuti/codice_cer.html'
    success_message = 'Codice CER modificato correttamente!'
    
    
    def get_success_url(self):        
        
        return reverse_lazy('gestionerifiuti:tabelle_generiche')
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context


def delete_codice_cer(request, pk): 
        deleteobject = get_object_or_404(CodiceCER, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('gestionerifiuti:tabelle_generiche')
        return redirect(url_match)
    



# Crea, modifica, cancella Codice Smalt/Rec

class CodiceSmaltRecCreateView(LoginRequiredMixin,CreateView):
    model = CodiceSmaltRec
    form_class = CodiceSmaltRecModelForm
    template_name = 'gestionerifiuti/codice_smaltrec.html'
    success_message = 'Codice Smalt/Rec aggiunto correttamente!'
    

    def get_success_url(self):        
        return reverse_lazy('gestionerifiuti:tabelle_generiche')
    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }
        
        
        
class CodiceSmaltRecUpdateView(LoginRequiredMixin, UpdateView):
    model = CodiceSmaltRec
    form_class = CodiceSmaltRecModelForm
    template_name = 'gestionerifiuti/codice_smaltrec.html'
    success_message = 'Codice Smalt/Rec modificato correttamente!'
    
    
    def get_success_url(self):        
        
        return reverse_lazy('gestionerifiuti:tabelle_generiche')
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context


def delete_codice_smaltrec(request, pk): 
        deleteobject = get_object_or_404(CodiceSmaltRec, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('gestionerifiuti:tabelle_generiche')
        return redirect(url_match)
    
    
# Stampe
def performance_triennio(request):
    risultato_smaltimento = somma_quantita_per_anno_smaltimento_recupero('smaltimento')
    risultato_recupero = somma_quantita_per_anno_smaltimento_recupero('recupero')

    # Trova gli anni dall'unione dei dati di smaltimento e recupero
    anni_smaltimento = set()
    for dati_per_anno in risultato_smaltimento.values():
        anni_smaltimento.update(dati_per_anno.keys())

    anni_recupero = set()
    for dati_per_anno in risultato_recupero.values():
        anni_recupero.update(dati_per_anno.keys())

    anni = sorted(anni_smaltimento.union(anni_recupero))

    dati_tabella_smaltimento = [(tipo_movimento, risultato_smaltimento.get(tipo_movimento, {})) for tipo_movimento in risultato_smaltimento]
    dati_tabella_recupero = [(tipo_movimento, risultato_recupero.get(tipo_movimento, {})) for tipo_movimento in risultato_recupero]

    
    
    
    context = {
        
        'dati_tabella_smaltimento': dati_tabella_smaltimento,
        'dati_tabella_recupero': dati_tabella_recupero,
        'anni': anni,
    }
    
    return render(request, 'gestionerifiuti/reports/performance_triennio.html', context)