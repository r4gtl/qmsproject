from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
    context = {'fornitore': fornitore}
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
    print("Facility:" + str(facility))
    facility_contacts = FacilityContact.objects.filter(fk_facility=pk)
    form = FormFacility()
    print("Facility contacts:" + str(facility_contacts))
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
                                                            position=request.user,
                                                            fk_facility=fk_facility
                                                            )
        messages.info(request, 'The project was added!')
        return redirect('anagrafiche:facility')

    return render(request, 'anagrafiche/facility_contacts.html', {'facility': facility, 'form': form})
    
    

    

    
    