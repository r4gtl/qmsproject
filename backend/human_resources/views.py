import datetime
from datetime import timedelta

from core.utils import get_records_with_upcoming_expiry
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Sum
from django.http import FileResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView

from .charts import (get_average_age, get_gender_perc, get_ita_perc,
                     num_tot_dipendenti)
from .filters import HRFilter
from .forms import *
from .models import *
from .report_lab import ChartReport


def generate_chart_report(request):
    report = ChartReport(title="Report con Grafici")
    pdf_buffer = report.generate_pdf()
     # Imposta la risposta HTTP per visualizzare il PDF inline
    response = FileResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="chart_report.pdf"'
    #return FileResponse(pdf_buffer, as_attachment=True, filename="chart_report.pdf", content_type="application/pdf")
    return response

# Create your views here.
def human_resources_home(request):
    hr = HumanResource.objects.all().order_by('cognomedipendente')
    hr_active = HumanResource.objects.filter(datadimissioni__isnull=True).count()
    hr_filter = HRFilter(request.GET, queryset=hr)
    hr_average_age = get_average_age()
    hr_male = get_gender_perc('M')
    hr_female = get_gender_perc('F')
    hr_ita = get_ita_perc()
    page = request.GET.get('page', 1)
    paginator = Paginator(hr, 50)
    
    try:
        human_resources = paginator.page(page)
    except PageNotAnInteger:
        human_resources = paginator.page(1)
    except EmptyPage:
        human_resources = paginator.page(paginator.num_pages)
    context={
        'human_resources': human_resources,
        'filter': hr_filter,
        'hr_active': hr_active,
        'hr_average_age': hr_average_age,
        'hr_male': hr_male,
        'hr_female': hr_female,
        'hr_ita': hr_ita
    }
    return render(request, "human_resources/human_resources_home.html", context)

def scadenzario(request):
    prossime_formazioni = get_records_with_upcoming_expiry(DettaglioRegistroFormazione, "prossima_scadenza", 365)
    

    context = {
        'prossime_formazioni': prossime_formazioni,
        
    }

    return render(request, "human_resources/scadenzario.html", context)





class HumanResourceCreateView(LoginRequiredMixin,CreateView):
    model = HumanResource
    form_class = HumanResourceModelForm
    template_name = 'human_resources/single_operator.html'
    success_message = 'Operatore aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('human_resources:human_resources')
        
        pk_hr=self.object.pk
        return reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)


def add_new_operator(request):    
    context ={}    
    form = HumanResourceModelForm(request.POST or None, request.FILES)
    operatori = HumanResource.objects.all()
    if form.is_valid():
        form.save()
    else:
        messages.error(request, 'Errore!')          
    messages.info(request, 'Operatore aggiunto correttamente!')      
    context['form']= form
    context['operatori']= operatori
    return render(request, "human_resources/single_operator.html", context)



class HRUpdateView(LoginRequiredMixin,UpdateView):
    model = HumanResource
    form_class = HumanResourceModelForm
    template_name = 'human_resources/single_operator.html'
    success_message = 'Operatore modificato correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('human_resources:human_resources')
        
        pk_hr=self.object.pk
        return reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        if self.object.immagine:
            context['immagine'] = self.object.immagine.url
        else:
            context['immagine'] = False
        #context['elenco_formazione'] = DettaglioRegistroFormazione.objects.filter(fk_hr=self.object.pk)
        context['elenco_formazione'] = DettaglioRegistroFormazione.objects.filter(
                                            fk_hr=self.object.pk
                                            ).select_related('fk_registro_formazione').order_by('-fk_registro_formazione__data_formazione')
        context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        context['elenco_incarichi_sicurezza'] = HR_Safety.objects.filter(fk_hr=self.object.pk)
        return context


class ValutazioneOperatoreCreateView(LoginRequiredMixin,CreateView):
    model = ValutazioneOperatore
    form_class = ValutazioneOperatoreModelForm
    template_name = 'human_resources/valutazione_operatore.html'
    success_message = 'Valutazione aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:update_human_resource')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)    
    
    def get_initial(self):        
        fk_hr = self.kwargs['pk']  
        created_by = self.request.user      
        return {
            'fk_hr': fk_hr,
            'created_by': created_by,
            'created_at': datetime.datetime.now()
        }
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_hr = self.kwargs['pk']
        
        context['fk_hr'] = fk_hr  
        context['operatore'] = HumanResource.objects.get(pk=fk_hr)     
        return context    

    def get_success_url(self):        
        pk_hr=self.object.fk_hr.pk
        return reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
    

    
