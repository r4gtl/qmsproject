from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from .filters import LottoFilter
from anagrafiche.models import Fornitore
from .models import (TipoAnimale, TipoGrezzo, 
                    Scelta, Lotto, 
                    SceltaLotto
)

from .forms import (LottoModelForm, SceltaModelForm,
                    SceltaLottoModelForm, TipoAnimaleModelForm,
                    TipoGrezzoModelForm
)

def dashboard_acquisto_pelli(request):     
    lotti = Lotto.objects.all()
    
    lotti_filter = LottoFilter(request.GET, queryset=lotti)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(lotti, 50)
    
    try:
        lotti_paginator = paginator.page(page)
    except PageNotAnInteger:
        lotti_paginator = paginator.page(1)
    except EmptyPage:
        lotti_paginator = paginator.page(paginator.num_pages)
    context={
        'lotti_paginator': lotti_paginator,
        'filter': lotti_filter,
        
    }
    
    return render(request, 'acquistopelli/dashboard_acquisto_pelli.html', context)


class LottoCreateView(LoginRequiredMixin,CreateView):
    model = Lotto
    form_class = LottoModelForm
    template_name = 'acquistopelli/lotto.html'
    success_message = 'Lotto aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('acquistopelli:dashboard_acquisto_pelli')
        
        pk_lotto=self.object.pk
        return reverse_lazy('human_resources:modifica_lotto', kwargs={'pk':pk_lotto})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)