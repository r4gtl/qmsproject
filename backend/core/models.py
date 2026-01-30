from django.db import models
from threading import local

# Thread-local storage for current company context
_thread_locals = local()


def get_current_company():
    """
    Get the current company from thread-local storage.
    This is set by the CompanyMiddleware.
    """
    return getattr(_thread_locals, 'company', None)


def set_current_company(company):
    """
    Set the current company in thread-local storage.
    Called by CompanyMiddleware.
    """
    _thread_locals.company = company


class CompanyOwnedQuerySet(models.QuerySet):
    """
    Custom QuerySet that automatically filters by company
    """
    def for_company(self, company):
        """Filter queryset by specific company"""
        return self.filter(company=company)

    def for_current_company(self):
        """Filter queryset by current company from thread-local"""
        company = get_current_company()
        if company:
            return self.filter(company=company)
        return self.none()


class CompanyOwnedManager(models.Manager):
    """
    Manager that automatically filters all queries by current company
    """
    def get_queryset(self):
        qs = CompanyOwnedQuerySet(self.model, using=self._db)
        company = get_current_company()
        if company:
            return qs.filter(company=company)
        return qs

    def all_companies(self):
        """
        Get all records across all companies (for superuser/admin only)
        """
        return CompanyOwnedQuerySet(self.model, using=self._db)


class CompanyOwnedModel(models.Model):
    """
    Abstract base model for all company-owned models.

    Usage:
        class MyModel(CompanyOwnedModel):
            name = models.CharField(max_length=100)
            # company field is automatically added

    All queries will be automatically filtered by the current company.
    """
    company = models.ForeignKey(
        'accounts.Company',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name="Azienda",
        null=True,  # Temporary for migration
        blank=True
    )

    objects = CompanyOwnedManager()
    all_objects = models.Manager()  # Unfiltered manager for admin/superuser

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Automatically set company if not set
        """
        if not self.company_id:
            current_company = get_current_company()
            if current_company:
                self.company = current_company
        super().save(*args, **kwargs)
