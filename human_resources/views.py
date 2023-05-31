from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import HumanResource, Ward, Role
from .forms import HumanResourceModelForm, WardModelForm, RoleModelForm
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
        return reverse("human_resources:human_resources")
        
 
    # add form dictionary to context
    context["form"] = form
    context["obj"] = obj
 
    return render(request, "update_view.html", context)


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


# Creazione, Vista e Update Ward
class WardCreateView(LoginRequiredMixin,CreateView):
    model = Ward
    form_class = WardModelForm
    template_name = 'human_resources/ward.html'
    success_message = 'Reparto aggiunto correttamente!'
    success_url = reverse_lazy('human_resource:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

class WardUpdateView(LoginRequiredMixin,UpdateView):
    model = Ward
    form_class = WardModelForm
    template_name = 'human_resource/ward.html'
    success_message = 'Reparto modificato correttamente!'
    success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    
class WardDeleteView(LoginRequiredMixin, DeleteView):
    model = Ward
    success_url = reverse_lazy('human_resources:human_resources')
    

'''FINE SEZIONE TABELLE GENERICHE'''