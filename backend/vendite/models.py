from acquistopelli.models import Lotto, SceltaLotto
from anagrafiche.models import Cliente
from articoli.models import Articolo, Colore
from django.contrib.auth.models import User
from django.db import models


class OrdineCliente(models.Model):
    numero_ordine=models.CharField(max_length=10)
    data_ordine=models.DateField(null=False, blank=False)
    fk_cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Cliente")
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='ordine_cliente', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_ordine"]
        verbose_name="Ordine Cliente"
        verbose_name_plural = "Ordini Cliente"

    def __str__(self):
        return str("Ordine n. " + " " + self.numero_ordine) + " del " + str(self.data_ordine)
    
class DettaglioOrdineCliente(models.Model):
    fk_ordine = models.ForeignKey(OrdineCliente, related_name= 'dettaglio_ordine', on_delete=models.CASCADE)
    riferimento = models.CharField(max_length=15, null=True, blank=True)
    fk_articolo = models.ForeignKey(Articolo, related_name = 'dettaglio_ordine', on_delete=models.DO_NOTHING, verbose_name = 'Articolo')
    fk_colore = models.ForeignKey(Colore, related_name = 'dettaglio_ordine', on_delete=models.DO_NOTHING, verbose_name = 'Colore')
    um = models.CharField(max_length=5, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    data_consegna = models.DateField(null=True, blank=True)
    in_lavorazione = models.BooleanField(default=False)
    data_messa_in_lavoro = models.DateField(null=True, blank=True)
    completato = models.BooleanField(default=False)
    data_completamento = models.DateField(null=True, blank=True)


    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_ordine_cliente', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:        
        verbose_name = "Dettaglio Ordine"
        verbose_name_plural = "Dettaglio Ordini Cliente"

class SchedaLavorazione(models.Model):
    data_scheda = models.DateField(null=True, blank=True)
    fk_dettaglio_ordine_cliente = models.ForeignKey(DettaglioOrdineCliente, related_name= 'scheda_lavorazione', on_delete=models.CASCADE)
    fk_articolo = models.ForeignKey(Articolo, related_name = 'scheda_lavorazione', on_delete=models.DO_NOTHING, verbose_name = 'Articolo')
    fk_colore = models.ForeignKey(Colore, related_name = 'scheda_lavorazione', on_delete=models.DO_NOTHING, verbose_name = 'Colore')
    tot_pelli = models.PositiveIntegerField(null=True, blank=True)
    tot_pelli_finale = models.PositiveIntegerField(null=True, blank=True)
    metri_quadrati_finali = models.DecimalField(null=True, blank=True,
    max_digits=10,
    decimal_places=2,
    verbose_name = "Superficie (m²)",
    help_text = "Inserisci la superficie in metri quadrati"
)
    scheda_chiusa = models.BooleanField(default=False)
    data_chiusura = models.DateField(null=True, blank=True, verbose_name = 'Data Chiusura Scheda')
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='scheda_lavorazione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:        
        verbose_name = "Scheda lavorazione"
        verbose_name_plural = "Schede Lavorazione"

    def __str__(self):
        return str("Scheda n. " + " " + str(self.pk)) + " del " + str(self.data_scheda)
    


class XRScelteSchede(models.Model):
    fk_sceltalotto = models.ForeignKey(SceltaLotto, related_name= 'xrscelteschede', on_delete=models.CASCADE)
    fk_schedalavorazione = models.ForeignKey(SchedaLavorazione, related_name= 'xrscelteschede', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='xrscelteschede', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    