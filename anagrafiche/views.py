from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django_filters.views import FilterView


from .filters import FornitoreFilter, ClienteFilter

from .models import (Fornitore, Facility, 
                    FacilityContact, LwgFornitore, 
                    TransferValue, XrTransferValueLwgFornitore,
                    Cliente
)

from nonconformity.models import RapportoNC

from .forms import (FormFornitore, FormFacility,
                    FormFacilityContact, FormLwgFornitore,
                    FormXrTransferValueLwgFornitore, FormTransferValue,
                    FormCliente
)

# Create your views here.

def home_fornitori(request): 
    fornitori = Fornitore.objects.all()
    fornitori_filter = FornitoreFilter(request.GET, queryset=fornitori)
    #filterset_class = FornitoreFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(fornitori_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione
            
    try:
        fornitori_paginator = paginator.page(page)
    except PageNotAnInteger:
        fornitori_paginator = paginator.page(1)
    except EmptyPage:
        fornitori_paginator = paginator.page(paginator.num_pages)
        
    context = {
        #'fornitori': filterset_class,
        'fornitori_paginator': fornitori_paginator,
        'filter': fornitori_filter
    }
    return render(request, 'anagrafiche/home_fornitori.html', context)


class UpdateSupplier(LoginRequiredMixin, UpdateView):
    model = Fornitore
    template_name = 'anagrafiche/fornitore.html'
    form_class = FormFornitore
    success_url = reverse_lazy('anagrafiche:home_fornitori')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["lwg_certs"] = LwgFornitore.objects.filter(fk_fornitore_id=self.object.pk) 
        context["nc_associate"] = RapportoNC.objects.filter(fk_fornitore=self.object.pk) 
        
        return context
    
    def form_valid(self, form):        
        messages.info(self.request, 'Il fornitore è stato modificato!') # Compare sul success_url
        return super().form_valid(form)
    
class CreateSupplier(LoginRequiredMixin, CreateView):
    
    model = Fornitore
    form_class = FormFornitore
    success_message = 'Fornitore aggiunto correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    
    #fields = "__all__"
    success_url = reverse_lazy('anagrafiche:home_fornitori')
    
    template_name = "anagrafiche/fornitore.html"

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
            'created_at': datetime.datetime.now() 
        }
        
        
    
    
    def form_valid(self, form):        
        messages.info(self.request, 'Il fornitore è stato aggiunto!') # Compare sul success_url
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Errore! Il fornitore non è stato aggiunto!')
        return super().form_invalid(form)


class AddLwgCertificate(CreateView):
    
    model = LwgFornitore
    form_class = FormLwgFornitore
    success_message = 'Certificato aggiunto correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    
    #fields = "__all__"
    #success_url = reverse_lazy('anagrafiche:vedi_fornitore')
    
    template_name = "anagrafiche/lwg.html"


    def get_success_url(self):          
          fornitore=self.object.fk_fornitore
          print("Fornitore: " + str(fornitore))
          return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})

    def get_initial(self):
        fk_fornitore = self.kwargs['fk_fornitore']
        return {
            'fk_fornitore': fk_fornitore,
            
        }
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fornitore=self.kwargs['fk_fornitore']
        print("Fornitore: " + str(fornitore))
        context['fornitore'] = Fornitore.objects.get(pk=fornitore) # FILTRARE
        return context

class UpdateLwgCertificate(UpdateView):
    
    model = LwgFornitore
    form_class = FormLwgFornitore
    success_message = 'Certificato modificato correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    
    #fields = "__all__"
    #success_url = reverse_lazy('anagrafiche:vedi_fornitore')
    
    template_name = "anagrafiche/lwg.html"


    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          fornitore=self.object.fk_fornitore.pk
          return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        print("PK: " + str(pk))
        context['transfer_values'] = XrTransferValueLwgFornitore.objects.filter(fk_lwgfornitore_id=self.object.id) # FILTRARE
        context['fornitore'] = self.object.fk_fornitore.pk
        context['ragionesociale'] = Fornitore.objects.get(pk=self.object.fk_fornitore.pk)
        print("Context: " + str(context['ragionesociale']))
        return context



def delete_certificato(request, pk): 
        deleteobject = get_object_or_404(LwgFornitore, pk = pk)
        fornitore=deleteobject.fk_fornitore.pk   
        #dettaglio=deleteobject.iddettordine           
        #linea = deleteobject.id_linea  
        #tempomaster=deleteobject.idtempomaster      
        deleteobject.delete()
        url_match= reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})
        return redirect(url_match)

class XrTransferValueCreateView(CreateView):
    model = XrTransferValueLwgFornitore
    form_class = FormXrTransferValueLwgFornitore
    success_message = 'Transfer Value modificata correttamente!'
    success_url = reverse_lazy('anagrafiche:modifica_lwg')
    template_name = "anagrafiche/lwg_transfer_values.html"

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        
        context['fornitore'] = self.kwargs['pk']
        return context

    def get_initial(self):
        fk_fornitore = self.kwargs['pk']
        return {
            'fk_lwgfornitore': self.kwargs['pk']
            
        }
    
class XrTransferValueUpdateView(LoginRequiredMixin,UpdateView):
    model = XrTransferValueLwgFornitore
    form_class = FormXrTransferValueLwgFornitore
    template_name = 'anagrafiche/lwg_transfer_values.html'
    success_message = 'Transfer Value modificata correttamente!'
    success_url = reverse_lazy('anagrafiche:modifica_lwg')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)



    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          lwgcertificate=self.object.fk_lwgfornitore.pk
          return reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk': lwgcertificate})
    

