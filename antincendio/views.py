from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .filters import *
from .forms import *



# Create your views here.



def antincendio_home(request):
    estintori = Estintore.objects.all()
    tot_estintori = Estintore.objects.filter(data_dismissione__isnull=True).count()
    estintori_filter = EstintoreFilter(request.GET, queryset=estintori)
    filtered_estintori = estintori_filter.qs
    estintori_filter_count = filtered_estintori.count()

    
    # Paginazione Estintori
    page_estintori = request.GET.get('page', 1)
    paginator_estintori = Paginator(filtered_estintori, 50)
    try:
        estintori_paginator = paginator_estintori.page(page_estintori)
    except PageNotAnInteger:
        estintori_paginator = paginator_estintori.page(1)
    except EmptyPage:
        estintori_paginator = paginator_estintori.page(paginator_estintori.num_pages)




    context = {
        # Estintori
        'estintori': estintori,
        'estintori_paginator': estintori_paginator,
        'tot_estintori': tot_estintori,
        'filter_estintori': estintori_filter,
        'estintori_filter_count': estintori_filter_count,
        

    }

    return render(request, 'antincendio/home_antincendio.html', context)



# Estintori

class EstintoreCreateView(LoginRequiredMixin,CreateView):
    model = Estintore
    form_class = EstintoreModelForm
    template_name = 'antincendio/estintore.html'
    success_message = 'Estintore aggiunto correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:home_antincendio')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class EstintoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Estintore
    form_class = EstintoreModelForm
    template_name = 'antincendio/estintore.html'
    success_message = 'Estintore modificato correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:home_antincendio')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_estintore(request, pk):
        deleteobject = get_object_or_404(Estintore, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:home_antincendio')
        return redirect(url_match)