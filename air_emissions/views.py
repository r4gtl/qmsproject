from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import *
from .models import *

# Create your views here.
 
def dashboard_emissions(request):
    
    camini = PuntoEmissione.objects.all()
    tot_camini = PuntoEmissione.objects.count()
    

    
    
    context = {
        # Sostanze
        'camini': camini,        
        'tot_camini': tot_camini,
        
    }

    return render(request, 'air_emissions/dashboard_emissions.html', context)


# Camini

class PuntoEmissioneCreateView(LoginRequiredMixin,CreateView):
    model = PuntoEmissione
    form_class = PuntoEmissioneModelForm
    template_name = 'air_emissions/punto_emissione.html'
    success_message = 'Punto Emissione aggiunto correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('air_emissions:dashboard_emissions')

        pk_punto_emissione=self.object.pk
        return reverse_lazy('air_emissions:modifica_punto_emissione', kwargs={'pk':pk_punto_emissione})



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class PuntoEmissioneUpdateView(LoginRequiredMixin, UpdateView):
    model = PuntoEmissione
    form_class = PuntoEmissioneModelForm
    template_name = 'air_emissions/punto_emissione.html'
    success_message = 'Punto Emissione modificato correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('air_emissions:dashboard_emissions')

        pk_punto_emissione=self.object.pk
        return reverse_lazy('air_emissions:modifica_punto_emissione', kwargs={'pk':pk_punto_emissione})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_punto_emissione = self.object.pk
        context['elenco_analisi'] = RegistroControlloAnalitico.objects.filter(fk_punto_emissione=pk_punto_emissione).order_by('-data_prelievo')
        #context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        #context['elenco_schede_sicurezza'] = SchedaSicurezza.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_punto_emissione(request, pk):
        deleteobject = get_object_or_404(PuntoEmissione, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('air_emissions:dashboard_emissions')
        return redirect(url_match)



# Registro Analisi

class RegistroControlloAnaliticoCreateView(LoginRequiredMixin,CreateView):
    model = RegistroControlloAnalitico
    form_class = RegistroControlloAnaliticoModelForm
    template_name = 'air_emissions/registro_analisi.html'
    success_message = 'Registro aggiunto correttamente!'
    

    def get_success_url(self):        
        fk_punto_emissione = self.object.fk_punto_emissione.pk
        return reverse_lazy('air_emissions:modifica_punto_emissione', kwargs={'pk':fk_punto_emissione})
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def form_invalid(self, form):
        # Il form non è valido, puoi accedere agli errori
        print("Campi obbligatori mancanti:")
        for field_name, errors in form.errors.items():
            print(f"{field_name}: {', '.join(errors)}")
        # O mostrali all'utente o registrali in un file di log
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_initial(self):        
        fk_punto_emissione = self.kwargs["fk_punto_emissione"]
        created_by = self.request.user
        
        
        return {
            'created_by': created_by,
            'fk_punto_emissione': fk_punto_emissione,
            #'fk_human_resources': attrezzatura.fk_human_resource
        }
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        fk_punto_emissione = self.kwargs["fk_punto_emissione"]
        punto_emissione = PuntoEmissione.objects.get(pk=fk_punto_emissione)
        kwargs['initial']['fk_punto_emissione'] = fk_punto_emissione
        return kwargs

class RegistroControlloAnaliticoUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistroControlloAnalitico
    form_class = RegistroControlloAnaliticoModelForm
    template_name = 'air_emissions/registro_analisi.html'
    success_message = 'Registro modificato correttamente!'
    
    
    def get_success_url(self):        
        fk_punto_emissione = self.object.fk_punto_emissione.pk
        return reverse_lazy('air_emissions:modifica_punto_emissione', kwargs={'pk':fk_punto_emissione})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_punto_emissione = self.kwargs["fk_punto_emissione"]   
        print(f"fk_punto_emissione: {fk_punto_emissione}")
        context['punto_emissione'] = PuntoEmissione.objects.get(pk=fk_punto_emissione)
        #context['elenco_tarature'] = Taratura.objects.filter(fk_attrezzatura=pk_attrezzatura) 
        #context['elenco_man_ord'] = ManutenzioneOrdinaria.objects.filter(fk_attrezzatura=pk_attrezzatura) 

        return context



def delete_registro_analisi(request, pk): 
        deleteobject = get_object_or_404(RegistroControlloAnalitico, pk = pk)                 
        fk_punto_emissione = deleteobject.fk_punto_emissione.pk
        deleteobject.delete()
        url_match = reverse_lazy('air_emissions:modifica_punto_emissione', kwargs={'pk':fk_punto_emissione})
        return redirect(url_match)

def registro_controlli_analitici(request):
    elenco_analisi=RegistroControlloAnalitico.objects.order_by('-data_prelievo')
    context = {
        # Sostanze
        'elenco_analisi': elenco_analisi
        
        
    }

    return render(request, 'air_emissions/reports/registro_controlli_analitici.html', context)