from django.db import models
from django.urls import reverse


class Ward(models.Model):
    
    description = models.CharField(max_length=50, null=False, blank=False, help_text="Nome reparto", db_column="descrizionereparto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["description"]
        verbose_name_plural = "wards"
        db_table = "reparti"

class Role(models.Model):
    
    description = models.CharField(max_length=50, null=False, blank=False, help_text="Nome mansione", db_column="descrizionemansione")
    fk_reparto = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["description"]
        verbose_name_plural = "roles"
        db_table = "mansioni"

class HumanResource(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    cognomedipendente = models.CharField(max_length=50, null=False, blank=False)
    nomedipendente = models.CharField(max_length=50, null=False, blank=False)
    immagine = models.ImageField(upload_to='operator_pictures/', default= 'avataaars.png',null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    dataassunzione = models.DateField(null=False, blank=False)
    datadimissioni = models.DateField(null=True, blank=True)
    fk_mansione = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    fk_reparto = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL)
    qualifica = models.CharField(max_length=50, null=True, blank=True)
    commenti = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cognomedipendente + " " + self.nomedipendente

    def get_absolute_url(self):
        return reverse("human_resources:update-human-resource", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-dataassunzione"]
        verbose_name_plural = "dipendenti"
        db_table = "dipendenti"