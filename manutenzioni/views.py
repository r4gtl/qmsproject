from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Sum, Count
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import (Attrezzatura, ManutenzioneStraordinaria,
                    ManutenzioneOrdinaria, Taratura
                    )
from .forms import AttrezzaturaModelForm, ManutenzioneOrdinariaModelForm, ManutenzioneOrdinariaModelForm, TaraturaModelForm
from .filters import AttrezzaturaFilter



def dashboard_manutenzioni(request):
    attrezzature = Attrezzatura.objects.all()
    manutenzioni_ordinarie = ManutenzioneOrdinaria.objects.all()
    manutenzioni_straordinarie = ManutenzioneStraordinaria.objects.all()
    tarature = Taratura.objects.all()
    attrezzature_filter = AttrezzaturaFilter
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
        'filter': attrezzature_filter,
        'manutenzioni_ordinarie': manutenzioni_ordinarie,
        'manutenzioni_straordinarie': manutenzioni_straordinarie,
        'tarature': tarature
    }
    return render(request, "manutenzioni/dashboard_manutenzioni.html", context)



class AttrezzaturaCreateView(LoginRequiredMixin,CreateView):
    model = Attrezzatura
    form_class = AttrezzaturaModelForm
    template_name = 'manutenzioni/attrezzatura.html'
    success_message = 'Attrezzatura aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        
        return reverse_lazy('manutenzioni:dashboard_manutenzioni')
        
    
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
        
        return reverse_lazy('manutenzioni:dashboard_manutenzioni')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_attrezzatura(request, pk): 
        deleteobject = get_object_or_404(Attrezzatura, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('manutenzioni:dashboard_manutenzioni')
        return redirect(url_match)