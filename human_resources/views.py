from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import (HumanResource, Ward, Role, 
                    AreaFormazione, CorsoFormazione,
                    )
from .forms import (HumanResourceModelForm, WardModelForm, RoleModelForm,
                    AreaFormazioneModelForm, CorsoFormazioneModelForm
                    )
from .filters import HRFilter

# Create your views here.
def human_resources_home(request):
    hr = HumanResource.objects.all().order_by('cognomedipendente')
    
    hr_filter = HRFilter(request.GET, queryset=hr)
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
        'filter': hr_filter
    }
    return render(request, "human_resources/human_resources_home.html", context)

def add_new_operator(request):    
    context ={}    
    form = HumanResourceModelForm(request.POST or None)
    
    if form.is_valid():
        form.save()
          
    context['form']= form
    return render(request, "human_resources/single_operator.html", context)

def update_human_resource(request, pk):    
    context ={}    
    obj = get_object_or_404(HumanResource, pk = pk)    
    form = HumanResourceModelForm(request.POST or None, instance = obj) 
    if form.is_valid():
        form.save()
        #return reverse("human_resources:human_resources")
        url_match= reverse_lazy('human_resources:human_resources')
        return redirect(url_match)
        
 
    # add form dictionary to context
    context["form"] = form
    context["obj"] = obj
 
    return render(request, "human_resources/single_operator.html", context)


# if request.method == 'POST':
                
        #         if form.is_valid():
        #                 supplier_saved = form.save(commit=False)
        #                 supplier_saved.save()
        #                 #Non funziona
                        
        #                 return HttpResponseRedirect(reverse('master_data:search-supplier'))
        # else:
                
        #         form = SupplierModelForm(instance=supplier)
        # context = {"supplier": supplier, "contacts": contacts, 'form':form}        
        # return render(request, "master_data/create_supplier.html", context)



'''SEZIONE TABELLE GENERICHE'''

def tabelle_generiche(request):
    wards = Ward.objects.all()
    roles = Role.objects.all()
    

    context = {'wards': wards, 
                'roles': roles,                
                }
    
    return render(request, "human_resources/tabelle_generiche_hr.html", context)


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
    
    
'''FINE SEZIONE TABELLE GENERICHE'''


'''SEZIONE FORMAZIONE'''
# Creazione delle tabelle generiche necessarie

def tabelle_generiche_formazione(request):
    aree_formazione = AreaFormazione.objects.all()
    corsi_formazione = CorsoFormazione.objects.all()
    

    context = {'aree_formazione': aree_formazione, 
                'corsi_formazione': corsi_formazione,                
                }
    
    return render(request, "human_resources/tabelle_generiche_formazione.html", context)

class AreaFormazioneCreateView(LoginRequiredMixin,CreateView):
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

class AreaFormazioneUpdateView(LoginRequiredMixin,UpdateView):
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
    
class CorsoFormazioneCreateView(LoginRequiredMixin,CreateView):
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
        print("Eccomi")      
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class CorsoFormazioneUpdateView(LoginRequiredMixin,UpdateView):
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