class XrTransferValueDeleteView(LoginRequiredMixin, DeleteView):
    # specify the model you want to use
    model = XrTransferValueLwgFornitore
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          lwgcertificate=self.object.fk_lwgfornitore.pk
          return reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk': lwgcertificate})
     
    #template_name = "geeks/geeksmodel_confirm_delete.html"


class ListaFornitoriView(FilterView):

        model = Fornitore
        context_object_name = 'initial_fornitori'
        template_name = "anagrafiche/home_fornitori.html"
        filterset_class = FornitoreFilter
        paginate_by = 30
        # ordering = ['-iddettordine']
        
def aggiungi_facility_details(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == "POST":
        form = FormFacility(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.facility = facility
        else:
            form = FormFacility()
        context = {'facility': facility, 'form': form}
        
        return render(request, "anagrafiche/facility.html", context)
    
    
class FacilityCreateView(CreateView):
    template_name = 'anagrafiche/facility.html'
    form_class = FormFacility
    
class FacilityUpdateView(UpdateView):
    model = Facility
    template_name = 'anagrafiche/facility.html'
    form_class = FormFacility
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['facility_contacts'] = FacilityContact.objects.filter(fk_facility=self.object.pk)        
        return context

# def edit_facility_details(request, pk):
#     facility = get_object_or_404(Facility, pk=pk)
#     # print("Facility:" + str(facility))
#     facility_contacts = FacilityContact.objects.filter(fk_facility=pk)
#     form = FormFacility()
#     # print("Facility contacts:" + str(facility_contacts))
#     if request.method == "POST":
#         form = FormFacility(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             form.instance.facility = facility
#         else:
#             form = FormFacility()

#     context = {'facility': facility, 
#                 'form': form,
#                 'facility_contacts': facility_contacts
#                 }
    
#     return render(request, "anagrafiche/facility.html", context)
    

def add_facility_contact(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    
    if request.method == "POST":
        form = FormFacilityContact(request.POST)
        fk_facility = facility
        nome_cognome = request.POST.get("name")
        contact_type = request.POST.get("contact_type")
        position = request.POST.get("position")
        facility_contact = FacilityContact.objects.create(name=nome_cognome, 
                                                            contact_type=contact_type,
                                                            position=position,
                                                            fk_facility=fk_facility
                                                            )
        messages.info(request, 'Il contatto è stato aggiunto!')
        return redirect('anagrafiche:edit_facility_details', pk=pk)
    else:
        form = FormFacilityContact()

    return render(request, 'anagrafiche/facility_contacts.html', {'facility': facility, 'form': form})
    
    
class FacilityContactUpdateView(LoginRequiredMixin, UpdateView):
    model = FacilityContact
    form_class = FormFacilityContact
    template_name = 'anagrafiche/facility_contacts.html'
    success_message = 'Contatto modificato correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):                
        fk_facility=self.object.fk_facility.pk        
        return reverse_lazy('anagrafiche:edit_facility_details', kwargs={'pk':fk_facility})

def delete_facility_contact(request, pk): 
        deleteobject = get_object_or_404(FacilityContact, pk = pk)         
        fk_facility=deleteobject.fk_facility.pk       
        deleteobject.delete()
        url_match= reverse_lazy('anagrafiche:edit_facility_details', kwargs={'pk':fk_facility})
        return redirect(url_match)    

# Creazione, Vista e Update Clienti
class ClienteCreateView(LoginRequiredMixin,CreateView):
    model = Cliente
    form_class = FormCliente
    template_name = 'anagrafiche/cliente.html'
    success_message = 'Cliente aggiunto correttamente!'
    success_url = reverse_lazy('anagrafiche:home_clienti')
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
            'created_at': datetime.datetime.now() 
        }
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

class ClienteUpdateView(LoginRequiredMixin,UpdateView):
    model = Cliente
    form_class = FormCliente
    template_name = 'anagrafiche/cliente.html'
    success_message = 'Cliente modificato correttamente!'
    success_url = reverse_lazy('anagrafiche:home_clienti')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'anagrafiche/home_clienti.html'
    paginate_by = 10


class ListaClienteView(FilterView):

        model = Cliente
        context_object_name = 'initial_clienti'
        template_name = "anagrafiche/home_clienti.html"
        filterset_class = ClienteFilter
        paginate_by = 30





'''SEZIONE TABELLE GENERICHE'''

# Creazione, Vista e Update Transfer Values
class TransferValueCreateView(LoginRequiredMixin,CreateView):
    model = TransferValue
    form_class = FormTransferValue
    template_name = 'anagrafiche/transfer_value.html'
    success_message = 'Transfer Value aggiunta correttamente!'
    success_url = reverse_lazy('anagrafiche:transfer_values_list')

class TransferValueUpdateView(LoginRequiredMixin,UpdateView):
    model = TransferValue
    form_class = FormTransferValue
    template_name = 'anagrafiche/transfer_value.html'
    success_message = 'Transfer Value modificata correttamente!'
    success_url = reverse_lazy('anagrafiche:transfer_values_list')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    
class TransferValueListView(LoginRequiredMixin, ListView):
    model = TransferValue
    template_name = 'anagrafiche/transfer_values_list.html'
    paginate_by = 10



'''FINE SEZIONE TABELLE GENERICHE'''
    

    
    