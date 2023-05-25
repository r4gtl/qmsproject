from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from .models import Fornitore, Facility, FacilityContact
from .forms import FormFornitore, FormFacility, FormFacilityContact
from .filters import FornitoreFilter

# Create your views here.

def home_fornitori(request): 
    fornitori = Fornitore.objects.all()
    filterset_class = FornitoreFilter
    context = {
        'fornitori': filterset_class,
        'filterset': filterset_class
    }
    return render(request, 'anagrafiche/home_fornitori.html', context)

def vedi_fornitore(request, pk):
    fornitore = get_object_or_404(Fornitore, pk=pk)
    form = FormFornitore(request.POST)
    print("Sono qui: " + str(fornitore) + str(fornitore.pk))
    print("Request method:" + str(request.method))
    if request.method == "POST":
        print("Sono qui sul post")
        if form.is_valid():
            fornitore_salvato = form.save(commit=False)
            fornitore_salvato.save()
            #url_match= reverse_lazy('anagrafiche:home_fornitori')
            #return redirect(url_match)
            return HttpResponseRedirect(reverse_lazy('anagrafiche:home_fornitori'))
            #return render(request, "anagrafiche/home_fornitori.html")
    else:
        print("Sono qui sul get")
        print("Fornitore: " + str(fornitore))
        form = FormFornitore(instance=fornitore)
            
        print("Sono qui sul fondo")    
        context = {'fornitore': fornitore, 'form': form}
        return render(request, "anagrafiche/fornitore.html", context)



def aggiungi_fornitore(request, pk):
    fornitore = get_object_or_404(Fornitore, pk=pk)
    if request.method == "POST":
        form = FormFornitore(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.fornitore = fornitore
        else:
            form = FormFornitore()
        context = {'fornitore': fornitore, 'form': form}
        return render(request, "anagrafiche/fornitore.html", context)

class CreateSupplier(CreateView):
    model = Fornitore
    fields = "__all__"
    
    template_name = "anagrafiche/fornitore.html"
    

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
    
    

    

    
    