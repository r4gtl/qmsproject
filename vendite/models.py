from acquistopelli.models import Lotto
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
    fk_ordine= models.ForeignKey(OrdineCliente, related_name= 'dettaglio_ordine', on_delete=models.CASCADE)



    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_ordine_cliente', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:        
        verbose_name = "Dettaglio Ordine"
        verbose_name_plural = "Dettaglio Ordini Cliente"
    