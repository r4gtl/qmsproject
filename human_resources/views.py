from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.edit import CreateView, UpdateView
from .models import HumanResource
from .forms import HumanResourceModelForm
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
