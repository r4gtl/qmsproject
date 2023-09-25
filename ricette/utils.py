from .models import RicettaRifinizione, DettaglioRicettaRifinizione
from chem_man.models import ProdottoChimico, PrezzoProdotto
from django.db import models
from django.db.models import Sum, OuterRef, F, Subquery, FloatField