class ValutazioneOperatoreUpdateView(LoginRequiredMixin, UpdateView):
    model = ValutazioneOperatore
    form_class = ValutazioneOperatoreModelForm
    template_name = 'human_resources/valutazione_operatore.html'
    success_message = 'Valutazione modificata correttamente!'
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)    
    
    def get_success_url(self):        
        pk_hr=self.object.fk_hr.pk
        return reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        
        context['fk_hr'] = self.object.fk_hr.pk  
        context['operatore'] = HumanResource.objects.get(pk=self.object.fk_hr.pk)     
        return context

def delete_valutazione_operatore(request, pk): 
        deleteobject = get_object_or_404(ValutazioneOperatore, pk = pk)         
        pk_hr=deleteobject.fk_hr.pk       
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
        return redirect(url_match)  


# XR Incarichi sicurezza-Operatore
class HR_SafetyCreateView(LoginRequiredMixin,CreateView):
    model = HR_Safety
    form_class = HR_SafetyModelForm
    template_name = 'human_resources/safety_role_operatore.html'
    success_message = 'Incarico aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:update_human_resource')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)    
    
    def get_initial(self):        
        fk_hr = self.kwargs['pk']  
        created_by = self.request.user      
        return {
            'fk_hr': fk_hr,
            'created_by': created_by,            
        }
    
    def get_success_url(self):        
        pk_hr=self.object.fk_hr.pk
        return reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_hr = self.kwargs['pk']
        
        context['fk_hr'] = fk_hr  
        context['operatore'] = HumanResource.objects.get(pk=fk_hr)     
        return context
    
class HR_SafetyUpdateView(LoginRequiredMixin, UpdateView):
    model = HR_Safety
    form_class = HR_SafetyModelForm
    template_name = 'human_resources/safety_role_operatore.html'
    success_message = 'Incarico modificato correttamente!'
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)    
    
    def get_success_url(self):        
        pk_hr=self.object.fk_hr.pk
        return reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        
        context['fk_hr'] = self.object.fk_hr.pk  
        context['operatore'] = HumanResource.objects.get(pk=self.object.fk_hr.pk)     
        return context

def delete_hr_safety(request, pk): 
        deleteobject = get_object_or_404(HR_Safety, pk = pk)         
        pk_hr=deleteobject.fk_hr.pk       
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:update_human_resource', kwargs={'pk':pk_hr})
        return redirect(url_match)  


'''SEZIONE TABELLE GENERICHE'''

def tabelle_generiche(request):
    wards = Ward.objects.all()
    roles = Role.objects.all()
    centridilavoro = CentrodiLavoro.objects.all()
    safety_roles = Safety_Role.objects.all()
    

    context = {'wards': wards, 
                'roles': roles,  
                'centridilavoro': centridilavoro,
                'safety_roles': safety_roles              
                }
    
    return render(request, "human_resources/tabelle_generiche_hr.html", context)

# Creazione, Update e Delete Centro di Lavoro
class CentrodiLavoroCreateView(LoginRequiredMixin,CreateView):
    model = CentrodiLavoro
    form_class = CentrodiLavoroModelForm
    template_name = 'human_resources/centro_di_lavoro.html'
    success_message = 'Centro di Lavoro aggiunto correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class CentrodiLavoroUpdateView(LoginRequiredMixin,UpdateView):
    model = CentrodiLavoro
    form_class = CentrodiLavoroModelForm
    template_name = 'human_resources/centro_di_lavoro.html'
    success_message = 'Reparto modificato correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    
