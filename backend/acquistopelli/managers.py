from django.db import models
from django.db.models import (ExpressionWrapper, F, IntegerField, OuterRef,
                              Subquery, Sum)
from django.db.models.functions import Coalesce


class LottoQuerySet(models.QuerySet):
    def con_pelli_disponibili(self):
        from vendite.models import \
            XRScelteSchede  # Import ritardato per evitare cicli

        from .models import \
            SceltaLotto  # Import locale per evitare import circolari

        used_quantity_subquery = XRScelteSchede.objects.filter(
            fk_sceltalotto=OuterRef('pk')
        ).values('fk_sceltalotto').annotate(
            used=Sum('quantity')
        ).values('used')[:1]

        scelte_con_rimanenza = SceltaLotto.objects.annotate(
            used_quantity=Coalesce(Subquery(used_quantity_subquery), 0),
            remaining=ExpressionWrapper(
                F('pezzi') - Coalesce(Subquery(used_quantity_subquery), 0),
                output_field=IntegerField()
            )
        ).filter(remaining__gt=0)

        return self.filter(sceltalotto__in=scelte_con_rimanenza).distinct()


class LottoManager(models.Manager):
    def get_queryset(self):
        return LottoQuerySet(self.model, using=self._db)

    def con_pelli_disponibili(self):
        return self.get_queryset().con_pelli_disponibili()