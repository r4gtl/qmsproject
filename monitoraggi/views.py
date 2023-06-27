from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView



from .models import (
                    MonitoraggioAcqua, MonitoraggioGas, MonitoraggioEnergiaElettrica, DatoProduzione
)
from .forms import (
                    MonitoraggioAcquaModelForm, MonitoraggioGasModelForm, MonitoraggioEnergiaElettricaModelForm, DatoProduzioneModelForm
)
# Create your views here.

def dashboard_monitoraggi(request):
    
    consumi_acqua = MonitoraggioAcqua.objects.all()
    consumi_gas = MonitoraggioGas.objects.all()
    consumi_energia_elettrica = MonitoraggioEnergiaElettrica.objects.all()
    dati_produzione = DatoProduzione.objects.all()
    mq_last_year=DatoProduzione.somma_produzione_ultimo_anno('mq')
    n_pelli_last_year=DatoProduzione.somma_produzione_ultimo_anno('n_pelli')
    energia_elettrica_last_year = MonitoraggioEnergiaElettrica.somma_energia_ultimo_anno()
    gas_last_year = MonitoraggioGas.somma_gas_ultimo_anno()
    if mq_last_year==0:
        kwh_mq_mj = 0
        mc_mq_mj = 0
    else:
        kwh_mq_mj = (float(energia_elettrica_last_year) / float(mq_last_year))*3.6
        mc_mq_mj = (float(gas_last_year) / float(mq_last_year))*38.4
        

    context = {
        'consumi_acqua': consumi_acqua,
        'consumi_gas': consumi_gas,
        'consumi_energia_elettrica': consumi_energia_elettrica,
        'dati_produzione': dati_produzione,
        'mq_last_year': mq_last_year,
        'n_pelli_last_year': n_pelli_last_year,
        'kwh_mq_mj': kwh_mq_mj,
        'mc_mq_mj': mc_mq_mj
    }
    return render(request, "monitoraggi/dashboard_monitoraggi.html", context)


# Acqua

class MonitoraggioAcquaCreateView(LoginRequiredMixin,CreateView):
    model = MonitoraggioAcqua
    form_class = MonitoraggioAcquaModelForm
    template_name = 'monitoraggi/monitoraggio_acqua.html'
    success_message = 'Monitoraggio aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class MonitoraggioAcquaUpdateView(LoginRequiredMixin, UpdateView):
    model = MonitoraggioAcqua
    form_class = MonitoraggioAcquaModelForm
    template_name = 'monitoraggi/monitoraggio_acqua.html'
    success_message = 'Monitoraggio modificato correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):        
        
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_monitoraggio_acqua(request, pk): 
        deleteobject = get_object_or_404(MonitoraggioAcqua, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('monitoraggi:dashboard_monitoraggi')
        return redirect(url_match)

# Gas
class MonitoraggioGasCreateView(LoginRequiredMixin,CreateView):
    model = MonitoraggioGas
    form_class = MonitoraggioGasModelForm
    template_name = 'monitoraggi/monitoraggio_gas.html'
    success_message = 'Monitoraggio aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class MonitoraggioGasUpdateView(LoginRequiredMixin, UpdateView):
    model = MonitoraggioGas
    form_class = MonitoraggioGasModelForm
    template_name = 'monitoraggi/monitoraggio_gas.html'
    success_message = 'Monitoraggio modificato correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):        
        
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_monitoraggio_gas(request, pk): 
        deleteobject = get_object_or_404(MonitoraggioGas, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('monitoraggi:dashboard_monitoraggi')
        return redirect(url_match)


# Energia Elettrica
class MonitoraggioEnergiaElettricaCreateView(LoginRequiredMixin,CreateView):
    model = MonitoraggioEnergiaElettrica
    form_class = MonitoraggioEnergiaElettricaModelForm
    template_name = 'monitoraggi/monitoraggio_energia_elettrica.html'
    success_message = 'Monitoraggio aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class MonitoraggioEnergiaElettricaUpdateView(LoginRequiredMixin, UpdateView):
    model = MonitoraggioEnergiaElettrica
    form_class = MonitoraggioEnergiaElettricaModelForm
    template_name = 'monitoraggi/monitoraggio_energia_elettrica.html'
    success_message = 'Monitoraggio modificato correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):        
        
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_monitoraggio_energia_elettrica(request, pk): 
        deleteobject = get_object_or_404(MonitoraggioEnergiaElettrica, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('monitoraggi:dashboard_monitoraggi')
        return redirect(url_match)

# Dati Produzione

class DatoProduzioneCreateView(LoginRequiredMixin,CreateView):
    model = DatoProduzione
    form_class = DatoProduzioneModelForm
    template_name = 'monitoraggi/dato_produzione.html'
    success_message = 'Dato produzione aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class DatoProduzioneUpdateView(LoginRequiredMixin, UpdateView):
    model = DatoProduzione
    form_class = DatoProduzioneModelForm
    template_name = 'monitoraggi/dato_produzione.html'
    success_message = 'Dato produzione modificato correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self): 
        return reverse_lazy('monitoraggi:dashboard_monitoraggi')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_lettura_dato_produzione(request, pk): 
        deleteobject = get_object_or_404(DatoProduzione, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('monitoraggi:dashboard_monitoraggi')
        return redirect(url_match)