def delete_centro_di_lavoro(request, pk): 
        deleteobject = get_object_or_404(CentrodiLavoro, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:tabelle_generiche')
        return redirect(url_match)

# Creazione, Update e Delete Ward
class WardCreateView(LoginRequiredMixin,CreateView):
    model = Ward
    form_class = WardModelForm
    template_name = 'human_resources/ward.html'
    success_message = 'Reparto aggiunto correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class WardUpdateView(LoginRequiredMixin,UpdateView):
    model = Ward
    form_class = WardModelForm
    template_name = 'human_resources/ward.html'
    success_message = 'Reparto modificato correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    
def delete_ward(request, pk): 
        deleteobject = get_object_or_404(Ward, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:tabelle_generiche')
        return redirect(url_match)

# Creazione, Update e Delete Role
class RoleCreateView(LoginRequiredMixin,CreateView):
    model = Role
    form_class = RoleModelForm
    template_name = 'human_resources/role.html'
    success_message = 'Mansione aggiunta correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class RoleUpdateView(LoginRequiredMixin,UpdateView):
    model = Role
    form_class = RoleModelForm
    template_name = 'human_resources/role.html'
    success_message = 'mansione modificata correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    
def delete_role(request, pk): 
        deleteobject = get_object_or_404(Role, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:tabelle_generiche')
        return redirect(url_match)

# Creazione, Update e Delete Incarico Sicurezza
class Safety_RoleCreateView(LoginRequiredMixin,CreateView):
    model = Safety_Role
    form_class = Safety_RoleModelForm
    template_name = 'human_resources/safety_role.html'
    success_message = 'Incarico aggiunto correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class Safety_RoleUpdateView(LoginRequiredMixin,UpdateView):
    model = Safety_Role
    form_class = Safety_RoleModelForm
    template_name = 'human_resources/safety_role.html'
    success_message = 'Incarico modificato correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    
def delete_safety_role(request, pk): 
        deleteobject = get_object_or_404(Safety_Role, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:tabelle_generiche')
        return redirect(url_match)
    
    
'''FINE SEZIONE TABELLE GENERICHE'''


'''SEZIONE FORMAZIONE'''
# Prevedere una dashboard con grafici per area formazione, ore formazione fornita
# prossime scadenze
def dashboard_formazione(request):
    aree_formazione = AreaFormazione.objects.all()
    corsi_formazione = CorsoFormazione.objects.all()
    registri_formazione = RegistroFormazione.objects.all()
    

    context = {'aree_formazione': aree_formazione, 
                'corsi_formazione': corsi_formazione, 
                'registri_formazione': registri_formazione,               
                }
    
    return render(request, "human_resources/dashboard_formazione.html", context)


# Creazione delle tabelle generiche necessarie
def tabelle_generiche_formazione(request):
    aree_formazione = AreaFormazione.objects.all()
    corsi_formazione = CorsoFormazione.objects.all()
    

    context = {'aree_formazione': aree_formazione, 
                'corsi_formazione': corsi_formazione,                
                }
    
    return render(request, "human_resources/tabelle_generiche_formazione.html", context)

class AreaFormazioneCreateView(LoginRequiredMixin, CreateView):
    model = AreaFormazione
    form_class = AreaFormazioneModelForm
    template_name = 'human_resources/area_formazione.html'
    success_message = 'Area Formazione aggiunta correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class AreaFormazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = AreaFormazione
    form_class = AreaFormazioneModelForm
    template_name = 'human_resources/area_formazione.html'
    success_message = 'Area Formazione modificata correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        print("PK: " + str(pk))
        context['corsi_associati'] = CorsoFormazione.objects.filter(fk_areaformazione=self.object.id) # FILTRARE        
        return context

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    
def delete_area_formazione(request, pk): 
        deleteobject = get_object_or_404(AreaFormazione, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:tabelle_generiche_formazione')
        return redirect(url_match)
    
class CorsoFormazioneCreateView(LoginRequiredMixin, CreateView):
    model = CorsoFormazione
    form_class = CorsoFormazioneModelForm
    template_name = 'human_resources/corso_formazione.html'
    success_message = 'Corso Formazione aggiunto correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

    def form_valid(self, form):               
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class CorsoFormazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = CorsoFormazione
    form_class = CorsoFormazioneModelForm
    template_name = 'human_resources/corso_formazione.html'
    success_message = 'Corso Formazione modificato correttamente!'
    success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    
def delete_corso_formazione(request, pk): 
        deleteobject = get_object_or_404(CorsoFormazione, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('human_resources:tabelle_generiche_formazione')
        return redirect(url_match)
    

# Registro Formazione
class RegistroFormazioneCreateView(LoginRequiredMixin, CreateView):
    model = RegistroFormazione
    form_class = RegistroFormazioneModelForm
    template_name = 'human_resources/registro_formazione.html'
    success_message = 'Formazione aggiunta correttamente!'
        
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('human_resources:dashboard_formazione')
        
        pk_registro_formazione=self.object.pk
        return reverse_lazy('human_resources:modifica_registro_formazione', kwargs={'pk':pk_registro_formazione})


class RegistroFormazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistroFormazione
    form_class = RegistroFormazioneModelForm
    template_name = 'human_resources/registro_formazione.html'
    success_message = 'Formazione modificata correttamente!'    
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        print("PK: " + str(pk))
        context['operatori_associati'] = DettaglioRegistroFormazione.objects.filter(fk_registro_formazione=self.object.id) # FILTRARE        
        return context
    
    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('human_resources:dashboard_formazione')
        
        pk_registro_formazione=self.object.pk
        return reverse_lazy('human_resources:modifica_registro_formazione', kwargs={'pk':pk_registro_formazione})
    

    
def delete_registro_formazione(request, pk): 
        deleteobject = get_object_or_404(RegistroFormazione, pk = pk)   
            
        deleteobject.delete()
        url_match = reverse_lazy('human_resources:dashboard_formazione')
        return redirect(url_match)


# Dettaglio Registro Formazione
class DettaglioRegistroFormazioneCreateView(LoginRequiredMixin, CreateView):
    model = DettaglioRegistroFormazione
    form_class = DettaglioRegistroFormazioneModelForm
    template_name = 'human_resources/dettaglio_registro_formazione.html'
    success_message = 'Operatore aggiunto correttamente!'
    
    def get_initial(self):        
        fk_registro_formazione = self.kwargs['pk']        
        return {
            'fk_registro_formazione': fk_registro_formazione,
        }

    def get_success_url(self):          
        fk_registro_formazione=self.object.fk_registro_formazione.pk        
        return reverse_lazy('human_resources:modifica_registro_formazione', kwargs={'pk':fk_registro_formazione})
    
    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    
class DettaglioRegistroFormazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioRegistroFormazione
    form_class = DettaglioRegistroFormazioneModelForm
    template_name = 'human_resources/dettaglio_registro_formazione.html'
    success_message = 'Operatore modificato correttamente!'
    
    
    def get_success_url(self):          
        fk_registro_formazione=self.object.fk_registro_formazione.pk
        
        return reverse_lazy('human_resources:modifica_registro_formazione', kwargs={'pk':fk_registro_formazione})
    
    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk_registro_formazione = self.kwargs['fk_registro_formazione'] 
        pk_dettaglioregistro = self.kwargs['pk']               
        context['fk_registroformazione'] = RegistroFormazione.objects.get(pk=pk_registro_formazione)
        return context

def delete_dettaglio_registro_formazione(request, pk): 
        deleteobject = get_object_or_404(DettaglioRegistroFormazione, pk = pk)   
        fk_registro_formazione = deleteobject.fk_registro_formazione.pk      
        deleteobject.delete()
        url_match = reverse_lazy('human_resources:modifica_registro_formazione', kwargs={'pk':fk_registro_formazione})
        return redirect(url_match)


'''FINE SEZIONE FORMAZIONE'''

'''SEZIONE REGISTRO ORE'''

def dashboard_registro_ore(request):
    current_year = datetime.date.today().year
    last_three_years = [current_year - i for i in range(3)]
    
    registri_ore = RegistroOreLavoro.objects.filter(entry_year__in=last_three_years)
    somma_ore_lavorate = registri_ore.aggregate(Sum('ore_lavorate'))
    somma_ore_lavorabili = registri_ore.aggregate(Sum('ore_lavorabili'))
    somma_ore_ferie = registri_ore.aggregate(Sum('ferie_permessi'))
    
    #queryset = RegistroFormazione.objects.values('fk_corso__fk_areaformazione__descrizione').annotate(ore_lavorate=Sum('ore_lavorate'))
    if somma_ore_ferie:
        print("Ore lavorare: " + str(somma_ore_ferie))
    else:
        print("Vuoto")

    context = {'registri_ore': registri_ore, 
            'somma_ore_lavorate': somma_ore_lavorate['ore_lavorate__sum'], 
            'somma_ore_lavorabili': somma_ore_lavorabili['ore_lavorabili__sum'],
            'somma_ore_ferie': somma_ore_ferie['ferie_permessi__sum'],

                
                }
    
    return render(request, "human_resources/dashboard_registro_ore.html", context)


class RegistroOreLavoroCreateView(LoginRequiredMixin, CreateView):
    model = RegistroOreLavoro
    form_class = RegistroOreLavoroModelForm
    template_name = 'human_resources/registro_ore.html'
    success_message = 'Mese aggiunto correttamente!'
    success_url = reverse_lazy('human_resources:dashboard_registro_ore')

    def get_initial(self):        
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

    
    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)


class RegistroOreLavoroUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistroOreLavoro
    form_class = RegistroOreLavoroModelForm
    template_name = 'human_resources/registro_ore.html'
    success_message = 'Mese modificato correttamente!'
    success_url = reverse_lazy('human_resources:dashboard_registro_ore')

    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

def delete_registro_ore(request, pk): 
        deleteobject = get_object_or_404(RegistroOreLavoro, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('human_resources:dashboard_registro_ore')
        return redirect(url_match)

'''FINE SEZIONE REGISTRO ORE'''

