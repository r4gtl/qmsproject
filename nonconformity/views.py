from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView



from .models import Processo, RapportoNC, RapportoAudit
from .forms import ProcessoModelForm, RapportoNCModelForm, RapportoAuditModelForm
from .filters import RapportoAuditFilter, RapportoNCFilter


def home_rapporti_nc(request): 
    rapporti_nc = RapportoNC.objects.all()
    rapporti_nc_filter = RapportoNCFilter(request.GET, queryset=rapporti_nc)
    #filterset_class = FornitoreFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(rapporti_nc_filter.qs, 50)  # Utilizza rapporti_nc_filter.qs per la paginazione
            
    try:
        rapporti_nc_filter_paginator = paginator.page(page)
    except PageNotAnInteger:
        rapporti_nc_filter_paginator = paginator.page(1)
    except EmptyPage:
        rapporti_nc_filter_paginator = paginator.page(paginator.num_pages)
        
    context = {
        
        'rapporti_nc_filter_paginator': rapporti_nc_filter_paginator,
        'filter': rapporti_nc_filter
    }
    return render(request, 'nonconformity/home_rapporti_nc.html', context)



class RapportoNCCreateView(LoginRequiredMixin,CreateView):
    model = RapportoNC
    form_class = RapportoNCModelForm
    template_name = 'nonconformity/rapporto_nc.html'
    success_message = 'Rapporto aggiunto correttamente!'
    

    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:home_rapporti_nc')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class RapportoNCUpdateView(LoginRequiredMixin, UpdateView):
    model = RapportoNC
    form_class = RapportoNCModelForm
    template_name = 'nonconformity/rapporto_nc.html'
    success_message = 'Rapporto modificato correttamente!'
    
    
    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:home_rapporti_nc')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_rapporto_nc(request, pk): 
        deleteobject = get_object_or_404(RapportoNC, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('nonconformity:home_rapporti_nc')
        return redirect(url_match)



'''Rapporti di Audit'''


def home_rapporti_audit(request): 
    rapporti_audit = RapportoAudit.objects.all()
    rapporti_audit_filter = RapportoNCFilter(request.GET, queryset=rapporti_audit)
    #filterset_class = FornitoreFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(rapporti_audit_filter.qs, 50)  # Utilizza rapporti_audit_filter.qs per la paginazione
            
    try:
        rapporti_audit_filter_paginator = paginator.page(page)
    except PageNotAnInteger:
        rapporti_audit_filter_paginator = paginator.page(1)
    except EmptyPage:
        rapporti_audit_filter_paginator = paginator.page(paginator.num_pages)
        
    context = {
        
        'rapporti_audit_filter_paginator': rapporti_audit_filter_paginator,
        'filter': rapporti_audit_filter
    }
    return render(request, 'nonconformity/home_rapporti_audit.html', context)



class RapportoAuditCreateView(LoginRequiredMixin,CreateView):
    model = RapportoAudit
    form_class = RapportoAuditModelForm
    template_name = 'nonconformity/rapporto_audit.html'
    success_message = 'Rapporto aggiunto correttamente!'
    

    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:home_rapporti_audit')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class RapportoAuditUpdateView(LoginRequiredMixin, UpdateView):
    model = RapportoAudit
    form_class = RapportoAuditModelForm
    template_name = 'nonconformity/rapporto_audit.html'
    success_message = 'Rapporto modificato correttamente!'
    
    
    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:home_rapporti_audit')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_rapporto_audit(request, pk): 
        deleteobject = get_object_or_404(RapportoAudit, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('nonconformity:home_rapporti_audit')
        return redirect(url_match)