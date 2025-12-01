from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from PIL import Image


class Company(models.Model):
    """
    Model for Company (Azienda) - Core of Multi-Tenant SaaS
    Each company has its own isolated data
    """
    name = models.CharField(max_length=200, verbose_name="Nome Azienda")
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # Company details
    vat_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Partita IVA")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Indirizzo")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Città")
    country = models.CharField(max_length=100, default='IT', verbose_name="Paese")

    # Branding
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Logo")

    # Status and subscription
    is_active = models.BooleanField(default=True, verbose_name="Attiva")
    subscription_plan = models.CharField(
        max_length=50,
        default='free',
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        verbose_name="Piano Subscription"
    )
    subscription_expires = models.DateField(null=True, blank=True, verbose_name="Scadenza Subscription")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Azienda"
        verbose_name_plural = "Aziende"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Profile(models.Model):
    """
    Extended User Profile with Company relationship
    """
    # User roles
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_USER = 'user'
    ROLE_VIEWER = 'viewer'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Amministratore'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_USER, 'Utente'),
        (ROLE_VIEWER, 'Visualizzatore'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name="Azienda",
        null=True,  # Temporary: will be required after data migration
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        verbose_name="Ruolo"
    )
    avatar = models.ImageField(default='avatar.png', upload_to='profile_pics', verbose_name="Avatar")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")

    # Additional fields
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telefono")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Reparto")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Profilo Utente"
        verbose_name_plural = "Profili Utenti"

    def __str__(self):
        return f'{self.user.username} - {self.company.name}'

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_manager(self):
        return self.role in [self.ROLE_ADMIN, self.ROLE_MANAGER]
