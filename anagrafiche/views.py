from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView


from .filters import FornitoreFilter

from .models import (Fornitore, Facility, 
                     FacilityContact, LwgFornitore, 
                     TransferValue, XrTransferValueLwgFornitore
)

from .forms import (FormFornitore, FormFacility,
                    FormFacilityContact, FormLwgFornitore,
                    FormXrTransferValueLwgFornitore,
)

# Create your views here.

def home_fornitori(request): 
    fornitori = Fornitore.objects.all()
    filterset_class = FornitoreFilter
    context = {
        'fornitori': filterset_class,
        'filterset': filterset_class
    }
    return render(request, 'anagrafiche/home_fornitori.html', context)

# def vedi_fornitore(request, pk):
#     fornitore = get_object_or_404(Fornitore, pk=pk)
#     form = FormFornitore(request.POST)
#     print("Sono qui: " + str(fornitore) + str(fornitore.pk))
#     print("Request method:" + str(request.method))
#     if request.method == "POST":
#         print("Sono qui sul post")
#         if form.is_valid():
#             fornitore_salvato = form.save(commit=False)
#             fornitore_salvato.save()
#             #url_match= reverse_lazy('anagrafiche:home_fornitori')
#             #return redirect(url_match)
#             return HttpResponseRedirect(reverse_lazy('anagrafiche:home_fornitori'))
#             #return render(request, "anagrafiche/home_fornitori.html")
#     else:
#         print("Sono qui sul get")
#         print("Fornitore: " + str(fornitore))
#         form = FormFornitore(instance=fornitore)
            
#         print("Sono qui sul fondo")    
#         context = {'fornitore': fornitore, 'form': form}
#         return render(request, "anagrafiche/fornitore.html", context)



# def aggiungi_fornitore(request):
#     #fornitore = get_object_or_404(Fornitore, pk=pk)
#     print(request.is_lwg)
#     if request.method == "POST":
#         form = FormFornitore(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             #form.instance.fornitore = fornitore
#         else:
#             form = FormFornitore()
#         context = {'form': form}
#         return render(request, "anagrafiche/fornitore.html", context)

class UpdateSupplier(LoginRequiredMixin, UpdateView):
    model = Fornitore
    template_name = 'anagrafiche/fornitore.html'
    form_class = FormFornitore
    success_url = reverse_lazy('anagrafiche:home_fornitori')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["lwg_certs"] = LwgFornitore.objects.filter(fk_fornitore_id=self.object.pk) 
        
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
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["lwg_certs"] = LwgFornitore.objects.filter(fk_fornitore_id=self.fornitore_id) 
        return context
    
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
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          fornitore=self.object.fk_fornitore.pk
          return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})

    def get_initial(self):
        fk_fornitore = self.kwargs['fk_fornitore']
        return {
            'fk_fornitore': fk_fornitore,
            
        }
    
    #def get_context_data(self, **kwargs):        
    #    context = super().get_context_data(**kwargs)
    #    pk = self.object.pk
    #    print("PK: " + str(pk))
    #    context['transfer_values'] = XrTransferValueLwgFornitore.objects.filter(fk_lwgfornitore_id=self.object.id) # FILTRARE
    #    return context

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


class AddXrTranferValue(CreateView):
    model = XrTransferValueLwgFornitore
    form_class = FormXrTransferValueLwgFornitore
    success_message = 'Certificato modificato correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    template_name = "anagrafiche/lwg_transfer_values.html"

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print("kwargs: " + str(self.kwargs))  
        #context['fornitore'] = self.object.fornitore.pk
        
        context['lwg_cert'] = self.kwargs['pk']
        #context['certificato'] = LwgFornitore.objects.get(pk=self.object.pk)
        
        return context

    #def get_initial(self):
    #    fk_fornitore = self.kwargs['fk_fornitore']
    #    return {
    #        'fk_fornitore': fk_fornitore,
    #        
    #    }
    

    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          lwgcertificate=self.object.fk_lwgfornitore.pk
          return reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk': lwgcertificate})
    
    


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

def edit_facility_details(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    # print("Facility:" + str(facility))
    facility_contacts = FacilityContact.objects.filter(fk_facility=pk)
    form = FormFacility()
    # print("Facility contacts:" + str(facility_contacts))
    if request.method == "POST":
        form = FormFacility(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.facility = facility
        else:
            form = FormFacility()

    context = {'facility': facility, 
                'form': form,
                'facility_contacts': facility_contacts
                }
    
    return render(request, "anagrafiche/facility.html", context)
    

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
    
    

    

    
    